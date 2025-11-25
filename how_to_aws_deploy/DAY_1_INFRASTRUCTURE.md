# 📅 DAY 1: Setup Infrastruktury AWS

**Czas:** 3-4 godziny  
**Cel:** Utworzenie całej infrastruktury AWS (VPC, RDS, ALB, Security Groups)

⚠️ **WAŻNE:** Otwórz plik `AWS_IDs_TRACKER.md` i zapisuj tam WSZYSTKIE ID zasobów, które utworzysz!

---

## 🎯 Co zrobimy dzisiaj?

1. ✅ Utworzenie VPC (Virtual Private Cloud)
2. ✅ Utworzenie Subnets (publiczne i prywatne)
3. ✅ Konfiguracja Internet Gateway
4. ✅ Utworzenie NAT Gateway
5. ✅ Konfiguracja Route Tables
6. ✅ Utworzenie Security Groups
7. ✅ Utworzenie bazy danych RDS PostgreSQL
8. ✅ Utworzenie Application Load Balancer
9. ✅ Utworzenie Target Group
10. ✅ Utworzenie ECR Repository
11. ✅ Utworzenie S3 Bucket
12. ✅ Utworzenie IAM Role dla EC2

---

## 📋 Przed Rozpoczęciem

1. **Zaloguj się do AWS Console:**
   - Idź na: https://aws.amazon.com/free
   - Zaloguj się swoim kontem

2. **Wybierz region:**
   - W prawym górnym rogu (obok nazwy użytkownika)
   - Kliknij na region
   - Wybierz: **Europe (Frankfurt) eu-central-1**
   - ⚠️ **WSZYSTKO** rób w tym samym regionie!

3. **Otwórz notatnik:**
   - Otwórz plik `AWS_IDs_TRACKER.md`
   - Będziesz tam zapisywać wszystkie ID

---

## 🌐 KROK 1: Utworzenie VPC (Virtual Private Cloud)

**Co to jest VPC?** To Twoja prywatna sieć w AWS, odizolowana od innych.

### 1.1. Wejdź do VPC Dashboard

1. W AWS Console, w górnym pasku wyszukaj: **VPC**
2. Kliknij **VPC** (pierwszy wynik)
3. Upewnij się, że region to **eu-central-1**

### 1.2. Utwórz VPC

1. W lewym menu kliknij: **Your VPCs**
2. Kliknij pomarańczowy przycisk: **Create VPC**

### 1.3. Wypełnij formularz

**VPC settings:**
- **Resources to create:** Wybierz **VPC only**
- **Name tag:** `forum-vpc`
- **IPv4 CIDR block:** `10.0.0.0/16`
- **IPv6 CIDR block:** Zostaw **No IPv6 CIDR block**
- **Tenancy:** Wybierz **Default**

### 1.4. Utwórz

1. Kliknij **Create VPC** (na dole)
2. Poczekaj 5 sekund
3. Zobaczysz komunikat: "Successfully created VPC"
4. **ZAPISZ VPC ID** do `AWS_IDs_TRACKER.md` (np. `vpc-0abc123def456`)

**✅ Checkpoint:** Masz VPC z ID zapisanym w notatniku

---

## 🗂️ KROK 2: Utworzenie Subnets

**Co to są Subnets?** To podsieci w Twojej VPC. Będziemy mieli:
- **2 Public Subnets** (dla ALB) w różnych Availability Zones
- **2 Private Subnets** (dla EC2) w różnych Availability Zones
- **2 Database Subnets** (dla RDS) w różnych Availability Zones

### 2.1. Wejdź do Subnets

1. W lewym menu VPC Dashboard kliknij: **Subnets**
2. Kliknij: **Create subnet**

### 2.2. Utwórz Public Subnet 1

**VPC:**
- **VPC ID:** Wybierz `forum-vpc` (to co przed chwilą utworzyłeś)

**Subnet settings:**
- **Subnet name:** `forum-public-subnet-1a`
- **Availability Zone:** Wybierz **eu-central-1a**
- **IPv4 CIDR block:** `10.0.1.0/24`

Kliknij **Add new subnet** (na dole)

