# ✅ DEPLOYMENT CHECKLIST - WYDRUKUJ I ODZNACZAJ!

Data rozpoczęcia: __________  
Zespół: ________________

---

## 🎯 DZIEŃ 1 - INFRASTRUCTURE (Wtorek)

### Przygotowanie (30 min)
- [ ] Konto AWS utworzone
- [ ] Region wybrany: eu-central-1
- [ ] AWS CLI zainstalowany i skonfigurowany
- [ ] IAM user utworzony z AdministratorAccess

### VPC i Networking (1h)
- [ ] VPC utworzone (10.0.0.0/16)
- [ ] Internet Gateway created i attached
- [ ] Public Subnet 1 (10.0.1.0/24) - eu-central-1a
- [ ] Public Subnet 2 (10.0.2.0/24) - eu-central-1b
- [ ] Private Subnet 1 (10.0.10.0/24) - eu-central-1a
- [ ] Private Subnet 2 (10.0.11.0/24) - eu-central-1b
- [ ] Elastic IP allocated
- [ ] NAT Gateway created (w public subnet 1)
- [ ] Public Route Table created
- [ ] Public RT: route do IGW (0.0.0.0/0)
- [ ] Public RT: associated z public subnets
- [ ] Private Route Table created
- [ ] Private RT: route do NAT GW (0.0.0.0/0)
- [ ] Private RT: associated z private subnets

### Security Groups (30 min)
- [ ] ALB Security Group (port 80, 443 from 0.0.0.0/0)
- [ ] EC2 Security Group (port 80 from ALB SG, SSH from my IP)
- [ ] RDS Security Group (port 5432 from EC2 SG)

### RDS PostgreSQL (1h)
- [ ] DB Subnet Group created
- [ ] Silne hasło wygenerowane i ZAPISANE
- [ ] RDS instance created (db.t3.micro)
- [ ] RDS status: available
- [ ] RDS Endpoint ZAPISANY

### ECR (10 min)
- [ ] ECR repository created
- [ ] ECR URI ZAPISANY

### Application Load Balancer (45 min)
- [ ] Target Group created (health check: /api/health/)
- [ ] Application Load Balancer created
- [ ] ALB w public subnets
- [ ] Listener HTTP:80 → Target Group
- [ ] ALB DNS name ZAPISANY

### IAM (15 min)
- [ ] IAM Role: EC2-Forum-Role created
- [ ] Policies attached (SSM, CloudWatch, ECR)
- [ ] Instance Profile created

### Secrets (15 min)
- [ ] Parameter Store: DATABASE_URL
- [ ] Parameter Store: SECRET_KEY
- [ ] Parameter Store: ALLOWED_HOSTS
- [ ] Parameter Store: CORS_ALLOWED_ORIGINS

**KONIEC DNIA 1** ✅  
Czas zakończenia: __________

---

## 🚀 DZIEŃ 2 - DEPLOYMENT (Środa)

### Docker Image (1h)
- [ ] Docker Desktop uruchomiony
- [ ] Zalogowany do ECR
- [ ] Docker image zbudowany lokalnie
- [ ] Image przetestowany lokalnie (opcjonalnie)
- [ ] Image tagged dla ECR
- [ ] Image pushed do ECR (latest + versioned)
- [ ] Image widoczny w ECR Console

### Launch Template (30 min)
- [ ] Latest AMI ID pobrany
- [ ] User data script utworzony i zmodyfikowany
- [ ] Key Pair created i ZAPISANY (.pem file)
- [ ] Launch Template created

### Auto Scaling Group (30 min)
- [ ] ASG created (min:1, max:3, desired:2)
- [ ] ASG w private subnets
- [ ] Target Group attached
- [ ] Scaling policy created (CPU 70%)
- [ ] Instancje uruchomione (2/2)
- [ ] Instancje InService

### Health Checks (15 min)
- [ ] Target Group: healthy (2/2)
- [ ] Test: curl ALB_DNS/api/health/ → success
- [ ] Test: curl ALB_DNS/api/categories/ → success

