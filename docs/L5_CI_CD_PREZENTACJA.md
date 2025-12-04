# L5 - Proces CI/CD - Prezentacja Implementacji

## 🎯 Slajd 1: Wprowadzenie

### CI/CD dla Forum Application

**Projekt:** Full-stack web application  
**Stack technologiczny:**
- Backend: Django REST Framework (Python)
- Frontend: React (JavaScript)
- Infrastruktura: AWS (EC2, ECR, S3, ASG, ALB, RDS)

**Cel:** Automatyzacja procesu testowania, budowania i wdrażania aplikacji

---

## 🏗️ Slajd 2: Architektura CI/CD

### Strategia Branchy

```
┌─────────────────────────────────────────┐
│  Branch: development                    │
│  • Automatyczne testy                   │
│  • Brak deploymentu                    │
│  • Workflow: ci-development.yml        │
└─────────────────────────────────────────┘
              ↓ Merge
┌─────────────────────────────────────────┐
│  Branch: main                          │
│  • Testy + Deployment                  │
│  • Build → ECR + S3                    │
│  • ASG Instance Refresh                │
│  • Workflow: ci-main-deploy.yml        │
└─────────────────────────────────────────┘
```

---

## 🔄 Slajd 3: Przepływ CI/CD - Development

### Workflow: ci-development.yml

```
Push do development
    ↓
┌──────────────────────────────┐
│  Test Backend                 │
│  • PostgreSQL service         │
│  • Migracje                   │
│  • Django check               │
│  • flake8 linting             │
│  • Unit tests                 │
└──────────────────────────────┘
    ↓
┌──────────────────────────────┐
│  Test Frontend               │
│  • npm ci                    │
│  • ESLint (przez build)     │
│  • Build test                │
└──────────────────────────────┘
    ↓
✅ Status: Pass / ❌ Fail
```

**Czas:** ~3-5 minut

---

## 🚀 Slajd 4: Przepływ CI/CD - Main (Deployment)

### Workflow: ci-main-deploy.yml

```
Push do main
    ↓
PHASE 1: Testy (Backend + Frontend)
    ↓ ✅
PHASE 2: Build
    • Docker → ECR
    • React → S3
    ↓ ✅
PHASE 3: Update Infrastructure
    • Launch Template update
    ↓ ✅
PHASE 4: Deploy
    • ASG Instance Refresh
    • Zero-downtime
    ↓
✅ Deployment Complete
```

**Czas:** ~10-15 minut

---

## 🔐 Slajd 5: Bezpieczeństwo - AWS OIDC

### Problem: Statyczne klucze AWS

**Tradycyjne podejście:**
- ❌ Access Keys w GitHub Secrets
- ❌ Wymagają rotacji
- ❌ Ryzyko wycieku

**Nasze rozwiązanie: AWS OIDC**

```
GitHub Actions
    ↓ OIDC Token
AWS Identity Provider
    ↓ Assume Role
IAM Role (GitHubActionsRole)
    ↓
AWS Services (ECR, S3, EC2)
```

**Zalety:**
- ✅ Brak statycznych kluczy
- ✅ Automatyczna rotacja
- ✅ Granularne uprawnienia
- ✅ Bezpieczniejsze

---

## 🛠️ Slajd 6: Technologie

### Stack technologiczny CI/CD

**Platforma CI/CD:**
- GitHub Actions

**Testowanie:**
- PostgreSQL 15 (service container)
- Django Test Framework
- ESLint
- flake8

**Build & Deploy:**
- Docker
- AWS ECR
- AWS S3
- AWS EC2 Auto Scaling Group
- AWS Launch Template

**Konfiguracja:**
- AWS Systems Manager Parameter Store
- AWS IAM + OIDC

---

## 📊 Slajd 7: Kluczowe funkcjonalności

### ✅ Automatyczne testy
- Backend z PostgreSQL
- Frontend z ESLint
- Linting kodu

### ✅ Automatyczny build
- Docker image → ECR
- React build → S3
- Tagowanie (SHA commit)

### ✅ Automatyczny deployment
- Zero-downtime
- Rolling deployment
- ASG Instance Refresh

### ✅ Monitoring
- Status w GitHub Actions
- Logi wszystkich kroków

---

## 📈 Slajd 8: Metryki

### Wydajność

| Workflow | Czas wykonania |
|----------|----------------|
| Development (testy) | 3-5 min |
| Main (testy + deploy) | 10-15 min |

### Koszty

**GitHub Actions:**
- 2000 min/miesiąc Free Tier
- ~130 deploymentów/miesiąc

**AWS:**
- ECR: <$1/miesiąc
- S3: <$1/miesiąc

---

## 🎯 Slajd 9: Osiągnięcia

### ✅ Co zostało zrealizowane

1. **Kompletny proces CI/CD**
   - Od commita do deploymentu
   - Zero manualnych kroków

2. **Bezpieczeństwo**
   - AWS OIDC zamiast statycznych kluczy
   - Granularne uprawnienia

3. **Zero-downtime deployment**
   - ASG Instance Refresh
   - Rolling deployment

4. **Automatyczne testy**
   - Backend + Frontend
   - Przed każdym deploymentem

---

## 🔮 Slajd 10: Możliwości rozbudowy

### Przyszłe ulepszenia

- [ ] Testy end-to-end (E2E)
- [ ] Integracja z CloudWatch
- [ ] Automatyczny rollback
- [ ] Multi-environment (dev/staging/prod)
- [ ] Blue-Green deployment
- [ ] Canary deployments

---

## 📝 Slajd 11: Podsumowanie

### Kluczowe punkty

1. **Automatyzacja** - pełny proces CI/CD
2. **Bezpieczeństwo** - AWS OIDC
3. **Zero-downtime** - ASG Instance Refresh
4. **Testowanie** - automatyczne przed deploymentem
5. **Skalowalność** - gotowe do rozbudowy

### Rezultat

✅ **Produkcyjny proces CI/CD** gotowy do użycia

---

## 📚 Slajd 12: Dokumentacja

### Pliki projektu

- `.github/workflows/ci-development.yml`
- `.github/workflows/ci-main-deploy.yml`
- `docs/CI_CD_GUIDE.md`
- `docs/AWS_OIDC_SETUP.md`

### Konfiguracja AWS

- IAM Role: `GitHubActionsRole`
- ECR: `forum-backend`
- S3: `forum-frontend-builds-kongoapp`
- ASG: `forum-asg`

---

**Dziękuję za uwagę!**