### 2.3. Utwórz Public Subnet 2

**Subnet settings:**
- **Subnet name:** `forum-public-subnet-1b`
- **Availability Zone:** Wybierz **eu-central-1b**
- **IPv4 CIDR block:** `10.0.2.0/24`

Kliknij **Add new subnet**

### 2.4. Utwórz Private Subnet 1

**Subnet settings:**
- **Subnet name:** `forum-private-subnet-1a`
- **Availability Zone:** Wybierz **eu-central-1a**
- **IPv4 CIDR block:** `10.0.10.0/24`

Kliknij **Add new subnet**

### 2.5. Utwórz Private Subnet 2

**Subnet settings:**
- **Subnet name:** `forum-private-subnet-1b`
- **Availability Zone:** Wybierz **eu-central-1b**
- **IPv4 CIDR block:** `10.0.11.0/24`

Kliknij **Add new subnet**

### 2.6. Utwórz Database Subnet 1

**Subnet settings:**
- **Subnet name:** `forum-db-subnet-1a`
- **Availability Zone:** Wybierz **eu-central-1a**
- **IPv4 CIDR block:** `10.0.20.0/24`

Kliknij **Add new subnet**

### 2.7. Utwórz Database Subnet 2

**Subnet settings:**
- **Subnet name:** `forum-db-subnet-1b`
- **Availability Zone:** Wybierz **eu-central-1b**
- **IPv4 CIDR block:** `10.0.21.0/24`

### 2.8. Finalizuj

1. Kliknij **Create subnet** (na dole)
2. Poczekaj 10 sekund
3. Zobaczysz komunikat: "Successfully created 6 subnets"
4. **ZAPISZ WSZYSTKIE SUBNET IDs** do `AWS_IDs_TRACKER.md`

**✅ Checkpoint:** Masz 6 subnets utworzonych i zapisanych

---

## 🌍 KROK 3: Internet Gateway

**Co to jest IGW?** To brama pozwalająca VPC komunikować się z Internetem.

### 3.1. Utwórz Internet Gateway

1. W lewym menu kliknij: **Internet gateways**
2. Kliknij: **Create internet gateway**
3. **Name tag:** `forum-igw`
4. Kliknij **Create internet gateway**
5. **ZAPISZ IGW ID** do notatnika

### 3.2. Podłącz do VPC

1. Zobaczysz komunikat: "Attach to VPC to enable resource connectivity"
2. Kliknij przycisk: **Attach to a VPC**
3. **Available VPCs:** Wybierz `forum-vpc`
4. Kliknij **Attach internet gateway**

**✅ Checkpoint:** Internet Gateway podłączony do VPC

---

## 🔀 KROK 4: NAT Gateway

**Co to jest NAT Gateway?** Pozwala zasobom w private subnets łączyć się z Internetem (np. do update), ale nie pozwala na połączenia z zewnątrz do nich.

### 4.1. Alokuj Elastic IP

NAT Gateway potrzebuje publicznego IP.

1. W lewym menu kliknij: **Elastic IPs**
2. Kliknij: **Allocate Elastic IP address**
3. **Network Border Group:** Zostaw domyślne
4. **Tags:** (opcjonalne) Name = `forum-nat-eip`
5. Kliknij **Allocate**
6. **ZAPISZ Elastic IP** (np. `3.123.45.67`) do notatnika

### 4.2. Utwórz NAT Gateway

1. W lewym menu kliknij: **NAT gateways**
2. Kliknij: **Create NAT gateway**

**Settings:**
- **Name:** `forum-nat-gateway`
- **Subnet:** Wybierz `forum-public-subnet-1a` ⚠️ MUSI być public!
- **Connectivity type:** Wybierz **Public**
- **Elastic IP allocation ID:** Wybierz Elastic IP z poprzedniego kroku

3. Kliknij **Create NAT gateway**
4. **ZAPISZ NAT Gateway ID** do notatnika
5. ⏳ Poczekaj 2-3 minuty aż status zmieni się na **Available**

**✅ Checkpoint:** NAT Gateway dostępny w public subnet

---

## 🛤️ KROK 5: Route Tables

