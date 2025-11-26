# 📅 DAY 2: Deployment Aplikacji

**Czas:** 3-4 godziny  
**Cel:** Deployment Django + React + konfiguracja Cloudflare

⚠️ **WAŻNE:** Musisz mieć ukończony DAY 1! Sprawdź czy wszystkie zasoby są utworzone.

---

## 🎯 Co zrobimy dzisiaj?

1. ✅ Setup AWS Systems Manager Parameter Store (secrets)
2. ✅ Build i push Docker image do ECR
3. ✅ Build React frontend i upload do S3
4. ✅ Utworzenie Launch Template dla EC2
5. ✅ Utworzenie Auto Scaling Group
6. ✅ Test połączenia z bazą danych
7. ✅ Migracja bazy danych
8. ✅ Konfiguracja Cloudflare (DNS, SSL, WAF)
9. ✅ Test całej aplikacji
10. ✅ (Opcjonalnie) Setup GitHub Actions CI/CD

---

## 📋 Przed Rozpoczęciem

### Sprawdź czy masz:
- [ ] Wszystkie ID z DAY 1 zapisane w `AWS_IDs_TRACKER.md`
- [ ] RDS Status: **Available**
- [ ] ALB Status: **Active**
- [ ] Docker Desktop uruchomiony
- [ ] AWS CLI skonfigurowane
- [ ] Sklonowane repo: `git pull origin main`

### 📂 WAŻNE: Otwórz plik `AWS_IDs_TRACKER.md`
**Wszystkie wartości potrzebne w tym tutorialu znajdują się w `AWS_IDs_TRACKER.md`!**

Podczas wykonywania kroków, będziemy się odwoływać do wartości z tego pliku w formacie:
- `[AWS_IDs_TRACKER: RDS Endpoint]` = Zobacz sekcję "RDS POSTGRESQL" w AWS_IDs_TRACKER.md
- `[AWS_IDs_TRACKER: ALB DNS]` = Zobacz sekcję "LOAD BALANCER" w AWS_IDs_TRACKER.md
- itd.

---

## 📖 Jak Używać AWS_IDs_TRACKER.md

**W tym tutorialu często zobaczysz:**
```
[AWS_IDs_TRACKER: Nazwa Wartości]
```

To oznacza: **Otwórz plik `AWS_IDs_TRACKER.md` i znajdź tę wartość!**

### Przykład:
Gdy widzisz:
```bash
docker tag forum-backend:latest [AWS_IDs_TRACKER: ECR URI]:latest
```

1. Otwórz `AWS_IDs_TRACKER.md`
2. Znajdź sekcję "📦 ECR REPOSITORY"
3. Skopiuj wartość z pola "ECR URI"
4. Wklej ją w poleceniu

### 💡 Wskazówka:
Miej otwarty `AWS_IDs_TRACKER.md` w drugim oknie/monitorze podczas całego deploymentu!

---

## 🔐 KROK 1: Parameter Store (Secrets)

**Co to jest Parameter Store?** Bezpieczne przechowywanie sekretów (hasła, klucze API).

### 1.1. Wygeneruj Django SECRET_KEY

**Otwórz terminal/PowerShell w folderze projektu:**

```bash
# Windows PowerShell
cd D:\Users\TOMEK\CURRENT_AMBER_VERSION\WEBAPP
cd backend
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```bash
# Mac/Linux
cd backend
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**SKOPIUJ** wygenerowany klucz (np. `django-insecure-abc123...`)

### 1.2. Przygotuj zmienne środowiskowe

Będziesz potrzebować (wszystkie wartości są w `AWS_IDs_TRACKER.md`):
- **SECRET_KEY** - wygenerowany wyżej
- **DATABASE_URL** - `[AWS_IDs_TRACKER: DB Endpoint + Master Password]`
- **ALLOWED_HOSTS** - `[AWS_IDs_TRACKER: ALB DNS]`

**Format DATABASE_URL:**
```
postgresql://forumadmin:[AWS_IDs_TRACKER: Master Password]@[AWS_IDs_TRACKER: DB Endpoint]:5432/forumdb
```

**Twoja konkretna DATABASE_URL:**
```
postgresql://forumadmin:ForumDB2024!Secure@forum-db.caps6eywcswv.us-east-1.rds.amazonaws.com:5432/forumdb
```

### 1.3. Dodaj parametry do AWS

**W AWS Console:**

1. Wpisz w wyszukiwaniu: **Systems Manager**
2. Kliknij **Systems Manager**
3. W lewym menu kliknij: **Parameter Store**
4. Kliknij: **Create parameter**

#### Parametr 1: SECRET_KEY