### Migracja Bazy (30 min)
- [ ] Połączenie z EC2 przez Session Manager
- [ ] Docker container running
- [ ] Migrations executed
- [ ] Superuser created
- [ ] Test data loaded (seed_data)

### Cloudflare (1h)
- [ ] Domena zakupiona/gotowa
- [ ] Domena dodana do Cloudflare
- [ ] Nameservers zmienione u rejestratora
- [ ] DNS propagation completed
- [ ] CNAME record created (api → ALB DNS)
- [ ] SSL/TLS: Full mode
- [ ] Always Use HTTPS: ON
- [ ] HSTS enabled
- [ ] Security features configured

### Aktualizacja Parametrów (15 min)
- [ ] ALLOWED_HOSTS updated z domeną
- [ ] CORS_ALLOWED_ORIGINS updated z domeną
- [ ] ASG instance refresh triggered
- [ ] New instances healthy

### Testy Finalne (30 min)
- [ ] Test: https://domena/api/health/
- [ ] Test: https://domena/api/categories/
- [ ] Test: https://domena/admin/
- [ ] SSL Labs scan: Grade A
- [ ] Browser test: works perfectly
- [ ] Mobile test: responsive

### Frontend (BONUS - jeśli zostanie czas)
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] REACT_APP_API_URL configured
- [ ] Custom domain in Vercel
- [ ] DNS record for frontend
- [ ] CORS updated for frontend domain
- [ ] Frontend accessible and working

**KONIEC DNIA 2** ✅  
Czas zakończenia: __________

---

## 📸 DOKUMENTACJA DO PREZENTACJI

- [ ] Screenshot: AWS VPC diagram
- [ ] Screenshot: EC2 instances running
- [ ] Screenshot: RDS database
- [ ] Screenshot: ALB with healthy targets
- [ ] Screenshot: Cloudflare dashboard
- [ ] Screenshot: Application working
- [ ] Screenshot: Admin panel
- [ ] Screenshot: SSL Labs A+ grade
- [ ] Diagram architektury (draw.io)

---

## 📊 METRYKI DO POKAZANIA

- [ ] Number of EC2 instances: ____
- [ ] Database size: ____ MB
- [ ] Total requests handled: ____
- [ ] Average response time: ____ ms
- [ ] Uptime: _____%
- [ ] SSL Grade: ____
- [ ] Threats blocked by Cloudflare: ____

---

## 🎓 PRZYGOTOWANIE DO PREZENTACJI

### Demo Flow:
1. [ ] Pokazać live aplikację (frontend + backend)
2. [ ] Pokazać AWS Console (VPC, EC2, RDS, ALB)
3. [ ] Pokazać Auto Scaling w akcji
4. [ ] Pokazać Cloudflare dashboard
5. [ ] Pokazać monitoring (CloudWatch)
6. [ ] Pokazać logs
7. [ ] Q&A preparation

### Kto co prezentuje:
- Osoba 1: _________________ → VPC i networking
- Osoba 2: _________________ → Database i backend
- Osoba 3: _________________ → Auto Scaling i Load Balancer
- Osoba 4: _________________ → Cloudflare i security

---

## ✅ FINALNA WERYFIKACJA (przed prezentacją)

- [ ] Aplikacja działa przez https://
- [ ] Wszystkie API endpoints działają
- [ ] Admin panel dostępny
- [ ] Auto Scaling działa (przetestowane)
- [ ] Health checks: 100%
- [ ] SSL certificate: valid
- [ ] No errors in logs
- [ ] Database: migrated + data loaded
- [ ] Team confident in presenting

---

## 🆘 EMERGENCY CONTACTS

AWS Support: ____________________  
Cloudflare Support: ____________________  
Team Lead: ____________________  

---

**POWODZENIA! 🚀**

Podpisy zespołu:

1. _________________ Data: _______
2. _________________ Data: _______
3. _________________ Data: _______
4. _________________ Data: _______