**Co to są Route Tables?** Określają jak ruch sieciowy jest kierowany w VPC.

### 5.1. Utwórz Public Route Table

1. W lewym menu kliknij: **Route tables**
2. Kliknij: **Create route table**

**Settings:**
- **Name:** `forum-public-rtb`
- **VPC:** Wybierz `forum-vpc`

3. Kliknij **Create route table**
4. **ZAPISZ Route Table ID** do notatnika

### 5.2. Dodaj route do Internetu

1. Kliknij na `forum-public-rtb` (link w tabeli)
2. Na dole, kliknij zakładkę: **Routes**
3. Kliknij **Edit routes**
4. Kliknij **Add route**

**New route:**
- **Destination:** `0.0.0.0/0`
- **Target:** Wybierz **Internet Gateway**, potem wybierz `forum-igw`

5. Kliknij **Save changes**

### 5.3. Przypisz Public Subnets

1. Kliknij zakładkę: **Subnet associations**
2. Kliknij **Edit subnet associations**
3. Zaznacz checkboxy przy:
   - `forum-public-subnet-1a`
   - `forum-public-subnet-1b`
4. Kliknij **Save associations**

### 5.4. Utwórz Private Route Table

1. Wróć do **Route tables**
2. Kliknij: **Create route table**

**Settings:**
- **Name:** `forum-private-rtb`
- **VPC:** Wybierz `forum-vpc`

3. Kliknij **Create route table**
4. **ZAPISZ Route Table ID**

### 5.5. Dodaj route do NAT Gateway

1. Kliknij na `forum-private-rtb`
2. Zakładka **Routes** → **Edit routes**
3. **Add route**

**New route:**
- **Destination:** `0.0.0.0/0`
- **Target:** Wybierz **NAT Gateway**, potem wybierz `forum-nat-gateway`

4. Kliknij **Save changes**

### 5.6. Przypisz Private Subnets

1. Zakładka **Subnet associations** → **Edit subnet associations**
2. Zaznacz:
   - `forum-private-subnet-1a`
   - `forum-private-subnet-1b`
   - `forum-db-subnet-1a`
   - `forum-db-subnet-1b`
3. Kliknij **Save associations**

**✅ Checkpoint:** Route tables skonfigurowane dla public i private subnets

---

## 🔒 KROK 6: Security Groups

**Co to są Security Groups?** To firewalle kontrolujące ruch sieciowy do/z zasobów.

### 6.1. Security Group dla ALB

1. W lewym menu kliknij: **Security groups**
2. Kliknij: **Create security group**

**Basic details:**
- **Security group name:** `forum-alb-sg`
- **Description:** `Security group for Application Load Balancer`
- **VPC:** Wybierz `forum-vpc`

**Inbound rules:**
1. Kliknij **Add rule**
   - **Type:** HTTP
   - **Protocol:** TCP
   - **Port range:** 80
   - **Source:** Anywhere-IPv4 (`0.0.0.0/0`)
   - **Description:** `Allow HTTP from anywhere`

2. Kliknij **Add rule**
   - **Type:** HTTPS
   - **Protocol:** TCP
   - **Port range:** 443
   - **Source:** Anywhere-IPv4 (`0.0.0.0/0`)
   - **Description:** `Allow HTTPS from anywhere`

**Outbound rules:**
- Zostaw domyślne (All traffic, 0.0.0.0/0)

3. Kliknij **Create security group**
4. **ZAPISZ Security Group ID** (dla ALB)

### 6.2. Security Group dla EC2

1. Kliknij: **Create security group**

**Basic details:**
- **Security group name:** `forum-ec2-sg`
- **Description:** `Security group for EC2 instances`
- **VPC:** Wybierz `forum-vpc`

**Inbound rules:**
1. Kliknij **Add rule**
   - **Type:** HTTP
   - **Protocol:** TCP
   - **Port range:** 80
   - **Source:** Custom, wybierz `forum-alb-sg` (Security Group ALB)
   - **Description:** `Allow HTTP from ALB only`

2. Kliknij **Add rule**
   - **Type:** SSH
   - **Protocol:** TCP
   - **Port range:** 22
   - **Source:** My IP (Cursor to automatycznie wypełni Twoim IP)
   - **Description:** `SSH access for management`

