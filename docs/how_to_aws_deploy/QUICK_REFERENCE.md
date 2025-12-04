# 🚀 Quick Reference - AWS CLI Commands

Szybki dostęp do najważniejszych komend AWS CLI.

---

## 📋 Setup

### Configure AWS CLI
```bash
aws configure
# AWS Access Key ID: [Twój klucz]
# AWS Secret Access Key: [Twój secret]
# Default region: eu-central-1
# Default output format: json
```

### Sprawdź konfigurację
```bash
aws sts get-caller-identity
aws configure list
```

---

## 🐳 ECR (Docker Registry)

### Login do ECR
```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin [ACCOUNT-ID].dkr.ecr.eu-central-1.amazonaws.com
```

### List repositories
```bash
aws ecr describe-repositories
```

### List images w repository
```bash
aws ecr list-images --repository-name forum-backend
```

### Build, tag, push image
```bash
# Build
cd backend
docker build -t forum-backend .

# Tag
docker tag forum-backend:latest [ECR-URI]:latest

# Push
docker push [ECR-URI]:latest
```

---

## 🪣 S3 (Storage)

### List buckets
```bash
aws s3 ls
```

### List plików w bucket
```bash
aws s3 ls s3://forum-frontend-builds-xxx/
aws s3 ls s3://forum-frontend-builds-xxx/latest/ --recursive
```

### Upload plików
```bash
aws s3 cp file.txt s3://bucket-name/
aws s3 sync ./local-folder/ s3://bucket-name/remote-folder/ --delete
```

### Download plików
```bash
aws s3 cp s3://bucket-name/file.txt ./
aws s3 sync s3://bucket-name/remote-folder/ ./local-folder/
```

### Usuń pliki
```bash
aws s3 rm s3://bucket-name/file.txt
aws s3 rm s3://bucket-name/folder/ --recursive
```

---

## 🗄️ RDS (Database)

### Describe RDS instances
```bash
aws rds describe-db-instances
```

### Specific instance info
```bash
aws rds describe-db-instances --db-instance-identifier forum-db
```

### Get RDS endpoint
```bash
aws rds describe-db-instances --db-instance-identifier forum-db --query "DBInstances[0].Endpoint.Address" --output text
```

### Stop RDS (oszczędzanie kosztów)
```bash
aws rds stop-db-instance --db-instance-identifier forum-db
```

### Start RDS
```bash
aws rds start-db-instance --db-instance-identifier forum-db
```

### RDS status
```bash
aws rds describe-db-instances --db-instance-identifier forum-db --query "DBInstances[0].DBInstanceStatus" --output text
```

---

## 🖥️ EC2 (Compute)

### List wszystkich instancji
```bash
aws ec2 describe-instances
```

### List running instances
```bash
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"
```

### List instancji z Auto Scaling Group
```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names forum-asg --query "AutoScalingGroups[0].Instances"
```

### Get instance ID
```bash
aws ec2 describe-instances --filters "Name=tag:Name,Values=forum-ec2-asg" --query "Reservations[].Instances[].InstanceId" --output text
```

### Connect via Session Manager
```bash
# Install Session Manager plugin first: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html

aws ssm start-session --target [INSTANCE-ID]
```

### Stop instance
```bash
aws ec2 stop-instances --instance-ids [INSTANCE-ID]
```

### Start instance
```bash
aws ec2 start-instances --instance-ids [INSTANCE-ID]
```

### Terminate instance
```bash
aws ec2 terminate-instances --instance-ids [INSTANCE-ID]
```

---

## 📊 Auto Scaling Group

### Describe ASG
```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names forum-asg
```

### Get desired capacity
```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names forum-asg --query "AutoScalingGroups[0].DesiredCapacity"
```

### Update capacity
```bash
# Scale down to 0 (save money)
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name forum-asg \
  --min-size 0 \
  --max-size 0 \
  --desired-capacity 0

# Scale back up to 2
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name forum-asg \
  --min-size 1 \
  --max-size 4 \
  --desired-capacity 2
```

