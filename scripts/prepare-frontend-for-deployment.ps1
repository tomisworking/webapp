# PowerShell script to build React frontend and upload to S3 for EC2 deployment

$ErrorActionPreference = "Stop"

Write-Host "===== Frontend Deployment Preparation =====" -ForegroundColor Cyan
Write-Host ""

# Configuration
$FRONTEND_DIR = "./frontend"
$BUILD_DIR = "$FRONTEND_DIR/build"
$S3_BUCKET = "forum-frontend-builds"  # Change this to your bucket name
$S3_PATH = "latest"
$AWS_REGION = "eu-central-1"

# Step 1: Check if frontend directory exists
if (-not (Test-Path $FRONTEND_DIR)) {
    Write-Host "❌ Frontend directory not found: $FRONTEND_DIR" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Frontend directory found" -ForegroundColor Green

# Step 2: Install dependencies
Write-Host ""
Write-Host "Step 1: Installing npm dependencies..." -ForegroundColor Yellow
Push-Location $FRONTEND_DIR

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing packages..."
    npm install
} else {
    Write-Host "node_modules exists, skipping install"
}

# Step 3: Create production .env file
Write-Host ""
Write-Host "Step 2: Creating production environment file..." -ForegroundColor Yellow

# Get ALB DNS or domain
$API_DOMAIN = Read-Host "Enter your ALB DNS or domain (e.g., api.yourdomain.com)"

@"
# Production environment variables
REACT_APP_API_URL=https://${API_DOMAIN}
"@ | Out-File -FilePath ".env.production" -Encoding utf8

Write-Host "✅ Created .env.production" -ForegroundColor Green
Get-Content ".env.production"

# Step 4: Build React app
Write-Host ""
Write-Host "Step 3: Building React application..." -ForegroundColor Yellow
npm run build

if (-not (Test-Path "build")) {
    Write-Host "❌ Build failed - build directory not found" -ForegroundColor Red
    exit 1
}

Write-Host "✅ React build completed" -ForegroundColor Green

# Get build size
$buildSize = (Get-ChildItem -Path "build" -Recurse | Measure-Object -Property Length -Sum).Sum
$buildSizeMB = [math]::Round($buildSize / 1MB, 2)
Write-Host "Build size: $buildSizeMB MB"

# Step 5: Check if S3 bucket exists, create if not
Write-Host ""
Write-Host "Step 4: Checking S3 bucket..." -ForegroundColor Yellow

try {
    aws s3 ls "s3://$S3_BUCKET" 2>&1 | Out-Null
    Write-Host "✅ Bucket exists: $S3_BUCKET" -ForegroundColor Green
} catch {
    Write-Host "Bucket doesn't exist. Creating..." -ForegroundColor Yellow
    aws s3 mb "s3://$S3_BUCKET" --region $AWS_REGION
    
    # Block public access
    aws s3api put-public-access-block `
        --bucket $S3_BUCKET `
        --public-access-block-configuration `
        "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
    
    Write-Host "✅ Bucket created: $S3_BUCKET" -ForegroundColor Green
}

# Step 6: Upload to S3
Write-Host ""
Write-Host "Step 5: Uploading build to S3..." -ForegroundColor Yellow
aws s3 sync build/ "s3://$S3_BUCKET/$S3_PATH/" `
    --delete `
    --region $AWS_REGION `
    --exclude ".DS_Store" `
    --exclude "*.map"

Write-Host "✅ Upload completed" -ForegroundColor Green

# Step 7: Create versioned backup
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
Write-Host ""
Write-Host "Creating versioned backup..."
aws s3 sync "s3://$S3_BUCKET/$S3_PATH/" "s3://$S3_BUCKET/backups/$TIMESTAMP/" --region $AWS_REGION

Write-Host "✅ Backup created: s3://$S3_BUCKET/backups/$TIMESTAMP/" -ForegroundColor Green

# Step 8: Update Parameter Store
Write-Host ""
Write-Host "Step 6: Updating Parameter Store..." -ForegroundColor Yellow

aws ssm put-parameter `
    --name "/forum/FRONTEND_BUCKET" `
    --value "$S3_BUCKET" `
    --type "String" `
    --overwrite `
    --region $AWS_REGION 2>$null

# Summary
Write-Host ""
Write-Host "===== Deployment Preparation Complete =====" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Frontend is ready for deployment!" -ForegroundColor Green
Write-Host ""
Write-Host "S3 Location: s3://$S3_BUCKET/$S3_PATH/"
Write-Host "Backup: s3://$S3_BUCKET/backups/$TIMESTAMP/"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update your Launch Template user-data script with:"
Write-Host "   FRONTEND_BUCKET_PLACEHOLDER → $S3_BUCKET"
Write-Host ""
Write-Host "2. Run instance refresh to deploy:"
Write-Host "   aws autoscaling start-instance-refresh --auto-scaling-group-name forum-asg"
Write-Host ""
Write-Host "3. Verify deployment:"
Write-Host "   curl https://${API_DOMAIN}/"
Write-Host ""

Pop-Location

