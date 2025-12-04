# Complete CI/CD Pipeline - Eraser.io Simple Description

## System Overview

CI/CD system with two branches: development (testing) and main (testing + deployment).

## Flow

**GITHUB REPOSITORY**
- Contains two branches:
  - development branch (for testing)
  - main branch (for testing and deployment)

**DEVELOPMENT BRANCH FLOW:**
Developer pushes to development branch
  ↓
GitHub Actions: ci-development.yml workflow triggers
  ↓
Run Backend Tests (Django + PostgreSQL)
  ↓
Run Frontend Tests (React + ESLint)
  ↓
Report test results to developer

**MAIN BRANCH FLOW:**
Developer pushes to main branch
  ↓
GitHub Actions: ci-main-deploy.yml workflow triggers
  ↓
PHASE 1: Testing
  ├─ Backend Tests (Django + PostgreSQL)
  └─ Frontend Tests (React + ESLint)
  ↓ (both must pass)
PHASE 2: Build
  ├─ Build Docker image → Push to AWS ECR
  └─ Build React app → Upload to AWS S3
  ↓
PHASE 3: Deploy
  ├─ Update AWS Launch Template
  └─ Trigger AWS Auto Scaling Group refresh
  ↓
AWS DEPLOYMENT
  ├─ EC2 instances pull Docker image from ECR
  ├─ EC2 instances download React build from S3
  └─ New instances replace old ones
  ↓
Production application running

## Components

**GitHub Repository**
- Source code storage
- Two branches: development, main

**GitHub Actions**
- ci-development.yml: Testing workflow for development branch
- ci-main-deploy.yml: Testing + deployment workflow for main branch

**AWS ECR**
- Docker image registry
- Stores backend Docker images

**AWS S3**
- Frontend build storage
- Stores React application builds

**AWS EC2 Auto Scaling Group**
- Manages EC2 instances
- Runs application containers
- Pulls images from ECR
- Downloads builds from S3

