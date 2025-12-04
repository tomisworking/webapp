# CI/CD Pipeline - Development Branch

## System Overview

Automated testing pipeline for development branch. Tests code quality and functionality before merging to main.

## Components

### Source Control
- GitHub Repository
- Branch: development

### CI/CD Platform
- GitHub Actions
- Workflow: ci-development.yml

### Testing
- PostgreSQL service container
- Django tests
- React build test
- ESLint validation
- flake8 linting

## Flow

1. Developer pushes code to development branch
2. GitHub Actions triggers workflow
3. Backend tests run (PostgreSQL, Django, flake8)
4. Frontend tests run (ESLint, build)
5. Results reported to GitHub

## Key Points
- Testing only, no deployment
- Parallel test execution
- Fast feedback (3-5 minutes)
- Gate before merge to main
