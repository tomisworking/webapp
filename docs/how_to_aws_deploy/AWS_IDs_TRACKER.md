# 📝 AWS IDs TRACKER - ZAPISUJ WSZYSTKIE ID TUTAJ!

**WAŻNE:** Skopiuj ten plik i wypełniaj podczas deploymentu!

Data: __________  
Kto wypełnia: __________

---

## 🔐 AWS CREDENTIALS

```
AWS Account ID: 311603531332
IAM Username: ______________________ (wypełnij swoim username)
Access Key ID: ______________________ (nie udostępniaj publicznie!)
Secret Access Key: ______________________ (nie udostępniaj publicznie!)
Region: us-east-1
```

---

## 🌐 VPC & NETWORKING

```
VPC ID: vpc-05ff311c776e4aea1

Internet Gateway ID: igw-00d4728afdddf92db

PUBLIC SUBNETS:
  Public Subnet 1 (1a): subnet-0e801890e6a1c3e7a
  Public Subnet 2 (1b): subnet-0976ad46c2ca3bd73

PRIVATE SUBNETS:
  Private Subnet 1 (1a): subnet-072cc390fea8a3d4d
  Private Subnet 2 (1b): subnet-0a0e069ccfd7ce27e

DB SUBNETS:
  DB Subnet 1 (1a): subnet-0a5d74c8848073011
  DB Subnet 2 (1b): subnet-079f042372b89ecec

NAT GATEWAY:
  Elastic IP Address: 100.28.147.103
  NAT Gateway ID: nat-0464aca433dfa4772

ROUTE TABLES:
  Public RT: rtb-07882c1169a86da99
  Private RT: rtb-0ed3fe72e62ac8fea
```

---

## 🔒 SECURITY GROUPS

```
ALB Security Group: sg-01929c8ed5d6bd382
EC2 Security Group: sg-0952d8bb8c260cd52
RDS Security Group: sg-0e95c59beccd25718
```

---

## 🗄️ RDS POSTGRESQL

```
DB Instance Identifier: forum-db
DB Subnet Group: forum-db-subnet-group

Master Username: forumadmin
Master Password: ForumDB2024!Secure
  (ZAPISZ BEZPIECZNIE!)

DB Name: forumdb
DB Endpoint: forum-db.caps6eywcswv.us-east-1.rds.amazonaws.com

Port: 5432
```

**DATABASE_URL (pełny):**
```
postgresql://forumadmin:ForumDB2024!Secure@forum-db.caps6eywcswv.us-east-1.rds.amazonaws.com:5432/forumdb
```

---

## 📦 ECR REPOSITORY

```
Repository Name: forum-backend
ECR URI: 311603531332.dkr.ecr.us-east-1.amazonaws.com/forum-backend
```

---

## ⚖️ LOAD BALANCER

```
Target Group Name: forum-tg
Target Group ARN: arn:aws:elasticloadbalancing:us-east-1:311603531332:targetgroup/forum-tg/2fcc31d5819edc32

Application Load Balancer Name: forum-alb
ALB ARN: arn:aws:elasticloadbalancing:us-east-1:311603531332:loadbalancer/app/forum-alb/________________
ALB DNS: forum-alb-1684129147.us-east-1.elb.amazonaws.com

Listener ARN: arn:aws:elasticloadbalancing:us-east-1:311603531332:listener/app/forum-alb/________________
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
Role Name: forum-ec2-role
Role ARN: arn:aws:iam::311603531332:role/forum-ec2-role

Instance Profile Name: forum-ec2-role
Instance Profile ARN: arn:aws:iam::311603531332:instance-profile/forum-ec2-role
```

---

## 🔑 SECRETS (Parameter Store)

```
/forum/DATABASE_URL: ✅ Created
/forum/SECRET_KEY: ✅ Created
/forum/ALLOWED_HOSTS: ✅ Created
/forum/FRONTEND_BUCKET: forum-frontend-builds-kongoapp
```

**SECRET_KEY (zapisz backup):**
```
django-insecure-dev-key-change-in-production-123456789
```

**S3 Bucket Name:**
```
forum-frontend-builds-kongoapp
```

---

## 🌍 CLOUDFLARE

```
Domain: ______________________ (twoja domena, np. mojeforum.tk)
Cloudflare Account Email: ______________________

Nameservers:
  NS 1: ____________________.ns.cloudflare.com
  NS 2: ____________________.ns.cloudflare.com

DNS Records:
  Type: CNAME
  Name: @ (root domain)
  Target: forum-alb-1684129147.us-east-1.elb.amazonaws.com
  Proxy: ☑️ Proxied

  Type: CNAME
  Name: www
  Target: forum-alb-1684129147.us-east-1.elb.amazonaws.com
  Proxy: ☑️ Proxied
```

---

## 🔗 FINAL URLs

```
ALB Direct Access (HTTP): http://forum-alb-1684129147.us-east-1.elb.amazonaws.com
Health Check: http://forum-alb-1684129147.us-east-1.elb.amazonaws.com/health
API Categories: http://forum-alb-1684129147.us-east-1.elb.amazonaws.com/api/categories/
Admin Panel: http://forum-alb-1684129147.us-east-1.elb.amazonaws.com/admin/

With Cloudflare (HTTPS - po konfiguracji domeny):
Frontend: https://[TWOJA-DOMENA]
Admin Panel: https://[TWOJA-DOMENA]/admin/
Health Check: https://[TWOJA-DOMENA]/api/health/
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


