# CI/CD Architecture Description for Eraser.io

## System Overview

A comprehensive CI/CD pipeline for a full-stack web application deployed on AWS infrastructure. The system uses GitHub Actions for automation, AWS services for deployment, and implements secure authentication via OIDC.

## Components

### Source Control
- GitHub Repository with two main branches: development and main
- Development branch: automated testing only
- Main branch: automated testing + deployment

### CI/CD Platform
- GitHub Actions workflows
- Two workflows: ci-development.yml (testing) and ci-main-deploy.yml (testing + deployment)

### Testing Infrastructure
- PostgreSQL 15 service container for backend tests
- Django test framework for backend validation
- ESLint for frontend code quality
- flake8 for Python linting

### Build Services
- Docker for containerizing Django backend
- npm for building React frontend
- AWS ECR (Elastic Container Registry) for storing Docker images
- AWS S3 (Simple Storage Service) for storing React build artifacts

### Deployment Infrastructure
- AWS EC2 Auto Scaling Group (ASG) for compute instances
- AWS Launch Template for EC2 instance configuration
- AWS Application Load Balancer (ALB) for traffic distribution
- AWS Systems Manager Parameter Store for configuration management

### Security
- AWS IAM (Identity and Access Management)
- AWS OIDC (OpenID Connect) provider for GitHub Actions authentication
- IAM Role: GitHubActionsRole with permissions for ECR, S3, EC2, Auto Scaling, and Systems Manager

## Data Flow

### Development Branch Flow
1. Developer pushes code to development branch
2. GitHub Actions triggers ci-development.yml workflow
3. Backend tests run with PostgreSQL service container
4. Frontend tests run with ESLint validation
5. Results reported back to GitHub

### Main Branch Flow (Full CI/CD)
1. Developer pushes code to main branch or merges PR
2. GitHub Actions triggers ci-main-deploy.yml workflow
3. Phase 1: Run backend and frontend tests (must pass)
4. Phase 2: Build Docker image and push to ECR, build React app and upload to S3
5. Phase 3: Update Launch Template with new Docker image tag
6. Phase 4: Trigger ASG Instance Refresh for zero-downtime deployment
7. New EC2 instances launch with updated Docker image and frontend from S3
8. Old instances terminate after new instances are healthy

## Authentication Flow
1. GitHub Actions requests OIDC token from GitHub
2. GitHub Actions assumes IAM role using OIDC token
3. AWS validates token against OIDC provider
4. IAM role grants temporary credentials
5. GitHub Actions uses credentials to access AWS services

## Key Features
- Automated testing before deployment
- Containerized backend deployment
- Static frontend hosting on S3
- Zero-downtime rolling deployment
- Secure authentication without static keys
- Versioned Docker images using commit SHA
- Infrastructure as code via Launch Templates

## Workflow Dependencies
- Test jobs run in parallel
- Build jobs depend on test jobs passing
- Launch Template update depends on successful builds
- Deployment depends on Launch Template update
- All jobs use AWS OIDC for authentication

## Deployment Strategy
- Rolling deployment via ASG Instance Refresh
- Minimum healthy percentage: 50%
- Instance warmup: 60 seconds
- New instances pull latest Docker image from ECR
- New instances download frontend build from S3
- Old instances terminate after new instances are verified healthy