**Outbound rules:**
- Zostaw domyślne (All traffic, 0.0.0.0/0)

3. Kliknij **Create security group**
4. **ZAPISZ Security Group ID** (dla EC2)

### 6.3. Security Group dla RDS

1. Kliknij: **Create security group**

**Basic details:**
- **Security group name:** `forum-rds-sg`
- **Description:** `Security group for RDS PostgreSQL`
- **VPC:** Wybierz `forum-vpc`

**Inbound rules:**
1. Kliknij **Add rule**
   - **Type:** PostgreSQL
   - **Protocol:** TCP
   - **Port range:** 5432
   - **Source:** Custom, wybierz `forum-ec2-sg` (Security Group EC2)
   - **Description:** `Allow PostgreSQL from EC2 only`

**Outbound rules:**
- Zostaw domyślne

2. Kliknij **Create security group**
3. **ZAPISZ Security Group ID** (dla RDS)

**✅ Checkpoint:** Masz 3 Security Groups (ALB, EC2, RDS)

---

## 💾 KROK 7: RDS PostgreSQL Database

**Co to jest RDS?** Managed service dla baz danych. AWS zarządza backupami, updatami, itp.

### 7.1. Utwórz DB Subnet Group

1. W wyszukiwaniu AWS Console wpisz: **RDS**
2. Kliknij **RDS**
3. W lewym menu kliknij: **Subnet groups**
4. Kliknij: **Create DB subnet group**

**Settings:**
- **Name:** `forum-db-subnet-group`
- **Description:** `Subnet group for Forum RDS`
- **VPC:** Wybierz `forum-vpc`

**Add subnets:**
- **Availability Zones:** Wybierz `eu-central-1a` i `eu-central-1b`
- **Subnets:** Wybierz:
  - `10.0.20.0/24` (forum-db-subnet-1a)
  - `10.0.21.0/24` (forum-db-subnet-1b)

5. Kliknij **Create**

### 7.2. Utwórz RDS Instance

1. W lewym menu kliknij: **Databases**
2. Kliknij: **Create database**

**Engine options:**
- **Engine type:** PostgreSQL
- **Engine Version:** Zostaw najnowszą (np. PostgreSQL 15.x)

**Templates:**
- Wybierz: **Free tier** ⚠️ WAŻNE!

**Settings:**
- **DB instance identifier:** `forum-db`
- **Master username:** `forumadmin`
- **Master password:** Wpisz silne hasło (np. `ForumDB2024!Secure`)
- **Confirm password:** Powtórz hasło
- **⚠️ ZAPISZ HASŁO** do `AWS_IDs_TRACKER.md` i bezpiecznego miejsca!

**DB instance class:**
- Zostaw: **db.t3.micro** (Free tier)

**Storage:**
- **Storage type:** General Purpose SSD (gp3)
- **Allocated storage:** `20` GiB
- **Storage autoscaling:** Wyłącz (odznacz checkbox)

**Connectivity:**
- **Compute resource:** Don't connect to an EC2 compute resource
- **Virtual private cloud (VPC):** Wybierz `forum-vpc`
- **DB subnet group:** Wybierz `forum-db-subnet-group`
- **Public access:** **No** ⚠️ WAŻNE! Baza NIE może być publiczna
- **VPC security group:** Choose existing
  - Usuń `default`, dodaj `forum-rds-sg`
- **Availability Zone:** No preference

**Database authentication:**
- Zostaw: **Password authentication**

**Additional configuration** (rozwiń):
- **Initial database name:** `forumdb`
- **Backup retention period:** `7` days
- **Enable encryption:** Zostaw zaznaczone

**Monitoring:**
- Zostaw domyślne

3. **Przewiń na dół i sprawdź szacunkowe koszty:** Powinno pokazać $0 (Free tier)
4. Kliknij **Create database**
5. ⏳ Poczekaj 5-10 minut aż status zmieni się na **Available**
6. **ZAPISZ RDS Endpoint** (np. `forum-db.abc123.eu-central-1.rds.amazonaws.com`)

