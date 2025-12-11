# 🚀 AWS Deployment Guide - Forum Application

## 📋 Przegląd

Ten folder zawiera kompletną dokumentację do wdrożenia aplikacji Forum na AWS. Deployment podzielony jest na 2 dni (6-8 godzin total).

**⚠️ WAŻNE:** To jest Twój pierwszy deployment na AWS? Przeczytaj WSZYSTKO w tej kolejności!

---

## 🎯 Architektura Finalna

```
┌─────────────────────────────────────────────────────────────┐
│                      CLOUDFLARE                              │
│  • DNS Management                                            │
│  • SSL/TLS Certificate (Let's Encrypt)                       │
│  • WAF (Web Application Firewall)                            │
│  • DDoS Protection                                           │
│  • CDN (Content Delivery Network)                            │
│  • Rate Limiting                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                   AWS CLOUD                                  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Application Load Balancer (ALB)               │ │
│  │            Public Subnets (2 AZ)                       │ │
│  └──────────────────────┬─────────────────────────────────┘ │
│                         │                                    │
│                         ↓                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │       Auto Scaling Group (Private Subnets)             │ │
│  │                                                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │ │
│  │  │ EC2 t2.micro │  │ EC2 t2.micro │  │ EC2 t2.micro │ │ │
│  │  │              │  │              │  │              │ │ │
│  │  │ • Nginx :80  │  │ • Nginx :80  │  │ • Nginx :80  │ │ │
│  │  │ • Django     │  │ • Django     │  │ • Django     │ │ │
│  │  │   :8000      │  │   :8000      │  │   :8000      │ │ │
│  │  │ • React      │  │ • React      │  │ • React      │ │ │
│  │  │   (static)   │  │   (static)   │  │   (static)   │ │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │ │
│  └─────────┼──────────────────┼──────────────────┼─────────┘ │
│            │                  │                  │           │
│            └──────────────────┼──────────────────┘           │
│                               ↓                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         RDS PostgreSQL (t4g.micro)                     │ │
│  │              Private Subnet                             │ │
│  │         (tylko EC2 ma dostęp)                           │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         S3 Bucket (React Frontend Builds)              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         ECR (Docker Images Repository)                 │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Struktura Dokumentacji

| Plik | Czas | Opis |
|------|------|------|
| **[DAY_1_INFRASTRUCTURE.md](DAY_1_INFRASTRUCTURE.md)** | 3-4h | Setup infrastruktury AWS (VPC, Subnets, RDS, ALB, Security Groups) |
| **[DAY_2_DEPLOYMENT.md](DAY_2_DEPLOYMENT.md)** | 3-4h | Deployment aplikacji (Docker, ECR, ASG, Cloudflare) |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | - | Cheatsheet - szybkie komendy AWS CLI |
| **[../AWS_IDs_TRACKER.md](../AWS_IDs_TRACKER.md)** | - | Notatnik na ID zasobów AWS (wypełniajcie w trakcie!) |

---

## 💰 Koszty

### AWS Free Tier (pierwsze 12 miesięcy):
- **EC2 t2.micro:** 750h/miesiąc = DARMOWE dla 1 instancji 24/7
- **RDS t4g.micro:** 750h/miesiąc = DARMOWE dla 1 instancji 24/7
- **ALB:** 750h/miesiąc + 15GB data processing = DARMOWE
- **S3:** 5GB storage = DARMOWE
- **Data Transfer:** 15GB out/miesiąc = DARMOWE

**Szacunkowy koszt w Free Tier:** ~$0-8/miesiąc (głównie data transfer powyżej limitu)

### Po Free Tier (od 13 miesiąca):
- EC2 t2.micro: ~$8.50/mies
- RDS t4g.micro: ~$13/mies
- ALB: ~$16/mies
- S3: ~$0.50/mies
- Data Transfer: ~$9/mies
- NAT Gateway: ~$9/mies

**Szacunkowy koszt:** ~$56/miesiąc

### Cloudflare:
- **Free Plan** - w pełni wystarczający (DNS, SSL, CDN, WAF, DDoS)

---

## 🎓 Wymagania - CO MUSISZ MIEĆ

### 1. Konto AWS
- [ ] Utworzone konto AWS (karta kredytowa potrzebna do weryfikacji)
- [ ] Włączony Free Tier
- [ ] Region wybrany: **eu-central-1** (Frankfurt)

### 2. Zainstalowane narzędzia
- [ ] **AWS CLI** (wersja 2) - [Instalacja](https://aws.amazon.com/cli/)
- [ ] **Docker Desktop** - [Instalacja](https://www.docker.com/products/docker-desktop)
- [ ] **Git** (już masz ✅)
- [ ] **Node.js 16+** (już masz ✅)

### 3. Konto Cloudflare
- [ ] Utworzone konto na [cloudflare.com](https://cloudflare.com)
- [ ] Domena (może być darmowa z [freenom.com](https://freenom.com) lub [dot.tk](http://dot.tk))

### 4. Dostęp do repozytorium
- [ ] Sklonowane repo: `git clone https://github.com/tomisworking/webapp.git`
- [ ] Branch main jest aktualny: `git pull origin main`

