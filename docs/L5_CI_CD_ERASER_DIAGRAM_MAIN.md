# CI/CD Pipeline - Main Branch

## System Overview

Complete CI/CD pipeline from code commit to production deployment on AWS. Includes testing, building, and zero-downtime deployment.

## Components

### Source Control
- GitHub Repository
- Branch: main

### CI/CD Platform
- GitHub Actions
- Workflow: ci-main-deploy.yml

### Testing
- PostgreSQL service container
- Django tests
- React build test
- ESLint validation

### Build
- Docker for backend
- npm for frontend
- AWS ECR for Docker images
- AWS S3 for frontend builds

### Deployment
- AWS EC2 Auto Scaling Group
- AWS Launch Template
- AWS Application Load Balancer

### Security
- AWS OIDC authentication
- IAM Role: GitHubActionsRole

## Flow

1. Developer pushes code to main branch
2. GitHub Actions triggers workflow
3. Phase 1: Run tests (backend + frontend)
4. Phase 2: Build Docker image → push to ECR
5. Phase 2: Build React app → upload to S3
6. Phase 3: Update Launch Template
7. Phase 4: Deploy via ASG Instance Refresh
8. New EC2 instances launch with updated code
9. Old instances terminate after new ones are healthy

## Authentication
- GitHub Actions → OIDC token → AWS IAM Role → AWS Services

## Key Points
- Zero-downtime deployment
- Rolling deployment strategy
- Automated testing before deployment
- Secure OIDC authentication
- Versioned Docker images