### Instance refresh (deploy new version)
```bash
aws autoscaling start-instance-refresh \
  --auto-scaling-group-name forum-asg \
  --preferences MinHealthyPercentage=50
```

### Check instance refresh status
```bash
aws autoscaling describe-instance-refreshes \
  --auto-scaling-group-name forum-asg
```

---

## ⚖️ Load Balancer

### Describe load balancers
```bash
aws elbv2 describe-load-balancers
```

### Get ALB DNS name
```bash
aws elbv2 describe-load-balancers --names forum-alb --query "LoadBalancers[0].DNSName" --output text
```

### Describe target groups
```bash
aws elbv2 describe-target-groups --names forum-tg
```

### Get target health
```bash
aws elbv2 describe-target-health --target-group-arn [TARGET-GROUP-ARN]
```

---

## 🔐 Systems Manager Parameter Store

### List parameters
```bash
aws ssm describe-parameters
```

### Get parameter value (bez decryption)
```bash
aws ssm get-parameter --name "/forum/ALLOWED_HOSTS"
```

### Get parameter value (z decryption)
```bash
aws ssm get-parameter --name "/forum/SECRET_KEY" --with-decryption --query "Parameter.Value" --output text
```

### Put/Update parameter
```bash
# String
aws ssm put-parameter --name "/forum/ALLOWED_HOSTS" --value "example.com,localhost" --type String --overwrite

# SecureString
aws ssm put-parameter --name "/forum/SECRET_KEY" --value "my-secret-key" --type SecureString --overwrite
```

### Delete parameter
```bash
aws ssm delete-parameter --name "/forum/TEST"
```

---

## 🔒 Security Groups

### List security groups
```bash
aws ec2 describe-security-groups
```

### Describe specific SG
```bash
aws ec2 describe-security-groups --group-ids [SG-ID]
```

### Describe by name
```bash
aws ec2 describe-security-groups --filters "Name=group-name,Values=forum-alb-sg"
```

---

## 📝 CloudWatch Logs

### List log groups
```bash
aws logs describe-log-groups
```

### List log streams
```bash
aws logs describe-log-streams --log-group-name /aws/lambda/my-function
```

### Tail logs (live)
```bash
aws logs tail /aws/lambda/my-function --follow
```

---

## 🌐 VPC

### List VPCs
```bash
aws ec2 describe-vpcs
```

### List subnets
```bash
aws ec2 describe-subnets --filters "Name=vpc-id,Values=[VPC-ID]"
```

### List route tables
```bash
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=[VPC-ID]"
```

### List internet gateways
```bash
aws ec2 describe-internet-gateways
```

### List NAT gateways
```bash
aws ec2 describe-nat-gateways
```

---

## 💰 Cost Explorer

### Get current month costs
```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date -u +%Y-%m-01),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost
```

---

## 🔍 Useful Filters & Queries

### Find resources by tag
```bash
aws ec2 describe-instances --filters "Name=tag:Name,Values=forum-*"
```

### Get all resources in VPC
```bash
aws ec2 describe-instances --filters "Name=vpc-id,Values=[VPC-ID]"
```

### List resources by region
```bash
aws ec2 describe-instances --region eu-central-1
```

---

## 🚀 Deployment Shortcuts

### Full redeploy (after code changes)

```bash
# 1. Build and push Docker
cd backend
docker build -t forum-backend .
docker tag forum-backend:latest [ECR-URI]:latest
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin [ACCOUNT-ID].dkr.ecr.eu-central-1.amazonaws.com
docker push [ECR-URI]:latest

# 2. Build and upload React
cd ../frontend
npm run build
aws s3 sync build/ s3://[S3-BUCKET]/latest/ --delete

# 3. Refresh EC2 instances
aws autoscaling start-instance-refresh --auto-scaling-group-name forum-asg --preferences MinHealthyPercentage=50
```