- **Name:** `/forum/SECRET_KEY`
- **Description:** `Django secret key`
- **Tier:** Standard
- **Type:** SecureString
- **KMS key source:** My current account
- **KMS Key ID:** Zostaw domyślne
- **Value:** Wklej wygenerowany SECRET_KEY

Kliknij **Create parameter**

#### Parametr 2: DATABASE_URL

1. Kliknij: **Create parameter**
- **Name:** `/forum/DATABASE_URL`
- **Description:** `PostgreSQL connection string`
- **Type:** SecureString
- **Value:** `postgresql://forumadmin:[AWS_IDs_TRACKER: Master Password]@[AWS_IDs_TRACKER: DB Endpoint]:5432/forumdb`

**📋 Weź wartości z AWS_IDs_TRACKER.md sekcja "RDS POSTGRESQL"**

Kliknij **Create parameter**

#### Parametr 3: ALLOWED_HOSTS

1. Kliknij: **Create parameter**
- **Name:** `/forum/ALLOWED_HOSTS`
- **Description:** `Django allowed hosts`
- **Type:** String (nie SecureString)
- **Value:** `[AWS_IDs_TRACKER: ALB DNS],localhost,127.0.0.1`

**📋 Twój konkretny przykład:**
  ```
  forum-alb-1684129147.us-east-1.elb.amazonaws.com,localhost,127.0.0.1
  ```

Kliknij **Create parameter**

#### Parametr 4: FRONTEND_BUCKET

1. Kliknij: **Create parameter**
- **Name:** `/forum/FRONTEND_BUCKET`
- **Description:** `S3 bucket for React builds`
- **Type:** String
- **Value:** Twoja nazwa S3 bucket (np. `forum-frontend-builds-tomek-2024`)

Kliknij **Create parameter**

**✅ Checkpoint:** 4 parametry w Parameter Store

---

## 🐳 KROK 2: Build i Push Docker Image

### 2.1. Login do ECR

**Otwórz terminal w folderze projektu:**

```bash
# Windows PowerShell / Mac / Linux
cd D:\Users\TOMEK\CURRENT_AMBER_VERSION\WEBAPP

# Login do ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [AWS_IDs_TRACKER: ECR URI - BEZ '/forum-backend']
```

**📋 Weź ECR URI z AWS_IDs_TRACKER.md sekcja "ECR REPOSITORY"**
**UWAGA:** Usuń `/forum-backend` z końca URI!

**Twój konkretny przykład:**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 311603531332.dkr.ecr.us-east-1.amazonaws.com
```

Powinno pokazać: **Login Succeeded**

### 2.2. Build Docker Image

```bash
cd backend
docker build -t forum-backend .
```

⏳ To zajmie 3-5 minut. Zobaczysz wiele kroków.

**Sprawdź czy image został utworzony:**
```bash
docker images | grep forum-backend
```

### 2.3. Tag Image

```bash
docker tag forum-backend:latest [AWS_IDs_TRACKER: ECR URI]:latest
```

**📋 Użyj pełnego ECR URI z AWS_IDs_TRACKER.md (z `/forum-backend`)**

**Twój konkretny przykład:**
```bash
docker tag forum-backend:latest 311603531332.dkr.ecr.us-east-1.amazonaws.com/forum-backend:latest
```

### 2.4. Push do ECR

```bash
docker push [AWS_IDs_TRACKER: ECR URI]:latest
```

⏳ To zajmie 2-5 minut (w zależności od internetu).

**Sprawdź w AWS Console:**
1. Idź do **ECR** → **Repositories** → `forum-backend`
2. Powinien być 1 image z tagiem `latest`

**✅ Checkpoint:** Docker image w ECR

---

## ⚛️ KROK 3: Build i Upload React Frontend

### 3.1. Przygotuj środowisko React

**Utwórz plik `.env.production` w folderze `frontend/`:**

```bash
cd ../frontend
```

**📋 Użyj ALB DNS z AWS_IDs_TRACKER.md sekcja "LOAD BALANCER"**

**Windows PowerShell:**
```powershell
@"
REACT_APP_API_URL=http://[AWS_IDs_TRACKER: ALB DNS]
"@ | Out-File -FilePath .env.production -Encoding utf8
```

**Mac/Linux:**
```bash
cat > .env.production << EOF
REACT_APP_API_URL=http://[AWS_IDs_TRACKER: ALB DNS]
EOF
```

**Twoja konkretna zawartość `.env.production`:**
```
REACT_APP_API_URL=http://forum-alb-1684129147.us-east-1.elb.amazonaws.com
```

### 3.2. Install dependencies (jeśli jeszcze nie)

```bash
npm install
```

### 3.3. Build React

```bash
npm run build
```

⏳ To zajmie 1-2 minuty.

**Sprawdź:**
```bash
ls build/
```

Powinny być pliki: `index.html`, `static/`, itp.

### 3.4. Upload do S3

```bash
# Przejdź do głównego folderu projektu
cd ..