**✅ Checkpoint:** RDS PostgreSQL dostępna w private subnets

---

## ⚖️ KROK 8: Application Load Balancer

**Co to jest ALB?** Rozdziela ruch między wiele instancji EC2.

### 8.1. Utwórz Target Group

1. W wyszukiwaniu AWS Console wpisz: **EC2**
2. Kliknij **EC2**
3. W lewym menu przewiń w dół do **Load Balancing**
4. Kliknij: **Target Groups**
5. Kliknij: **Create target group**

**Basic configuration:**
- **Choose a target type:** Instances
- **Target group name:** `forum-tg`
- **Protocol:** HTTP
- **Port:** `80`
- **VPC:** Wybierz `forum-vpc`

**Health checks:**
- **Health check protocol:** HTTP
- **Health check path:** `/health`
- **Advanced health check settings** (rozwiń):
  - **Healthy threshold:** `2`
  - **Unhealthy threshold:** `2`
  - **Timeout:** `5` seconds
  - **Interval:** `30` seconds
  - **Success codes:** `200`

6. Kliknij **Next**
7. **Register targets:** Pomiń (nie mamy jeszcze EC2)
8. Kliknij **Create target group**
9. **ZAPISZ Target Group ARN**

### 8.2. Utwórz Application Load Balancer

1. W lewym menu kliknij: **Load Balancers**
2. Kliknij: **Create load balancer**
3. Wybierz: **Application Load Balancer** → **Create**

**Basic configuration:**
- **Load balancer name:** `forum-alb`
- **Scheme:** Internet-facing
- **IP address type:** IPv4

**Network mapping:**
- **VPC:** Wybierz `forum-vpc`
- **Mappings:** Zaznacz checkboxy przy:
  - **eu-central-1a:** Wybierz `forum-public-subnet-1a`
  - **eu-central-1b:** Wybierz `forum-public-subnet-1b`

**Security groups:**
- Usuń `default`
- Wybierz: `forum-alb-sg`

**Listeners and routing:**
- **Protocol:** HTTP
- **Port:** 80
- **Default action:** Forward to `forum-tg`

4. Kliknij **Create load balancer**
5. ⏳ Poczekaj 2-3 minuty aż status zmieni się na **Active**
6. **ZAPISZ ALB DNS name** (np. `forum-alb-123456789.eu-central-1.elb.amazonaws.com`)

**✅ Checkpoint:** ALB utworzony i dostępny

---

## 🐳 KROK 9: ECR Repository (Docker)

**Co to jest ECR?** To rejestr dla Twoich Docker images.

1. W wyszukiwaniu wpisz: **ECR**
2. Kliknij **Elastic Container Registry**
3. Kliknij: **Get Started** (jeśli pierwszy raz) lub **Create repository**

**Settings:**
- **Visibility settings:** Private
- **Repository name:** `forum-backend`
- **Tag immutability:** Enable
- **Scan on push:** Enable
- **Encryption:** Pozostaw domyślne (AES-256)

4. Kliknij **Create repository**
5. **ZAPISZ Repository URI** (np. `123456789012.dkr.ecr.eu-central-1.amazonaws.com/forum-backend`)

**✅ Checkpoint:** ECR Repository utworzony

---

## 🪣 KROK 10: S3 Bucket (Frontend)

**Co to jest S3?** Storage dla plików. Tutaj będziemy trzymać React build.

1. W wyszukiwaniu wpisz: **S3**
2. Kliknij **S3**
3. Kliknij: **Create bucket**

**General configuration:**
- **Bucket name:** `forum-frontend-builds-[TWOJA-UNIKALNA-NAZWA]`
  - ⚠️ Nazwa musi być globalnie unikalna! Dodaj np. swoje inicjały
  - Przykład: `forum-frontend-builds-tomek-2024`
- **AWS Region:** eu-central-1

**Object Ownership:**
- Zostaw: **ACLs disabled**

**Block Public Access settings:**
- Zostaw WSZYSTKIE zaznaczone (bucket NIE ma być publiczny!)

**Bucket Versioning:**
- Wybierz: **Enable**

**Default encryption:**
- Zostaw domyślne (SSE-S3)

