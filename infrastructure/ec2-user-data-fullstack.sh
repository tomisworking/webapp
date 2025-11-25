#!/bin/bash
# EC2 User Data Script - Full-stack deployment
# Installs: Docker (Django backend) + Nginx + React frontend

set -e

# Log everything
exec > >(tee /var/log/user-data.log)
exec 2>&1

echo "===== Starting Full-Stack Forum App Setup ====="
echo "Timestamp: $(date)"

# ============================================
# 1. SYSTEM UPDATES & DEPENDENCIES
# ============================================
echo "Step 1: Installing system dependencies..."
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Nginx
yum install -y nginx

# Install AWS CLI v2 (if not present)
if ! command -v aws &> /dev/null; then
    echo "Installing AWS CLI..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip -q awscliv2.zip
    ./aws/install
    rm -rf aws awscliv2.zip
fi

# ============================================
# 2. GET SECRETS FROM PARAMETER STORE
# ============================================
echo "Step 2: Fetching secrets from Parameter Store..."
export AWS_DEFAULT_REGION=eu-central-1

DATABASE_URL=$(aws ssm get-parameter --name "/forum/DATABASE_URL" --with-decryption --query 'Parameter.Value' --output text)
SECRET_KEY=$(aws ssm get-parameter --name "/forum/SECRET_KEY" --with-decryption --query 'Parameter.Value' --output text)
ALLOWED_HOSTS=$(aws ssm get-parameter --name "/forum/ALLOWED_HOSTS" --query 'Parameter.Value' --output text)
CORS_ALLOWED_ORIGINS=$(aws ssm get-parameter --name "/forum/CORS_ALLOWED_ORIGINS" --query 'Parameter.Value' --output text)

echo "Secrets loaded successfully"

# ============================================
# 3. SETUP BACKEND (Django in Docker)
# ============================================
echo "Step 3: Setting up Django backend..."

# Login to ECR
echo "Logging into ECR..."
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin AWS_ACCOUNT_ID_PLACEHOLDER.dkr.ecr.eu-central-1.amazonaws.com

# Pull Django Docker image
echo "Pulling Django Docker image..."
docker pull ECR_URI_PLACEHOLDER:latest

# Run Django container
echo "Starting Django container..."
docker run -d \
  --name forum-backend \
  --restart unless-stopped \
  -p 8000:8000 \
  -e DATABASE_URL="$DATABASE_URL" \
  -e SECRET_KEY="$SECRET_KEY" \
  -e DEBUG=False \
  -e ALLOWED_HOSTS="$ALLOWED_HOSTS" \
  -e CORS_ALLOWED_ORIGINS="$CORS_ALLOWED_ORIGINS" \
  -e CSRF_TRUSTED_ORIGINS="$CORS_ALLOWED_ORIGINS" \
  ECR_URI_PLACEHOLDER:latest

# Wait for Django to start
echo "Waiting for Django to start..."
sleep 30

# Check Django health
if curl -f http://localhost:8000/api/health/ 2>/dev/null; then
    echo "✅ Django backend is healthy!"
else
    echo "⚠️  Django health check failed, checking logs..."
    docker logs forum-backend | tail -20
fi

# ============================================
# 4. SETUP FRONTEND (React build)
# ============================================
echo "Step 4: Setting up React frontend..."

# Create frontend directory
mkdir -p /var/www/frontend

# Option A: Download pre-built frontend from S3
if aws s3 ls s3://FRONTEND_BUCKET_PLACEHOLDER/latest/ 2>/dev/null; then
    echo "Downloading frontend build from S3..."
    aws s3 sync s3://FRONTEND_BUCKET_PLACEHOLDER/latest/ /var/www/frontend/
    echo "✅ Frontend downloaded from S3"
else
    echo "⚠️  No frontend build found in S3"
    echo "Creating placeholder index.html..."
    cat > /var/www/frontend/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Forum - Backend Ready</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
        .status { color: green; font-size: 24px; }
        a { color: #007bff; text-decoration: none; }
    </style>
</head>
<body>
    <h1>Forum Backend is Running!</h1>
    <p class="status">✅ Django API is ready</p>
    <p><a href="/api/health/">Check API Health</a></p>
    <p><a href="/admin/">Django Admin</a></p>
    <p><small>Frontend will be deployed soon...</small></p>
</body>
</html>
EOF
fi

# Set permissions
chown -R nginx:nginx /var/www/frontend
chmod -R 755 /var/www/frontend

# ============================================
# 5. CONFIGURE NGINX
# ============================================
echo "Step 5: Configuring Nginx..."

# Backup default config
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Create Nginx config
cat > /etc/nginx/conf.d/forum.conf << 'NGINXCONF'
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

    # Deny hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
NGINXCONF

# Remove default server block
rm -f /etc/nginx/conf.d/default.conf

# Test Nginx config
nginx -t

# Start Nginx
systemctl start nginx
systemctl enable nginx

echo "✅ Nginx configured and started"

# ============================================
# 6. VERIFY SETUP
# ============================================
echo "Step 6: Verifying setup..."

# Check services
echo "Checking Docker container..."
docker ps | grep forum-backend

echo "Checking Nginx..."
systemctl status nginx --no-pager

# Test endpoints
echo "Testing endpoints..."
echo "- Health check (Nginx): $(curl -s http://localhost/health)"
echo "- API health (Django): $(curl -s http://localhost/api/health/ | head -c 50)"

# ============================================
# 7. SETUP COMPLETE
# ============================================
echo "===== Setup Complete! ====="
echo "Instance IP: $(hostname -I | awk '{print $1}')"
echo "Services running:"
echo "  - Nginx: http://localhost:80"
echo "  - Django: http://localhost:8000"
echo "  - Frontend: http://localhost/"
echo "  - API: http://localhost/api/"
echo "  - Admin: http://localhost/admin/"
echo ""
echo "Check logs:"
echo "  - User-data: /var/log/user-data.log"
echo "  - Nginx: /var/log/nginx/"
echo "  - Django: docker logs forum-backend"
echo ""
echo "Deployment timestamp: $(date)"