# Upload React build do S3
aws s3 sync frontend/build/ s3://[AWS_IDs_TRACKER: S3 Bucket - FRONTEND_BUCKET]/latest/ --delete
```

**📋 Użyj nazwy S3 bucket zapisanej w Parameter Store - sekcja "SECRETS (Parameter Store)" w AWS_IDs_TRACKER.md**

**Twój konkretny przykład:**
```bash
aws s3 sync frontend/build/ s3://forum-frontend-builds-kongoapp/latest/ --delete
```

**Sprawdź w AWS Console:**
1. Idź do **S3** → Twój bucket → `latest/`
2. Powinny być pliki: `index.html`, `static/`, itp.

**✅ Checkpoint:** React build w S3

---

## 🚀 KROK 4: Launch Template

**Co to jest Launch Template?** Szablon określający jak EC2 instancje mają być uruchamiane.

### 4.1. Utwórz Launch Template

1. Idź do **EC2** Console
2. W lewym menu kliknij: **Launch Templates**
3. Kliknij: **Create launch template**

**Launch template name and description:**
- **Launch template name:** `forum-lt`
- **Template version description:** `Initial version`
- **Auto Scaling guidance:** Zaznacz checkbox

**Application and OS Images (AMI):**
- Kliknij: **Quick Start**
- Wybierz: **Amazon Linux**
- **Amazon Linux 2023 AMI** (najnowsza wersja)

**Instance type:**
- Wybierz: **t2.micro** (Free tier)

**Key pair (login):**
- Jeśli masz key pair: wybierz go (sprawdź w `AWS_IDs_TRACKER.md` sekcja "AUTO SCALING")
- Jeśli nie masz:
  - Kliknij: **Create new key pair**
  - **Key pair name:** `forum-key`
  - **Key pair type:** RSA
  - **Private key format:** `.pem` (Mac/Linux) lub `.ppk` (Windows PuTTY)
  - Kliknij **Create key pair**
  - ⚠️ **ZAPISZ plik .pem/.ppk** bezpiecznie!
  - 📝 **Zapisz lokalizację w `AWS_IDs_TRACKER.md` sekcja "AUTO SCALING"**

**Network settings:**
- **Subnet:** Nie wybieraj (zostaw Auto Scaling zdecyduje)
- **Firewall (security groups):** Select existing
  - Wybierz: `forum-ec2-sg` **[AWS_IDs_TRACKER: EC2 Security Group]**

**Advanced network configuration:**
- **Auto-assign public IP:** Disable (będą w private subnets)

**Storage (volumes):**
- **Volume 1 (AMI Root):**
  - **Size:** `8` GiB
  - **Volume type:** gp3
  - **Delete on termination:** Yes

**Resource tags:**
Kliknij **Add tag**:
- **Key:** `Name`
- **Value:** `forum-ec2-instance`
- **Resource types:** Zaznacz **Instances** i **Volumes**

**Advanced details:**
- **IAM instance profile:** Wybierz `forum-ec2-role` **[AWS_IDs_TRACKER: Instance Profile Name]**
- **Metadata accessible:** Enabled
- **Metadata version:** V2 only (IMDSv2)
- **User data:** Wklej poniższy skrypt 

**⚠️ KRYTYCZNE: W User Data zamień `[AWS_IDs_TRACKER: ECR URI]` na Twój rzeczywisty ECR URI z AWS_IDs_TRACKER.md!**

```bash
#!/bin/bash
set -e

# Logging
exec > >(tee /var/log/user-data.log)
exec 2>&1

echo "===== Forum EC2 Setup Started ====="
echo "Timestamp: $(date)"

# Update system
echo "Updating system packages..."
yum update -y

# Install Docker
echo "Installing Docker..."
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install AWS CLI v2 (if not present)
if ! command -v aws &> /dev/null; then
    echo "Installing AWS CLI..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
    cd /tmp
    unzip awscliv2.zip
    ./aws/install
fi

# Install Nginx
echo "Installing Nginx..."
yum install -y nginx
systemctl enable nginx

# Get configuration from Parameter Store
echo "Fetching configuration from Parameter Store..."
REGION="us-east-1"
SECRET_KEY=$(aws ssm get-parameter --name "/forum/SECRET_KEY" --with-decryption --query "Parameter.Value" --output text --region $REGION)
DATABASE_URL=$(aws ssm get-parameter --name "/forum/DATABASE_URL" --with-decryption --query "Parameter.Value" --output text --region $REGION)
ALLOWED_HOSTS=$(aws ssm get-parameter --name "/forum/ALLOWED_HOSTS" --query "Parameter.Value" --output text --region $REGION)
FRONTEND_BUCKET=$(aws ssm get-parameter --name "/forum/FRONTEND_BUCKET" --query "Parameter.Value" --output text --region $REGION)