4. Kliknij **Create bucket**
5. **ZAPISZ Bucket name** do notatnika

**✅ Checkpoint:** S3 Bucket utworzony

---

## 👤 KROK 11: IAM Role dla EC2

**Co to jest IAM Role?** Pozwala EC2 wykonywać akcje w AWS (np. pobierać z ECR, S3).

### 11.1. Utwórz Role

1. W wyszukiwaniu wpisz: **IAM**
2. Kliknij **IAM**
3. W lewym menu kliknij: **Roles**
4. Kliknij: **Create role**

**Trusted entity type:**
- Wybierz: **AWS service**
- **Use case:** Wybierz **EC2**
- Kliknij **Next**

**Add permissions:**
Wpisz w wyszukiwaniu i zaznacz:
1. `AmazonEC2ContainerRegistryReadOnly` (dostęp do ECR)
2. `AmazonS3ReadOnlyAccess` (dostęp do S3)
3. `CloudWatchAgentServerPolicy` (monitoring)
4. `AmazonSSMManagedInstanceCore` (Session Manager - bezpieczne SSH)

Kliknij **Next**

**Name, review, and create:**
- **Role name:** `forum-ec2-role`
- **Description:** `IAM role for Forum EC2 instances`

5. Kliknij **Create role**
6. **ZAPISZ Role name:** `forum-ec2-role`

**✅ Checkpoint:** IAM Role utworzona

---

## 🎉 DAY 1 ZAKOŃCZONY!

### ✅ Checklist - Co masz utworzone:

- [ ] VPC (`forum-vpc`)
- [ ] 6 Subnets (2 public, 2 private, 2 database)
- [ ] Internet Gateway podłączony
- [ ] NAT Gateway w public subnet
- [ ] 2 Route Tables (public i private)
- [ ] 3 Security Groups (ALB, EC2, RDS)
- [ ] RDS PostgreSQL (`forum-db`) - ⏳ Status: Available
- [ ] Application Load Balancer (`forum-alb`) - ⏳ Status: Active
- [ ] Target Group (`forum-tg`)
- [ ] ECR Repository (`forum-backend`)
- [ ] S3 Bucket (`forum-frontend-builds-xxx`)
- [ ] IAM Role (`forum-ec2-role`)

### 📝 Sprawdź `AWS_IDs_TRACKER.md`

Upewnij się, że zapisałeś WSZYSTKIE IDs:
- VPC ID
- Subnet IDs (wszystkie 6)
- Internet Gateway ID
- NAT Gateway ID
- Route Table IDs (2)
- Security Group IDs (3)
- RDS Endpoint
- ALB DNS Name
- Target Group ARN
- ECR Repository URI
- S3 Bucket Name
- IAM Role Name

---

## 🛌 Odpoczynek

Zrobione! Infrastruktura gotowa. 

**Jutro:** Deployment aplikacji (Docker, EC2, Cloudflare)

**Następny krok:** [DAY_2_DEPLOYMENT.md](DAY_2_DEPLOYMENT.md)

---

## 🆘 Troubleshooting DAY 1

### "VPC limit exceeded"
- Default limit to 5 VPCs per region
- Usuń nieużywane VPCs lub poproś o zwiększenie limitu

### "NAT Gateway nie zmienia się na Available"
- Poczekaj 3-5 minut
- Sprawdź czy Elastic IP jest przypisane

### "RDS tworzenie trwa długo"
- To normalne! RDS może tworzyć się 10-15 minut
- Nie przerywaj procesu

### "ALB nie chce się utworzyć"
- Sprawdź czy wybrałeś 2 PUBLICZNE subnets
- Sprawdź czy są w różnych Availability Zones

### "Nie widzę Free Tier przy RDS"
- Sprawdź czy wybrałeś **db.t3.micro**
- Free Tier działa tylko przez pierwsze 12 miesięcy

### "Security Group nie zapisuje reguł"
- Sprawdź czy wybrałeś prawidłową VPC
- Sprawdź format CIDR (0.0.0.0/0 dla wszystkich)

---

**Problem nie jest wymieniony?** Sprawdź AWS CloudTrail lub skontaktuj się z zespołem.

