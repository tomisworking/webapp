# Complete CI/CD Pipeline Diagram - For Eraser.io

## System Overview

Complete CI/CD architecture showing two parallel workflows: development branch (testing only) and main branch (testing + deployment to AWS).

## Flow Diagram Description

### Top Level: GitHub Repository

**GitHub Repository** contains two branches:
- **development branch**: Used for testing code changes
- **main branch**: Used for testing and production deployment

### Middle Level: GitHub Actions

**GitHub Actions** platform runs two separate workflows:

**Workflow 1: ci-development.yml**
- Triggered by: push or pull request to development branch
- Actions:
  - Test Backend (Django + PostgreSQL service container)
  - Test Frontend (React + ESLint validation)
- Result: Test reports only, no deployment

**Workflow 2: ci-main-deploy.yml**
- Triggered by: push or pull request to main branch
- Phase 1: Testing
  - Test Backend (Django + PostgreSQL)
  - Test Frontend (React + ESLint)
- Phase 2: Build
  - Build Docker image → Push to AWS ECR
  - Build React application → Upload to AWS S3
- Phase 3: Deploy
  - Update AWS Launch Template with new image tag
  - Trigger AWS Auto Scaling Group Instance Refresh
- Result: Code deployed to production

### Bottom Level: AWS Cloud

**AWS Cloud** contains three services:

**AWS ECR (Elastic Container Registry)**
- Stores Docker images
- Receives images from GitHub Actions workflow
- EC2 instances pull images from here

**AWS S3 (Simple Storage Service)**
- Stores React frontend builds
- Receives builds from GitHub Actions workflow
- EC2 instances download builds from here

**AWS EC2 Auto Scaling Group (ASG)**
- Manages EC2 instances running the application
- Receives deployment commands from GitHub Actions
- Pulls Docker images from ECR
- Downloads frontend builds from S3
- Serves application to users via Application Load Balancer

## Connection Flow

1. **Developer** pushes code to GitHub Repository (development or main branch)
2. **GitHub Repository** triggers appropriate GitHub Actions workflow
3. **GitHub Actions** executes workflow steps:
   - For development: runs tests only
   - For main: runs tests → builds artifacts → deploys to AWS
4. **AWS Services** receive artifacts:
   - ECR receives Docker images
   - S3 receives frontend builds
   - ASG receives deployment commands
5. **EC2 Instances** (managed by ASG) pull latest code and serve application

## Visual Layout

```
GitHub Repository (top)
  ├─ development branch
  └─ main branch
      ↓
GitHub Actions (middle)
  ├─ ci-development.yml workflow (left side)
  └─ ci-main-deploy.yml workflow (right side)
      ↓
AWS Cloud (bottom)
  ├─ ECR (left)
  ├─ S3 (center)
  └─ EC2 ASG (right)
```

## Key Visual Elements

- **Boxes**: Each major component (Repository, Actions, AWS) should be in separate boxes
- **Arrows**: Show flow from Repository → Actions → AWS
- **Branches**: Show two parallel paths (development and main) splitting from Repository
- **Workflows**: Show two workflow boxes side by side in GitHub Actions section
- **AWS Services**: Show three service boxes side by side in AWS section
- **Labels**: Each box should have clear labels indicating its purpose