# ECR Repository URI (REPLACE THIS WITH YOUR VALUE FROM AWS_IDs_TRACKER.md)
ECR_URI="311603531332.dkr.ecr.us-east-1.amazonaws.com/forum-backend"  # Twój konkretny URI

# Login to ECR
echo "Logging into ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin ${ECR_URI%%/*}

# Pull Django Docker image
echo "Pulling Django Docker image..."
docker pull ${ECR_URI}:latest

# Run Django container
echo "Starting Django container..."
docker run -d \
  --name forum-backend \
  --restart always \
  -p 8000:8000 \
  -e SECRET_KEY="$SECRET_KEY" \
  -e DATABASE_URL="$DATABASE_URL" \
  -e ALLOWED_HOSTS="$ALLOWED_HOSTS" \
  -e DEBUG="False" \
  -e CORS_ALLOWED_ORIGINS="http://${ALLOWED_HOSTS}" \
  ${ECR_URI}:latest

# Wait for Django to start
echo "Waiting for Django to start..."
sleep 10

# Download React build from S3
echo "Downloading React frontend from S3..."
mkdir -p /var/www/frontend
aws s3 sync s3://${FRONTEND_BUCKET}/latest/ /var/www/frontend/

# Configure Nginx
echo "Configuring Nginx..."
cat > /etc/nginx/conf.d/forum.conf << 'EOF_NGINX'
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80 default_server;
    server_name _;
    
    root /var/www/frontend;
    index index.html;

    client_max_body_size 10M;
    client_body_buffer_size 128k;

    # Health check for ALB
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Django health check
    location /api/health/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 10s;
        proxy_read_timeout 30s;
    }

    # API requests → Django
    location /api/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Django admin
    location /admin {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django static files
    location /static/ {
        proxy_pass http://django;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Django media files
    location /media/ {
        proxy_pass http://django;
        expires 7d;
        add_header Cache-Control "public";
    }

    # React frontend
    location / {
        try_files $uri $uri/ /index.html;
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
    }

    # React static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }

    # Security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
EOF_NGINX

# Remove default Nginx config
rm -f /etc/nginx/nginx.conf.default
rm -f /etc/nginx/conf.d/default.conf

# Start Nginx
echo "Starting Nginx..."
systemctl restart nginx

echo "===== Setup Complete ====="
echo "Services status:"
echo "  - Docker: $(systemctl is-active docker)"
echo "  - Nginx: $(systemctl is-active nginx)"
echo "  - Django container: $(docker ps --filter name=forum-backend --format '{{.Status}}')"
echo ""
echo "Logs:"
echo "  - This script: /var/log/user-data.log"
echo "  - Nginx: /var/log/nginx/error.log"
echo "  - Django: docker logs forum-backend"
echo ""
echo "Deployment timestamp: $(date)"
```

**⚠️ WAŻNE:** W User Data, zamień `[TWOJE-ECR-URI]` na Twój ECR URI!

4. Kliknij **Create launch template**
5. **ZAPISZ Launch Template ID**

**✅ Checkpoint:** Launch Template utworzony

---

## 📊 KROK 5: Auto Scaling Group

**Co to jest ASG?** Automatycznie uruchamia/zatrzymuje EC2 w zależności od ruchu.

### 5.1. Utwórz Auto Scaling Group

1. W lewym menu EC2 kliknij: **Auto Scaling Groups**
2. Kliknij: **Create Auto Scaling group**

**Step 1: Choose launch template**
- **Auto Scaling group name:** `forum-asg`
- **Launch template:** Wybierz `forum-lt`
- **Version:** Latest

Kliknij **Next**

**Step 2: Choose instance launch options**
- **VPC:** Wybierz `forum-vpc` **[AWS_IDs_TRACKER: VPC ID]**
- **Availability Zones and subnets:** Wybierz:
  - `forum-private-subnet-1a` **[AWS_IDs_TRACKER: Private Subnet 1 (1a)]**
  - `forum-private-subnet-1b` **[AWS_IDs_TRACKER: Private Subnet 2 (1b)]**

Kliknij **Next**

**Step 3: Configure advanced options**
- **Load balancing:** Attach to an existing load balancer
- **Choose from your load balancer target groups:** Wybierz `forum-tg` **[AWS_IDs_TRACKER: Target Group Name]**
- **Health checks:**
  - **Health check type:** ELB
  - **Health check grace period:** `300` seconds
  - **Enable group metrics collection:** Zaznacz

Kliknij **Next**

**Step 4: Configure group size and scaling**
- **Desired capacity:** `2`
- **Min desired capacity:** `1`
- **Max desired capacity:** `4`

**Scaling policies:**
- Wybierz: **Target tracking scaling policy**
- **Scaling policy name:** `forum-cpu-policy`
- **Metric type:** Average CPU utilization
- **Target value:** `70`

Kliknij **Next**

**Step 5: Add notifications**
- Pomiń (możesz dodać później SNS dla alertów)

Kliknij **Next**

**Step 6: Add tags**
- Kliknij **Add tag**
  - **Key:** `Name`
  - **Value:** `forum-ec2-asg`

Kliknij **Next**

**Step 7: Review**
- Sprawdź wszystko
- Kliknij **Create Auto Scaling group**

⏳ Poczekaj 5-7 minut. ASG uruchomi 2 instancje EC2.

**Sprawdź status:**
1. Idź do **EC2** → **Instances**
2. Powinny być 2 instancje z tagiem `forum-ec2-asg`
3. Status powinien zmienić się na **Running** po ~3 minutach

**✅ Checkpoint:** ASG uruchomiony z 2 instancjami

---

## 🧪 KROK 6: Test Połączenia z Bazą Danych

### 6.1. Connect do EC2 przez Session Manager

1. W **EC2** → **Instances**
2. Zaznacz jedną z instancji
3. Kliknij: **Connect**
4. Wybierz zakładkę: **Session Manager**
5. Kliknij: **Connect**

Otworzy się terminal w przeglądarce.

### 6.2. Sprawdź status

```bash
# Przejdź na ec2-user
sudo su - ec2-user

# Sprawdź status Docker
docker ps

# Sprawdź logi Django
docker logs forum-backend

# Sprawdź status Nginx
sudo systemctl status nginx
```

### 6.3. Test połączenia z RDS

```bash
# W kontenerze Django, sprawdź połączenie z bazą
docker exec -it forum-backend python manage.py check --database default
```

Jeśli wszystko OK, zobaczysz: `System check identified no issues`

**✅ Checkpoint:** EC2 łączy się z RDS

---

## 🗄️ KROK 7: Migracja Bazy Danych

**TYLKO PIERWSZY RAZ!** Uruchom migracje Django.

### 7.1. Uruchom migracje

```bash
# W Session Manager na EC2:
docker exec -it forum-backend python manage.py migrate
```

Zobaczysz listę migracji:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying users.0001_initial... OK
  Applying forum.0001_initial... OK
  ...
```

### 7.2. Utwórz superusera

```bash
docker exec -it forum-backend python manage.py createsuperuser
```

Podaj:
- **Email:** Twój email
- **Password:** Silne hasło
- **Password (again):** Powtórz

### 7.3. Załaduj dane testowe (opcjonalnie)

```bash
docker exec -it forum-backend python manage.py seed_data
```

**✅ Checkpoint:** Baza danych zmigrowana

---

## 🌐 KROK 8: Test ALB

### 8.1. Sprawdź ALB DNS

**📋 Twój ALB DNS (zapisany w AWS_IDs_TRACKER.md):**
```
forum-alb-1684129147.us-east-1.elb.amazonaws.com
```

1. Idź do **EC2** → **Load Balancers**
2. Kliknij na `forum-alb`
3. Skopiuj **DNS name** i sprawdź czy się zgadza z powyższym

### 8.2. Test w przeglądarce

**Otwórz przeglądarkę i wejdź na Twój ALB:**
```
http://forum-alb-1684129147.us-east-1.elb.amazonaws.com
```

Powinieneś zobaczyć **stronę React (Frontend)**!

**Test health check:**
```
http://forum-alb-1684129147.us-east-1.elb.amazonaws.com/health
```

Powinno pokazać: `healthy`

**Test API:**
```
http://forum-alb-1684129147.us-east-1.elb.amazonaws.com/api/categories/
```

Powinno pokazać JSON z kategoriami.

**Jeśli nie działa:**
- Sprawdź logi: `docker logs forum-backend`
- Sprawdź Target Group Health w AWS Console
- Poczekaj 2-3 minuty (health checks)

**✅ Checkpoint:** Aplikacja działa przez ALB!

---

## ☁️ KROK 9: Cloudflare Setup

**Cloudflare da nam:**
- Darmowy SSL/TLS
- CDN (szybsze ładowanie)
- WAF (firewall)
- DDoS protection

### 9.1. Dodaj domenę do Cloudflare

**📋 Zapisz domenę i dane Cloudflare w AWS_IDs_TRACKER.md sekcja "CLOUDFLARE"**

1. Idź na: https://dash.cloudflare.com/
2. Zaloguj się
3. Kliknij: **Add a Site**
4. Wpisz swoją domenę (np. `mojeforum.tk`)
5. Wybierz: **Free Plan**
6. Kliknij: **Continue**

### 9.2. Zmień nameservery

Cloudflare pokaże 2 nameservery (np. `alice.ns.cloudflare.com`, `bob.ns.cloudflare.com`)

1. Idź do swojego dostawcy domeny (np. Freenom, Namecheap)
2. Zmień nameservery na te z Cloudflare
3. Wróć do Cloudflare
4. Kliknij: **Done, check nameservers**

⏳ To może zająć 5-30 minut.

### 9.3. Dodaj DNS Record

**📋 Użyj ALB DNS z AWS_IDs_TRACKER.md sekcja "LOAD BALANCER"**

1. W Cloudflare, idź do zakładki: **DNS** → **Records**
2. Kliknij: **Add record**

**Record 1: Root domain**
- **Type:** CNAME
- **Name:** `@` (oznacza root domain)
- **Target:** `forum-alb-1684129147.us-east-1.elb.amazonaws.com` (Twój ALB DNS)
- **Proxy status:** Proxied (pomarańczowa chmurka) ⚠️ WAŻNE!
- **TTL:** Auto

Kliknij **Save**

**Record 2: WWW subdomain**
- **Type:** CNAME
- **Name:** `www`
- **Target:** `forum-alb-1684129147.us-east-1.elb.amazonaws.com` (Twój ALB DNS)
- **Proxy status:** Proxied
- **TTL:** Auto

Kliknij **Save**

**💾 Zapisz te rekordy w AWS_IDs_TRACKER.md sekcja "CLOUDFLARE"**

### 9.4. Konfiguracja SSL/TLS

1. Zakładka: **SSL/TLS**
2. Wybierz: **Full** (nie Strict, bo ALB ma HTTP)

### 9.5. Konfiguracja WAF (Firewall)

1. Zakładka: **Security** → **WAF**
2. Włącz: **Managed rules** (powinno być domyślnie włączone)

### 9.6. Konfiguracja Cache

1. Zakładka: **Caching** → **Configuration**
2. **Caching Level:** Standard

### 9.7. Test domeny

**Poczekaj 5-10 minut, potem wejdź na:**
```
https://[AWS_IDs_TRACKER: Domain]
```
**Użyj domeny z AWS_IDs_TRACKER.md sekcja "CLOUDFLARE"**

Powinieneś zobaczyć:
- ✅ Stronę Forum (React)
- ✅ Kłódkę SSL w przeglądarce

**✅ Checkpoint:** Domena działa przez Cloudflare!

---

## 🔄 KROK 10: Update ALLOWED_HOSTS

Teraz dodaj swoją domenę do ALLOWED_HOSTS.

### 10.1. Update Parameter Store

1. Idź do **Systems Manager** → **Parameter Store**
2. Kliknij na `/forum/ALLOWED_HOSTS`
3. Kliknij: **Edit**
4. **Value:** Dodaj swoją domenę:
   ```
   [TWOJA-DOMENA],www.[TWOJA-DOMENA],forum-alb-1684129147.us-east-1.elb.amazonaws.com,localhost,127.0.0.1
   ```
   
   **Twój konkretny przykład (zamień TWOJA-DOMENA na swoją):**
   ```
   mojeforum.tk,www.mojeforum.tk,forum-alb-1684129147.us-east-1.elb.amazonaws.com,localhost,127.0.0.1
   ```
5. Kliknij **Save changes**

### 10.2. Restart EC2 Instances

1. Idź do **EC2** → **Auto Scaling Groups** → `forum-asg`
2. Kliknij zakładkę: **Instance management**
3. Zaznacz obie instancje
4. **Actions** → **Instance refresh**
5. **Start instance refresh**

⏳ Poczekaj 5-7 minut. ASG uruchomi nowe instancje z zaktualizowaną konfiguracją.

**✅ Checkpoint:** Aplikacja działa z domeną!

---

## 🎉 DAY 2 ZAKOŃCZONY!

### ✅ Checklist - Co masz działające:

- [ ] Parameter Store ze sekretami (4 parametry)
- [ ] Docker image w ECR
- [ ] React build w S3
- [ ] Launch Template skonfigurowany
- [ ] Auto Scaling Group z 2 instancjami
- [ ] Baza danych zmigrowana
- [ ] ALB przekazuje ruch do EC2
- [ ] Cloudflare:
  - [ ] DNS skonfigurowane
  - [ ] SSL/TLS włączone
  - [ ] WAF aktywny
- [ ] Aplikacja działa na domenie przez HTTPS

---

## 🧪 Final Testing

**📋 Użyj domeny z AWS_IDs_TRACKER.md sekcja "FINAL URLs"**

### Test 1: Frontend
Wejdź na: `https://[AWS_IDs_TRACKER: Domain]`
- [ ] Widać stronę główną
- [ ] Widać kategorie

### Test 2: Rejestracja
- [ ] Kliknij "Register"
- [ ] Zarejestruj konto
- [ ] Zaloguj się

### Test 3: Thread
- [ ] Utwórz nowy wątek
- [ ] Dodaj odpowiedź
- [ ] Sprawdź profil

### Test 4: Admin Panel
Wejdź na: `https://[AWS_IDs_TRACKER: Domain]/admin`
- [ ] Zaloguj się (superuser z KROK 7 - zapisz w AWS_IDs_TRACKER.md sekcja "CREDENTIALS FOR DEMO")
- [ ] Sprawdź użytkowników, kategorie

**Wszystko działa? GRATULACJE! 🎊**

---

## 🚀 KROK 11 (Opcjonalnie): GitHub Actions CI/CD

### 11.1. Setup GitHub Secrets

**📋 Użyj wartości z AWS_IDs_TRACKER.md**

1. Idź na GitHub: https://github.com/tomisworking/webapp
2. **Settings** → **Secrets and variables** → **Actions**
3. Kliknij: **New repository secret**

**Dodaj secrets:**

| Name | Value | Gdzie znaleźć w AWS_IDs_TRACKER.md |
|------|-------|-----------------------------------|
| `AWS_ACCESS_KEY_ID` | `[AWS_IDs_TRACKER: Access Key ID]` | Sekcja "AWS CREDENTIALS" |
| `AWS_SECRET_ACCESS_KEY` | `[AWS_IDs_TRACKER: Secret Access Key]` | Sekcja "AWS CREDENTIALS" |
| `AWS_REGION` | `us-east-1` | Sekcja "AWS CREDENTIALS" |
| `ECR_REPOSITORY` | `forum-backend` | Sekcja "ECR REPOSITORY" |
| `S3_BUCKET` | `[AWS_IDs_TRACKER: S3 Bucket]` | Sekcja "SECRETS (Parameter Store)" |
| `ASG_NAME` | `forum-asg` | Sekcja "AUTO SCALING" |

### 11.2. Utwórz GitHub Actions Workflow

**Utwórz plik: `.github/workflows/deploy.yml`**

```yaml
name: Deploy to AWS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ secrets.AWS_REGION }}
    
    - name: Login to ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build and push Docker image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: ${{ secrets.ECR_REPOSITORY }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        cd backend
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
    
    - name: Build React frontend
      run: |
        cd frontend
        npm ci
        npm run build
    
    - name: Upload to S3
      run: |
        aws s3 sync frontend/build/ s3://${{ secrets.S3_BUCKET }}/latest/ --delete
    
    - name: Refresh Auto Scaling Group
      run: |
        aws autoscaling start-instance-refresh \
          --auto-scaling-group-name ${{ secrets.ASG_NAME }} \
          --preferences MinHealthyPercentage=50
```

**Commit i push:**
```bash
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions deployment workflow"
git push origin main
```

Teraz każdy push na `main` będzie automatycznie deployował na AWS! 🚀

**✅ Checkpoint:** CI/CD skonfigurowane

---

## 📊 Monitoring

### CloudWatch Logs

1. Idź do **CloudWatch** → **Log groups**
2. Możesz dodać CloudWatch agent do EC2 dla szczegółowych logów

### ALB Monitoring

1. **EC2** → **Load Balancers** → `forum-alb`
2. Zakładka: **Monitoring**
3. Zobacz metryki: Request count, Target response time, HTTP 5XX errors

### ASG Monitoring

1. **EC2** → **Auto Scaling Groups** → `forum-asg`
2. Zakładka: **Monitoring**
3. Zobacz metryki: CPU, Network In/Out

---

## 🆘 Troubleshooting DAY 2

### "EC2 nie startują"
- Sprawdź User Data w Launch Template
- Sprawdź logi: `/var/log/user-data.log` w Session Manager
- Sprawdź czy IAM Role ma odpowiednie permissions

### "Django container nie działa"
- SSH/Session Manager: `docker logs forum-backend`
- Sprawdź DATABASE_URL w Parameter Store
- Sprawdź Security Group (EC2 → RDS)

### "ALB pokazuje 503"
- Sprawdź Target Group Health
- Health check path musi być `/health`
- Poczekaj 2-3 minuty na health checks

### "React nie ładuje się"
- Sprawdź czy pliki są w S3: `aws s3 ls s3://[AWS_IDs_TRACKER: S3 Bucket]/latest/`
- Sprawdź `/var/www/frontend/` na EC2
- Sprawdź Nginx config: `sudo nginx -t`

### "Cloudflare nie działa"
- Sprawdź czy nameservery się zmieniły (24h max)
- Sprawdź czy Proxy jest włączone (pomarańczowa chmurka)
- Sprawdź SSL/TLS mode: Full (nie Strict)

### "Database connection refused"
- Sprawdź Security Group RDS (port 5432 z EC2 SG)
- Sprawdź czy RDS jest w tych samych subnets co DB Subnet Group
- Ping RDS endpoint z EC2: `telnet [AWS_IDs_TRACKER: DB Endpoint] 5432`

---

## 💰 Oszczędzanie Kosztów

### Wyłącz na noc (jeśli testowe):
```bash
# Stop Auto Scaling Group
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name forum-asg \
  --min-size 0 \
  --max-size 0 \
  --desired-capacity 0

# Rano włącz:
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name forum-asg \
  --min-size 1 \
  --max-size 4 \
  --desired-capacity 2
```

### Wyłącz RDS na noc:
```bash
# Stop RDS
aws rds stop-db-instance --db-instance-identifier forum-db

# Start RDS
aws rds start-db-instance --db-instance-identifier forum-db
```

---

## 📝 OSTATNI KROK: Zapisz Wszystko!

### ⚠️ KRYTYCZNE: Wypełnij AWS_IDs_TRACKER.md

Przed zakończeniem, upewnij się że zapisałeś WSZYSTKIE wartości w `AWS_IDs_TRACKER.md`:

**✅ Checklist - Co powinno być zapisane:**
- [ ] AWS Account ID i Region
- [ ] VPC ID, Subnet IDs
- [ ] Security Group IDs (ALB, EC2, RDS)
- [ ] RDS Endpoint i Master Password
- [ ] ECR URI
- [ ] ALB DNS Name
- [ ] Launch Template ID
- [ ] EC2 Instance IDs i Private IPs
- [ ] IAM Role ARNs
- [ ] Django SECRET_KEY (backup)
- [ ] Cloudflare Domain i Nameservers
- [ ] Django Admin credentials
- [ ] Final URLs (Backend API, Admin Panel, Frontend)

**Dlaczego to ważne?**
- 🔐 Bezpieczeństwo: Hasła i klucze w jednym miejscu
- 🚀 Deployment: Wszystkie ID potrzebne do CI/CD
- 🆘 Troubleshooting: Szybki dostęp do endpointów
- 👥 Zespół: Inni mogą przejąć deployment
- 📊 Prezentacja: Wszystko gotowe do pokazania

**🎯 Akcja:** Otwórz `AWS_IDs_TRACKER.md` i wypełnij wszystkie puste pola!

---

## 🎊 GRATULACJE!

**Twoja aplikacja jest live na AWS z:**
- ✅ Auto Scaling
- ✅ Load Balancing
- ✅ Managed Database
- ✅ SSL/TLS
- ✅ CDN
- ✅ WAF
- ✅ DDoS Protection

**Następne kroki:**
- Monitoring i alerting
- Backup strategy
- Cost optimization
- Performance tuning

**Powodzenia! 🚀**

---

## 📚 QUICK REFERENCE: AWS_IDs_TRACKER.md Mapping

Szybka ściągawka gdzie szukać wartości w `AWS_IDs_TRACKER.md`:

| Potrzebujesz | Sekcja w AWS_IDs_TRACKER.md | Pole |
|--------------|----------------------------|------|
| ECR URI | 📦 ECR REPOSITORY | ECR URI |
| ALB DNS | ⚖️ LOAD BALANCER | ALB DNS |
| RDS Endpoint | 🗄️ RDS POSTGRESQL | DB Endpoint |
| RDS Password | 🗄️ RDS POSTGRESQL | Master Password |
| VPC ID | 🌐 VPC & NETWORKING | VPC ID |
| Private Subnets | 🌐 VPC & NETWORKING | PRIVATE SUBNETS |
| EC2 Security Group | 🔒 SECURITY GROUPS | EC2 Security Group |
| Target Group | ⚖️ LOAD BALANCER | Target Group Name |
| IAM Role | 🔐 IAM ROLES | Instance Profile Name |
| S3 Bucket | 🔑 SECRETS (Parameter Store) | /forum/FRONTEND_BUCKET |
| Domain | 🌍 CLOUDFLARE | Domain |
| AWS Credentials | 🔐 AWS CREDENTIALS | Access Key ID, Secret |

**💡 Pro Tip:** Ctrl+F (lub Cmd+F) w `AWS_IDs_TRACKER.md` żeby szybko znaleźć potrzebną wartość!

---

**KONIEC DAY 2 DEPLOYMENT GUIDE**