---

## ⚙️ Setup Przed Startem

### 1. Zainstaluj AWS CLI

**Windows:**
```powershell
# Pobierz i zainstaluj z:
https://awscli.amazonaws.com/AWSCLIV2.msi

# Sprawdź instalację
aws --version
```

**Mac:**
```bash
brew install awscli
aws --version
```

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

### 2. Skonfiguruj AWS CLI

```bash
aws configure
```

Podaj:
- **AWS Access Key ID:** [z AWS Console → IAM → Users → Security credentials]
- **AWS Secret Access Key:** [z AWS Console → IAM → Users → Security credentials]
- **Default region:** `eu-central-1`
- **Default output format:** `json`

**Sprawdź konfigurację:**
```bash
aws sts get-caller-identity
```

Powinno pokazać Twoje konto AWS.

### 3. Zainstaluj Docker Desktop

**Windows/Mac:**
1. Pobierz: https://www.docker.com/products/docker-desktop
2. Zainstaluj
3. Uruchom Docker Desktop
4. Sprawdź:
```bash
docker --version
docker ps
```

---

## 📝 Plan Działania

### **Dzień 1: Infrastruktura AWS (3-4 godziny)**

**Cel:** Utworzenie wszystkich zasobów AWS (VPC, RDS, ALB, Security Groups)

**Co zrobisz:**
1. ✅ Setup VPC i Subnets (publiczne i prywatne)
2. ✅ Setup Internet Gateway i NAT Gateway
3. ✅ Utworzenie Security Groups
4. ✅ Utworzenie bazy danych RDS PostgreSQL
5. ✅ Utworzenie Application Load Balancer
6. ✅ Utworzenie Target Group
7. ✅ Utworzenie ECR Repository (dla Docker images)
8. ✅ Setup IAM Roles dla EC2
9. ✅ Utworzenie S3 Bucket (dla React buildu)

**Dokumentacja:** [DAY_1_INFRASTRUCTURE.md](DAY_1_INFRASTRUCTURE.md)

---

### **Dzień 2: Deployment Aplikacji (3-4 godziny)**

**Cel:** Deployment Django + React + konfiguracja Cloudflare

**Co zrobisz:**
1. ✅ Build i push Docker image do ECR
2. ✅ Build React frontend i upload do S3
3. ✅ Utworzenie Launch Template dla EC2
4. ✅ Utworzenie Auto Scaling Group
5. ✅ Migracja bazy danych
6. ✅ Konfiguracja Cloudflare (DNS, SSL, WAF)
7. ✅ Testowanie całej aplikacji
8. ✅ Setup CI/CD (GitHub Actions)

**Dokumentacja:** [DAY_2_DEPLOYMENT.md](DAY_2_DEPLOYMENT.md)

---

## 🆘 Troubleshooting

### "AWS CLI nie jest rozpoznawane"
- Uruchom ponownie terminal po instalacji
- Sprawdź PATH (Windows: dodaj `C:\Program Files\Amazon\AWSCLIV2\` do PATH)

### "Docker daemon is not running"
- Uruchom Docker Desktop
- Sprawdź czy ikona Docker jest w tray

### "Permission denied" przy Docker
- **Linux/Mac:** Dodaj użytkownika do grupy docker: `sudo usermod -aG docker $USER`
- Wyloguj się i zaloguj ponownie

### "Access Denied" w AWS
- Sprawdź czy AWS CLI jest skonfigurowane: `aws configure list`
- Sprawdź uprawnienia IAM użytkownika (potrzebujesz AdministratorAccess)

---

## 📚 Przydatne Linki

- **AWS Console:** https://console.aws.amazon.com/
- **AWS Free Tier:** https://aws.amazon.com/free/
- **AWS CLI Docs:** https://docs.aws.amazon.com/cli/
- **Docker Docs:** https://docs.docker.com/
- **Cloudflare Docs:** https://developers.cloudflare.com/

---

## ✅ Checklist Przed Startem

Upewnij się, że masz:

- [ ] Konto AWS utworzone i zweryfikowane
- [ ] AWS CLI zainstalowane i skonfigurowane
- [ ] Docker Desktop zainstalowany i uruchomiony
- [ ] Konto Cloudflare utworzone
- [ ] Domenę (może być darmowa)
- [ ] Sklonowane repozytorium
- [ ] Plik `AWS_IDs_TRACKER.md` otwarty do zapisywania ID

**Gotowy? Przejdź do:** [DAY_1_INFRASTRUCTURE.md](DAY_1_INFRASTRUCTURE.md) 🚀

---

## 💡 Wskazówki

- **Zapisuj wszystkie ID:** Używaj `AWS_IDs_TRACKER.md` do notowania VPC ID, Subnet ID, itp.
- **Nie spieszysz się:** Lepiej zrobić wolno i dobrze niż szybko i źle
- **Rób screenshoty:** Przydadzą się przy troubleshooting
- **Czytaj błędy:** AWS podaje dokładne komunikaty o błędach
- **Pytaj:** Jeśli coś nie działa, sprawdź najpierw dokumentację

---

**Powodzenia! 🎉**

