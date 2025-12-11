# 🚀 AWS Deployment Guide - Forum Application

Kompleksowy przewodnik wdrożenia aplikacji na AWS dla początkujących.

## 📋 Spis treści

1. [Przygotowanie](#przygotowanie)
2. [Lokalne testy z Docker](#lokalne-testy)
3. [Setup AWS](#setup-aws)
4. [Deployment](#deployment)
5. [Migracja danych](#migracja-danych)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Przygotowanie

### Wymagania

- Konto AWS (Free Tier)
- Zainstalowany Docker Desktop
- Python 3.11+
- Node.js 18+
- Git

### Struktura projektu (po zmianach)

```
WEBAPP/
├── backend/
│   ├── config/              # Django settings
│   ├── users/               # Users app
│   ├── forum/               # Forum app
│   ├── Dockerfile           # ✨ NOWY
│   ├── docker-entrypoint.sh # ✨ NOWY
│   ├── nginx/
│   │   └── nginx.conf       # ✨ NOWY
│   ├── .env.example         # ✨ NOWY
│   └── requirements.txt     # ✨ ZAKTUALIZOWANY
├── frontend/
├── docker-compose.yml       # ✨ NOWY
├── .github/workflows/
│   └── deploy-aws.yml       # ✨ NOWY
└── scripts/
    └── migrate_sqlite_to_postgres.py  # ✨ NOWY
```

---

## 🧪 Lokalne testy z Docker (opcjonalnie)

### Opcja A: SQLite (jak dotychczas)

Możesz nadal pracować lokalnie z SQLite - **to jest OK!**

```bash
cd backend
python manage.py runserver
```

### Opcja B: PostgreSQL przez Docker (test przed AWS)

Jeśli chcesz przetestować PostgreSQL lokalnie:

```bash
# 1. Utwórz plik .env w backend/
cp backend/.env.example backend/.env

# 2. Edytuj .env - odkomentuj DATABASE_URL:
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/forumdb

# 3. Uruchom wszystko przez Docker Compose
docker-compose up -d

# 4. Sprawdź czy działa
curl http://localhost/api/health/

# 5. Utwórz superusera
docker-compose exec django python manage.py createsuperuser

# 6. Załaduj dane testowe
docker-compose exec django python manage.py seed_data
```

**Ważne:** To jest tylko do TESTÓW! Na AWS będziesz używać RDS PostgreSQL.

---

## ☁️ Setup AWS

### Krok 1: Utworzenie konta AWS

1. Idź na: https://aws.amazon.com/free
2. "Create a Free Account"
3. Podaj dane + kartę kredytową (weryfikacja, nie pobiera opłat)
4. Wybierz "Basic Support - Free"

### Krok 2: Konfiguracja IAM

Po zalogowaniu do AWS Console:

1. **Włącz MFA dla root account:**
   - Kliknij swoją nazwę (góra prawa)
   - "Security credentials"
   - "Assign MFA device"
   - Użyj np. Google Authenticator

2. **Utwórz IAM user dla siebie:**
   - IAM → Users → Add user
   - Username: twoje-imie
   - Access: AWS Management Console + Programmatic
   - Permissions: AdministratorAccess
   - Zapisz Access Key ID i Secret!

3. **Zaloguj się jako IAM user** (już nie jako root)

### Krok 3: Wybór regionu

W AWS Console (góra prawa) wybierz: **Europe (Frankfurt) eu-central-1**

Wszystkie zasoby twórz w tym regionie!

---

## 🏗️ Tworzenie infrastruktury AWS

### Krok 4: VPC i Subnets

**AWS Console → VPC → Create VPC**

1. **VPC:**
   - Name: `forum-vpc`
   - CIDR: `10.0.0.0/16`
   - Tenancy: Default

2. **Internet Gateway:**
   - Name: `forum-igw`
   - Attach to `forum-vpc`

3. **Subnets (utwórz 4):**
   
   **Public Subnet 1:**
   - Name: `forum-public-1a`
   - VPC: forum-vpc
   - AZ: eu-central-1a
   - CIDR: `10.0.1.0/24`
   
   **Public Subnet 2:**
   - Name: `forum-public-1b`
   - VPC: forum-vpc
   - AZ: eu-central-1b
   - CIDR: `10.0.2.0/24`
   
   **Private Subnet 1:**
   - Name: `forum-private-1a`
   - VPC: forum-vpc
   - AZ: eu-central-1a
   - CIDR: `10.0.10.0/24`
   
   **Private Subnet 2:**
   - Name: `forum-private-1b`
   - VPC: forum-vpc
   - AZ: eu-central-1b
   - CIDR: `10.0.11.0/24`

4. **NAT Gateway** (dla private subnets):
   - Name: `forum-nat-gw`
   - Subnet: `forum-public-1a`
   - Elastic IP: Allocate (przycisk)

5. **Route Tables:**
   
   **Public Route Table:**
   - Name: `forum-public-rt`
   - VPC: forum-vpc
   - Routes: 
     - `0.0.0.0/0` → Internet Gateway
   - Associate: forum-public-1a, forum-public-1b
   
   **Private Route Table:**
   - Name: `forum-private-rt`
   - VPC: forum-vpc
   - Routes:
     - `0.0.0.0/0` → NAT Gateway
   - Associate: forum-private-1a, forum-private-1b

### Krok 5: Security Groups

**VPC → Security Groups → Create**

**1. ALB Security Group:**
```
Name: forum-alb-sg
VPC: forum-vpc
Inbound rules:
  - HTTP (80) from 0.0.0.0/0
  - HTTPS (443) from 0.0.0.0/0
Outbound rules:
  - All traffic to 0.0.0.0/0
```

**2. EC2 Security Group:**
```
Name: forum-ec2-sg
VPC: forum-vpc
Inbound rules:
  - HTTP (80) from forum-alb-sg
  - SSH (22) from your IP (znajdź na: https://whatismyip.com)
Outbound rules:
  - All traffic to 0.0.0.0/0
```

**3. RDS Security Group:**
```
Name: forum-rds-sg
VPC: forum-vpc
Inbound rules:
  - PostgreSQL (5432) from forum-ec2-sg
Outbound rules:
  - None (default deny)
```

### Krok 6: RDS PostgreSQL

**RDS → Create database**

```
Creation method: Standard create
Engine: PostgreSQL 15.x
Templates: Free tier
DB instance identifier: forum-db

Credentials:
  Master username: forumadmin
  Master password: [SILNE HASŁO - zapisz!]

Instance configuration:
  DB instance class: db.t3.micro (free tier)

Storage:
  Storage type: GP3
  Allocated storage: 20 GB
  Enable storage autoscaling: Yes
  Maximum storage threshold: 100 GB

Connectivity:
  VPC: forum-vpc
  Subnet group: Create new
  Public access: No
  VPC security group: forum-rds-sg
  Availability Zone: eu-central-1a

Database authentication: Password
  
Additional configuration:
  Initial database name: forumdb
  DB parameter group: default
  Backup retention period: 7 days
  Enable encryption: Yes
  Enable Enhanced monitoring: No (oszczędność)
```

**Czas utworzenia: ~10 minut**

Po utworzeniu zapisz **Endpoint** (np. `forum-db.xxxxx.eu-central-1.rds.amazonaws.com`)

### Krok 7: ECR (Docker Registry)

**ECR → Create repository**

```
Repository name: forum-backend
Visibility: Private
Image scanning: Scan on push
Encryption: AES-256
```

### Krok 8: Application Load Balancer

**EC2 → Load Balancers → Create Load Balancer**

```
Type: Application Load Balancer
Name: forum-alb
Scheme: Internet-facing
IP address type: IPv4

Network mapping:
  VPC: forum-vpc
  Subnets: forum-public-1a, forum-public-1b

Security groups: forum-alb-sg

Listeners:
  Protocol: HTTP
  Port: 80
  Default action: Create target group (następny krok)
```

**Target Group:**
```
Target type: Instances
Target group name: forum-tg
Protocol: HTTP
Port: 80
VPC: forum-vpc

Health checks:
  Protocol: HTTP
  Path: /api/health/
  Port: traffic port
  Healthy threshold: 2
  Unhealthy threshold: 2
  Timeout: 5
  Interval: 30
```

Zapisz **ALB DNS name** (np. `forum-alb-1234567890.eu-central-1.elb.amazonaws.com`)

### Krok 9: Launch Template

**EC2 → Launch Templates → Create**

```
Name: forum-launch-template
AMI: Amazon Linux 2023 (najnowszy)
Instance type: t2.micro
Key pair: Create new (zapisz .pem file!)
```

**Network settings:**
- Don't include in launch template (będzie w ASG)

**Security groups:**
- forum-ec2-sg

**Advanced details → User data:**

```bash
#!/bin/bash
# Update system
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install AWS CLI (if not present)
yum install -y aws-cli

# Get database URL from Parameter Store
export DATABASE_URL=$(aws ssm get-parameter --name "/forum/DATABASE_URL" --with-decryption --region eu-central-1 --query 'Parameter.Value' --output text)
export SECRET_KEY=$(aws ssm get-parameter --name "/forum/SECRET_KEY" --with-decryption --region eu-central-1 --query 'Parameter.Value' --output text)

# Login to ECR
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com

# Pull and run Docker image
docker pull YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/forum-backend:latest

docker run -d \
  --name forum-backend \
  --restart unless-stopped \
  -p 8000:8000 \
  -e DATABASE_URL="$DATABASE_URL" \
  -e SECRET_KEY="$SECRET_KEY" \
  -e DEBUG=False \
  -e ALLOWED_HOSTS="forum-alb-1234567890.eu-central-1.elb.amazonaws.com" \
  YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/forum-backend:latest

# Install and configure Nginx
yum install -y nginx
# ... nginx config (następny krok)
```

**UWAGA:** Zastąp `YOUR_AWS_ACCOUNT_ID` swoim AWS Account ID (znajdziesz w prawym górnym rogu Console)

### Krok 10: Auto Scaling Group

**EC2 → Auto Scaling Groups → Create**

```
Name: forum-asg

Launch template: forum-launch-template

VPC: forum-vpc
Subnets: forum-private-1a, forum-private-1b

Load balancing:
  Attach to existing load balancer
  Target group: forum-tg

Health checks:
  ELB health check: Enable
  Health check grace period: 300 seconds

Group size:
  Desired: 2
  Minimum: 1
  Maximum: 3

Scaling policies:
  Target tracking scaling policy
  Metric: Average CPU utilization
  Target value: 70
```

---

## 🔐 AWS Systems Manager - Secrets

**Systems Manager → Parameter Store → Create parameter**

Utwórz 3 parametry:

**1. DATABASE_URL:**
```
Name: /forum/DATABASE_URL
Type: SecureString
Value: postgresql://forumadmin:TWOJE_HASŁO@forum-db.xxxxx.eu-central-1.rds.amazonaws.com:5432/forumdb
```

**2. SECRET_KEY:**
```
Name: /forum/SECRET_KEY
Type: SecureString
Value: [wygeneruj długi losowy string]
```

Wygeneruj SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**3. ALLOWED_HOSTS:**
```
Name: /forum/ALLOWED_HOSTS
Type: String
Value: forum-alb-1234567890.eu-central-1.elb.amazonaws.com
```

---

## 🚢 Pierwszy Deployment

### Krok 11: Zbuduj i wyślij Docker image

```bash
# 1. Zaloguj się do AWS ECR
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com

# 2. Zbuduj image
cd backend
docker build -t forum-backend .

# 3. Tag image
docker tag forum-backend:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/forum-backend:latest

# 4. Push do ECR
docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/forum-backend:latest
```

### Krok 12: Uruchom instancje EC2

Auto Scaling Group automatycznie uruchomi 2 instancje.

Sprawdź: **EC2 → Instances** - powinny być 2 instancje z nazwą `forum-asg`

### Krok 13: Migracja bazy danych

```bash
# Połącz się z EC2 przez Session Manager lub SSH
aws ssm start-session --target INSTANCE_ID

# Na EC2:
docker exec forum-backend python manage.py migrate
docker exec forum-backend python manage.py createsuperuser
docker exec forum-backend python manage.py seed_data
```

### Krok 14: Test aplikacji

```bash
# Test health check
curl http://ALB_DNS_NAME/api/health/

# Test API
curl http://ALB_DNS_NAME/api/categories/
```

---

## 🌍 Cloudflare Setup

1. **Kup domenę** (np. `mojeforum.pl` na OVH za ~20zł/rok)

2. **Dodaj do Cloudflare:**
   - Cloudflare.com → Add site
   - Zmień nameservery na OVH na te z Cloudflare

3. **DNS Record:**
   ```
   Type: CNAME
   Name: api
   Target: forum-alb-1234567890.eu-central-1.elb.amazonaws.com
   Proxy: ON (pomarańczowa chmurka)
   ```

4. **SSL/TLS:**
   - SSL/TLS → Full (strict)

5. **Aktualizuj ALLOWED_HOSTS:**
   ```
   /forum/ALLOWED_HOSTS = api.mojeforum.pl,forum-alb-xxx.elb.amazonaws.com
   ```

---

## 📊 Migracja danych SQLite → PostgreSQL

Jeśli masz dane w SQLite które chcesz przenieść:

```bash
# 1. Lokalnie - eksport danych
cd backend
python ../scripts/migrate_sqlite_to_postgres.py export

# 2. Plik backups/data_export.json - skopiuj na serwer
# Możesz użyć S3 jako pośrednika:
aws s3 cp backups/data_export.json s3://TWOJ_BUCKET/

# 3. Na EC2 - pobierz i importuj
aws s3 cp s3://TWOJ_BUCKET/data_export.json /tmp/
docker cp /tmp/data_export.json forum-backend:/app/
docker exec forum-backend python manage.py loaddata /app/data_export.json
```

---

## 🐛 Troubleshooting

### Problem: EC2 nie może połączyć się z RDS

**Rozwiązanie:**
- Sprawdź Security Groups
- RDS-SG musi mieć inbound rule: Port 5432 from EC2-SG
- Test z EC2:
  ```bash
  docker exec forum-backend python -c "import psycopg2; conn = psycopg2.connect('$DATABASE_URL'); print('OK')"
  ```

### Problem: ALB Health Check fails

**Rozwiązanie:**
- Sprawdź czy aplikacja działa: `docker logs forum-backend`
- Test endpoint: `curl localhost:8000/api/health/`
- Sprawdź Security Group EC2-SG: musi mieć port 80 from ALB-SG

### Problem: Docker image nie startuje

**Rozwiązanie:**
```bash
# Zobacz logi
docker logs forum-backend

# Sprawdź czy wszystkie zmienne są ustawione
docker exec forum-backend env | grep DATABASE_URL
```

---

## 📝 Koszty szacunkowe

W ramach AWS Free Tier (12 miesięcy):
- EC2 t2.micro: 750h/miesiąc = DARMOWE (dla 1 instancji 24/7)
- RDS db.t3.micro: 750h/miesiąc = DARMOWE
- ALB: 750h/miesiąc + 15GB = ~$5/miesiąc
- NAT Gateway: ~$30/miesiąc ⚠️

**Total: ~$35/miesiąc**

**Oszczędność:** Możecie wyłączać środowisko gdy nie używacie (wieczory/weekendy)

---

## ✅ Checklist - Co masz już zrobione?

- [ ] Konto AWS utworzone
- [ ] VPC i Subnets skonfigurowane
- [ ] Security Groups utworzone
- [ ] RDS PostgreSQL działa
- [ ] ECR repository utworzone
- [ ] ALB i Target Group działa
- [ ] Launch Template gotowy
- [ ] Auto Scaling Group uruchomiony
- [ ] Docker image w ECR
- [ ] Aplikacja odpowiada na /api/health/
- [ ] Baza danych zmigrowana
- [ ] Cloudflare skonfigurowany

---

## 🎯 Następne kroki

Po działającym deploymencie:
1. **L5**: CI/CD już działa (GitHub Actions)
2. **L6**: Dodaj SAST/DAST do pipeline
3. **L7**: Zaimplementuj WAF w Django
4. **L8**: Hardening EC2 i RDS (CIS benchmarks)
5. **L9**: Testy bezpieczeństwa

---

**Pytania? Problemy?** Zobacz `docs/TROUBLESHOOTING.md` lub pytaj na zespołowym chacie!

