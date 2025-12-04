# 🏗️ Jak działa Auto Scaling i Load Balancer w Twojej architekturze

## 📊 Architektura ogólna

```
Internet (Użytkownicy)
    ↓
Cloudflare (DNS, SSL, CDN, WAF)
    ↓
Application Load Balancer (ALB) - forum-alb
    ↓
Auto Scaling Group (ASG) - forum-asg
    ↓
EC2 Instances (1-4 instancji)
    ├─ Nginx (reverse proxy)
    ├─ Django (Docker container)
    └─ React Frontend (static files)
    ↓
RDS PostgreSQL (baza danych)
```

---

## ⚖️ Application Load Balancer (ALB)

### Co robi ALB?

**ALB działa w public subnets** i:
1. Przyjmuje requesty z internetu (przez Cloudflare)
2. Rozdziela ruch między wiele EC2 instances (load balancing)
3. Sprawdza czy instancje są zdrowe (health checks)
4. Przekierowuje ruch tylko do healthy instances

### Konfiguracja ALB:

**Lokalizacja:**
- **VPC:** `forum-vpc`
- **Subnets:** 2 public subnets w różnych Availability Zones
  - `forum-public-subnet-1a` (us-east-1a)
  - `forum-public-subnet-1b` (us-east-1b)
- **Security Group:** `forum-alb-sg`
  - Pozwala HTTP (80) i HTTPS (443) z `0.0.0.0/0` (anywhere)

**Listener:**
- **Port:** 80 (HTTP)
- **Action:** Forward to Target Group (`forum-tg`)

**Target Group:** `forum-tg`
- **Protocol:** HTTP
- **Port:** 80
- **Health check:** `/health` endpoint
- **Health check interval:** 30 seconds
- **Healthy threshold:** 2 (po 2 sukcesach = healthy)
- **Unhealthy threshold:** 2 (po 2 porażkach = unhealthy)

---

## 🔄 Auto Scaling Group (ASG)

### Co robi ASG?

**ASG działa w private subnets** i:
1. Automatycznie tworzy/usuwa EC2 instances
2. Utrzymuje określoną liczbę instancji (Desired Capacity)
3. Rejestruje instancje w Target Group ALB
4. Reaguje na health checks (tworzy nowe instancje jeśli stare są unhealthy)
5. Rozkłada instancje między Availability Zones (redundancja)

### Konfiguracja ASG:

**Capacity:**
- **Desired Capacity:** 2 instancje
- **Minimum:** 1 instancja
- **Maximum:** 4 instancje

**Lokalizacja:**
- **VPC:** `forum-vpc`
- **Subnets:** 2 private subnets w różnych Availability Zones
  - `forum-private-subnet-1a` (us-east-1a)
  - `forum-private-subnet-1b` (us-east-1b)

**Launch Template:** `forum-launch-template`
- **AMI:** Amazon Linux 2023
- **Instance Type:** t3.micro (Free Tier)
- **IAM Role:** `forum-ec2-role`
- **Security Group:** `forum-ec2-sg`
  - Pozwala HTTP (80) tylko z `forum-alb-sg`
  - Pozwala SSH (22) z My IP (zarządzanie)
- **User Data:** Bash script z `user_data.txt`

**Health Checks:**
- **Type:** ELB (ALB health checks)
- **Grace Period:** 300 seconds (5 minut)

---

## 🔄 Przepływ ruchu (Request Flow)

### 1. Użytkownik wchodzi na https://kongoapp.pl

```
1. DNS (kongoapp.pl) → Cloudflare IP
2. Cloudflare → ALB (przez A record)
3. ALB → wybiera healthy EC2 instance
4. EC2 (Nginx) → zwraca React frontend
```

### 2. Frontend robi request do API

```
1. Frontend: GET /api/categories/
2. Cloudflare → ALB
3. ALB → wybiera healthy EC2 instance
4. EC2 Nginx → proxy do Django (port 8000)
5. Django → RDS PostgreSQL
6. Django → zwraca JSON
7. ALB → Cloudflare → User
```

---

## 🎯 Dlaczego te subnety?

### Public Subnets (dla ALB):
- Mają route do Internet Gateway
- Publiczne IP
- Dostępne z internetu

### Private Subnets (dla EC2):
- Mają route do NAT Gateway (tylko outbound)
- Brak publicznych IP
- Nie są bezpośrednio dostępne z internetu
- **Bezpieczniejsze** - ALB jest jedynym punktem wejścia

---

## 🔧 Launch Template vs Auto Scaling Group

### Launch Template określa:
- **Co** uruchomić (AMI, instance type)
- **Jak** skonfigurować (user data, IAM role)
- **Security Group** dla instancji

### Auto Scaling Group określa:
- **Gdzie** uruchomić (subnets, Availability Zones)
- **Ile** instancji (min/max/desired)
- **Kiedy** skalować (health checks, triggers)

