#!/bin/bash
# Script to build React frontend and upload to S3 for EC2 deployment

set -e

echo "===== Frontend Deployment Preparation ====="
echo ""

# Configuration
FRONTEND_DIR="./frontend"
BUILD_DIR="$FRONTEND_DIR/build"
S3_BUCKET="forum-frontend-builds"  # Change this to your bucket name
S3_PATH="latest"
AWS_REGION="eu-central-1"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ Frontend directory not found: $FRONTEND_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Frontend directory found${NC}"

# Step 2: Install dependencies
echo ""
echo "Step 1: Installing npm dependencies..."
cd $FRONTEND_DIR

if [ ! -d "node_modules" ]; then
    echo "Installing packages..."
    npm install
else
    echo "node_modules exists, skipping install (use 'npm ci' to ensure clean install)"
fi

# Step 3: Create production .env file
echo ""
echo "Step 2: Creating production environment file..."

# Get ALB DNS or domain from Parameter Store (or manual input)
echo "Enter your ALB DNS or domain (e.g., api.yourdomain.com or alb-xxx.amazonaws.com):"
read -p "API URL: https://" API_DOMAIN

cat > .env.production << EOF
# Production environment variables
REACT_APP_API_URL=https://${API_DOMAIN}
EOF

echo -e "${GREEN}✅ Created .env.production${NC}"
cat .env.production

# Step 4: Build React app
echo ""
echo "Step 3: Building React application..."
npm run build

if [ ! -d "build" ]; then
    echo -e "${RED}❌ Build failed - build directory not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ React build completed${NC}"
echo "Build size: $(du -sh build | cut -f1)"

# Step 5: Check if S3 bucket exists, create if not
echo ""
echo "Step 4: Checking S3 bucket..."

if aws s3 ls "s3://$S3_BUCKET" 2>&1 | grep -q 'NoSuchBucket'; then
    echo -e "${YELLOW}Bucket doesn't exist. Creating...${NC}"
    aws s3 mb "s3://$S3_BUCKET" --region $AWS_REGION
    
    # Block public access
    aws s3api put-public-access-block \
        --bucket $S3_BUCKET \
        --public-access-block-configuration \
        "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
    
    echo -e "${GREEN}✅ Bucket created: $S3_BUCKET${NC}"
else
    echo -e "${GREEN}✅ Bucket exists: $S3_BUCKET${NC}"
fi

# Step 6: Upload to S3
echo ""
echo "Step 5: Uploading build to S3..."
aws s3 sync build/ "s3://$S3_BUCKET/$S3_PATH/" \
    --delete \
    --region $AWS_REGION \
    --exclude ".DS_Store" \
    --exclude "*.map"

echo -e "${GREEN}✅ Upload completed${NC}"

# Step 7: Create versioned backup (optional)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo ""
echo "Creating versioned backup..."
aws s3 sync "s3://$S3_BUCKET/$S3_PATH/" "s3://$S3_BUCKET/backups/$TIMESTAMP/" --region $AWS_REGION

echo -e "${GREEN}✅ Backup created: s3://$S3_BUCKET/backups/$TIMESTAMP/${NC}"

# Step 8: Update Parameter Store with S3 bucket name
echo ""
echo "Step 6: Updating Parameter Store..."

aws ssm put-parameter \
    --name "/forum/FRONTEND_BUCKET" \
    --value "$S3_BUCKET" \
    --type "String" \
    --overwrite \
    --region $AWS_REGION 2>/dev/null || echo "Parameter Store update skipped"

# Summary
echo ""
echo "===== Deployment Preparation Complete ====="
echo ""
echo -e "${GREEN}Frontend is ready for deployment!${NC}"
echo ""
echo "S3 Location: s3://$S3_BUCKET/$S3_PATH/"
echo "Backup: s3://$S3_BUCKET/backups/$TIMESTAMP/"
echo ""
echo "Next steps:"
echo "1. Update your Launch Template user-data script with:"
echo "   FRONTEND_BUCKET_PLACEHOLDER → $S3_BUCKET"
echo ""
echo "2. Or run instance refresh to deploy:"
echo "   aws autoscaling start-instance-refresh --auto-scaling-group-name forum-asg"
echo ""
echo "3. Verify deployment:"
echo "   curl https://${API_DOMAIN}/"
echo ""

cd - > /dev/null