### Quick scale (temporarily)

```bash
# Scale up (handle more traffic)
aws autoscaling set-desired-capacity --auto-scaling-group-name forum-asg --desired-capacity 4

# Scale down (save money)
aws autoscaling set-desired-capacity --auto-scaling-group-name forum-asg --desired-capacity 1
```

### Quick check status

```bash
# Check everything
echo "=== RDS ===" && \
aws rds describe-db-instances --db-instance-identifier forum-db --query "DBInstances[0].DBInstanceStatus" --output text && \
echo "=== ALB ===" && \
aws elbv2 describe-load-balancers --names forum-alb --query "LoadBalancers[0].State.Code" --output text && \
echo "=== ASG ===" && \
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names forum-asg --query "AutoScalingGroups[0].DesiredCapacity" && \
echo "=== EC2 Instances ===" && \
aws ec2 describe-instances --filters "Name=tag:Name,Values=forum-ec2-asg" "Name=instance-state-name,Values=running" --query "Reservations[].Instances[].[InstanceId,State.Name]" --output table
```

---

## 🆘 Emergency Commands

### Kill all EC2 in ASG (emergency stop)
```bash
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name forum-asg \
  --min-size 0 \
  --max-size 0 \
  --desired-capacity 0
```

### Restart single EC2
```bash
# Get instance ID
INSTANCE_ID=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=forum-ec2-asg" "Name=instance-state-name,Values=running" --query "Reservations[0].Instances[0].InstanceId" --output text)

# Reboot
aws ec2 reboot-instances --instance-ids $INSTANCE_ID
```

### Check logs on EC2
```bash
# Connect
aws ssm start-session --target [INSTANCE-ID]

# Then in session:
sudo su - ec2-user
docker logs forum-backend -f
sudo tail -f /var/log/user-data.log
sudo tail -f /var/log/nginx/error.log
```

---

## 📚 Przydatne Aliasy (dodaj do ~/.bashrc lub ~/.zshrc)

```bash
# Alias dla AWS
alias aws-whoami='aws sts get-caller-identity'
alias aws-region='aws configure get region'

# Forum specific
alias forum-asg='aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names forum-asg'
alias forum-alb='aws elbv2 describe-load-balancers --names forum-alb'
alias forum-rds='aws rds describe-db-instances --db-instance-identifier forum-db'
alias forum-instances='aws ec2 describe-instances --filters "Name=tag:Name,Values=forum-ec2-asg" "Name=instance-state-name,Values=running" --query "Reservations[].Instances[].[InstanceId,PrivateIpAddress,State.Name]" --output table'
alias forum-scale-down='aws autoscaling update-auto-scaling-group --auto-scaling-group-name forum-asg --min-size 0 --max-size 0 --desired-capacity 0'
alias forum-scale-up='aws autoscaling update-auto-scaling-group --auto-scaling-group-name forum-asg --min-size 1 --max-size 4 --desired-capacity 2'
```

---

## 🔗 Przydatne Linki

- **AWS CLI Documentation:** https://docs.aws.amazon.com/cli/
- **AWS CLI Reference:** https://awscli.amazonaws.com/v2/documentation/api/latest/index.html
- **AWS Free Tier:** https://aws.amazon.com/free/
- **AWS Calculator:** https://calculator.aws/
- **AWS Status:** https://status.aws.amazon.com/

---

## 💡 Tips

1. **Zawsze sprawdzaj region:** `aws configure get region`
2. **Używaj --dry-run:** Niektóre komendy wspierają dry-run do testowania
3. **Output formats:** `--output json|text|table|yaml`
4. **Query:** Używaj `--query` do filtrowania: https://jmespath.org/
5. **Profile:** Możesz mieć wiele profili: `aws configure --profile dev`
6. **Pagination:** Dla dużych list: `--max-items` i `--starting-token`

---

**Ostatnia aktualizacja:** 2024