### ⚠️ WAŻNE: Subnet configuration

**W Launch Template:**
- ❌ **NIE** wybieraj konkretnego subnetu
- ✅ Zostaw puste

**W Auto Scaling Group:**
- ✅ Wybierz subnets (private subnets)
- ASG automatycznie rozkłada instancje między te subnety

**Dlaczego?**
- Launch Template definiuje "template" (szablon)
- ASG używa tego szablonu i decyduje gdzie uruchomić instancje
- Jeśli wybierzesz subnet w Launch Template, to go "na sztywno" ustawia
- ASG wtedy nie może dynamicznie wybierać między subnetami

---

## 🔄 Instance Refresh - jak to działa?

Gdy uruchamiasz Instance Refresh:

### Krok 1: ASG tworzy nową instancję
1. Używa Launch Template (z nowym user_data)
2. Uruchamia instancję w jednym z private subnets
3. Instancja wykonuje user_data script:
   - Instaluje Docker, Nginx
   - Pobiera Django image z ECR
   - Pobiera React build z S3
   - Konfiguruje Nginx
   - Uruchamia wszystko

### Krok 2: Health Checks
1. ALB zaczyna health checks na `/health` endpoint
2. Po 2 sukcesach (60 sekund) → instancja = **healthy**
3. ALB zaczyna wysyłać ruch do nowej instancji

### Krok 3: ASG terminuje starą instancję
1. ASG czeka na Instance Warmup (60 sekund)
2. ASG czeka aż nowa instancja przejdzie health checks
3. ASG terminuje starą instancję
4. Powtarza dla drugiej instancji

### Krok 4: Zakończenie
- Wszystkie instancje zaktualizowane
- ASG używa nowego Launch Template version

**Replacement Method:**
- **Prioritize availability:** Tworzy nowe przed terminowaniem starych
  - Może być 3-4 instancje przez moment (kosztuje więcej)
  - Lepsze dla produkcji (zero downtime)

---

## 🔒 Security Groups - jak współpracują?

### forum-alb-sg (ALB Security Group)
```
Inbound:
  - HTTP (80) z 0.0.0.0/0 (anywhere)
  - HTTPS (443) z 0.0.0.0/0 (anywhere)

Outbound:
  - All traffic do 0.0.0.0/0
```

### forum-ec2-sg (EC2 Security Group)
```
Inbound:
  - HTTP (80) tylko z forum-alb-sg ← WAŻNE!
  - SSH (22) z My IP

Outbound:
  - All traffic do 0.0.0.0/0
```

**Security Group reference:**
- EC2 przyjmuje HTTP tylko z ALB Security Group
- Nawet jeśli ktoś zna IP instancji, nie może się połączyć bezpośrednio
- Tylko ALB może wysyłać ruch do instancji

---

## 🎯 Dlaczego ten błąd subnet/security group?

Błąd:
```
Security group sg-xxx and subnet subnet-xxx belong to different networks
```

**Przyczyna:**
- Launch Template ma wybrany subnet Z INNEGO VPC
- LUB Security Group Z INNEGO VPC
- AWS wymaga aby były w tym samym VPC

**Rozwiązanie:**
1. W Launch Template → Network settings → Subnet: **Zostaw puste**
2. ASG wybierze odpowiednie subnety automatycznie
3. Security Group musi być z `forum-vpc` (sprawdź w EC2 → Security Groups)

---

## 📋 Twoja konfiguracja (powinna być):

| Zasób | VPC | Subnets | Security Group |
|-------|-----|---------|----------------|
| **ALB** | forum-vpc | 2 public subnets | forum-alb-sg |
| **ASG** | forum-vpc | 2 private subnets | (określone w Launch Template) |
| **EC2 (przez Launch Template)** | (z ASG) | (z ASG) | forum-ec2-sg |
| **RDS** | forum-vpc | 2 database subnets | forum-rds-sg |

---

## 🔍 Debug: Jak sprawdzić co się dzieje?

### 1. Sprawdź ALB Target Group Health
```
EC2 → Target Groups → forum-tg → Targets tab
```
- Ile instancji jest healthy?
- Jakie są health status details?

### 2. Sprawdź ASG Activity
```
EC2 → Auto Scaling Groups → forum-asg → Activity tab
```
- Czy instancje się uruchamiają?
- Czy są błędy?

### 3. Sprawdź Instance Launch
```
EC2 → Instances
```
- Czy nowe instancje mają status "running"?
- Czy mają prywatne IP (z private subnet)?
- Czy są w Target Group?

### 4. Sprawdź User Data Logs (na instancji)
```bash
# Session Manager
sudo tail -100 /var/log/user-data.log
```

---

**Ostatnia aktualizacja:** 2025-11-27












