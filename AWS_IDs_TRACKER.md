# 📝 AWS IDs TRACKER - ZAPISUJ WSZYSTKIE ID TUTAJ!

**WAŻNE:** Skopiuj ten plik i wypełniaj podczas deploymentu!

Data: __________  
Kto wypełnia: __________

---

## 🔐 AWS CREDENTIALS

```
AWS Account ID: ______________________
IAM Username: ______________________
Access Key ID: ______________________
Secret Access Key: ______________________
Region: eu-central-1
```

---

## 🌐 VPC & NETWORKING

```
VPC ID: vpc-______________________

Internet Gateway ID: igw-______________________

PUBLIC SUBNETS:
  Public Subnet 1 (1a): subnet-______________________
  Public Subnet 2 (1b): subnet-______________________

PRIVATE SUBNETS:
  Private Subnet 1 (1a): subnet-______________________
  Private Subnet 2 (1b): subnet-______________________

NAT GATEWAY:
  Elastic IP Allocation: eipalloc-______________________
  NAT Gateway ID: nat-______________________

ROUTE TABLES:
  Public RT: rtb-______________________
  Private RT: rtb-______________________
```

---

## 🔒 SECURITY GROUPS

```
ALB Security Group: sg-______________________
EC2 Security Group: sg-______________________
RDS Security Group: sg-______________________
```

---

## 🗄️ RDS POSTGRESQL

```
DB Instance Identifier: forum-db
DB Subnet Group: forum-db-subnet-group

Master Username: forumadmin
Master Password: ______________________
  (ZAPISZ BEZPIECZNIE!)

DB Name: forumdb
DB Endpoint: forum-db.______________________.eu-central-1.rds.amazonaws.com

Port: 5432
```

**DATABASE_URL (pełny):**
```
postgresql://forumadmin:HASŁO@ENDPOINT:5432/forumdb
```

---

## 📦 ECR REPOSITORY

```
Repository Name: forum-backend
ECR URI: ______________________.dkr.ecr.eu-central-1.amazonaws.com/forum-backend
```

---

## ⚖️ LOAD BALANCER

```
Target Group Name: forum-tg
Target Group ARN: arn:aws:elasticloadbalancing:eu-central-1:______:targetgroup/forum-tg/________________

Application Load Balancer Name: forum-alb
ALB ARN: arn:aws:elasticloadbalancing:eu-central-1:______:loadbalancer/app/forum-alb/________________
ALB DNS: forum-alb-________________.eu-central-1.elb.amazonaws.com

Listener ARN: arn:aws:elasticloadbalancing:eu-central-1:______:listener/app/forum-alb/________________
```

---

## 🚀 AUTO SCALING

```
Launch Template Name: forum-launch-template
Launch Template ID: lt-______________________

Auto Scaling Group Name: forum-asg

Key Pair Name: forum-key
Key Pair File: forum-key.pem (LOCATION: ______________________)
```

---

## 💻 EC2 INSTANCES

```
Instance 1:
  Instance ID: i-______________________
  Private IP: 10.0.10.____
  AZ: eu-central-1a
  Status: ____________

Instance 2:
  Instance ID: i-______________________
  Private IP: 10.0.11.____
  AZ: eu-central-1b
  Status: ____________
```

---

## 🔐 IAM ROLES

```
Role Name: EC2-Forum-Role
Role ARN: arn:aws:iam::______________________:role/EC2-Forum-Role

Instance Profile Name: EC2-Forum-Profile
Instance Profile ARN: arn:aws:iam::______________________:instance-profile/EC2-Forum-Profile
```

---

## 🔑 SECRETS (Parameter Store)

```
/forum/DATABASE_URL: ✅ Created
/forum/SECRET_KEY: ✅ Created
/forum/ALLOWED_HOSTS: ✅ Created
/forum/CORS_ALLOWED_ORIGINS: ✅ Created
```

**SECRET_KEY (zapisz backup):**
```
______________________________________________________
```

---

## 🌍 CLOUDFLARE

```
Domain: ______________________
Cloudflare Account Email: ______________________

Nameservers:
  NS 1: ____________________.ns.cloudflare.com
  NS 2: ____________________.ns.cloudflare.com

DNS Records:
  Type: CNAME
  Name: api
  Target: forum-alb-________________.eu-central-1.elb.amazonaws.com
  Proxy: ☑️ Proxied

  Type: CNAME (if frontend)
  Name: www
  Target: ______________________
  Proxy: ☐ DNS only
```

---

## 🔗 FINAL URLs

```
Backend API: https://api.______________________
Admin Panel: https://api.______________________/admin/
Frontend: https://______________________ (if deployed)

Health Check: https://api.______________________/api/health/
```

---

## 📊 CREDENTIALS FOR DEMO

```
Django Admin:
  Username: admin
  Password: ______________________

Test User:
  Email: alice@example.com
  Password: password123
```

---

## 💰 COST TRACKING

```
Expected Monthly Cost: $____________________
Free Tier Coverage: $____________________
Actual Cost (after 30 days): $____________________
```

---

## 🆘 TROUBLESHOOTING QUICK REFERENCE

### Connect to EC2:
```bash
aws ssm start-session --target i-______________________
```

### Check Docker logs:
```bash
sudo docker logs forum-backend
```

### Check user-data logs:
```bash
sudo cat /var/log/user-data.log
```

### Restart application:
```bash
aws autoscaling start-instance-refresh --auto-scaling-group-name forum-asg
```

---

## 📸 SCREENSHOTS LOCATIONS

```
VPC Diagram: ______________________
EC2 Instances: ______________________
RDS Database: ______________________
ALB Dashboard: ______________________
Cloudflare Analytics: ______________________
Application Working: ______________________
```

---

## ✅ COMPLETION STATUS

- [ ] All IDs recorded
- [ ] Passwords saved securely
- [ ] Backup created
- [ ] Team has access to this file
- [ ] Ready for presentation

---

**LAST UPDATED:** __________ by __________




