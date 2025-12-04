# L5 - Proces CI/CD - Sprawozdanie

## 📋 Informacje podstawowe

**Projekt:** Forum Application - Full Stack Web Application  
**Autor:** [Twoje imię]  
**Data:** [Data]  
**Laboratorium:** L5 - Proces CI/CD

---

## 1. Wprowadzenie

### 1.1. Cel laboratorium

Celem laboratorium było zaprojektowanie i wdrożenie kompleksowego procesu CI/CD (Continuous Integration / Continuous Deployment) dla aplikacji webowej Forum, składającej się z:
- **Backend:** Django REST Framework (Python)
- **Frontend:** React (JavaScript)
- **Infrastruktura:** AWS (EC2, ECR, S3, ASG, ALB, RDS)

### 1.2. Zakres projektu

Proces CI/CD obejmuje:
- ✅ Automatyczne testy aplikacji (backend i frontend)
- ✅ Budowanie i publikowanie obrazów Docker do AWS ECR
- ✅ Budowanie i publikowanie frontendu do AWS S3
- ✅ Automatyczny deployment na infrastrukturę AWS
- ✅ Integracja z GitHub Actions
- ✅ Uwierzytelnianie przez AWS OIDC (bez statycznych kluczy)

---

## 2. Architektura CI/CD

### 2.1. Ogólny przepływ

```
┌─────────────────────────────────────────────────────────────┐
│                    GITHUB REPOSITORY                        │
│  • Branch: development (testy)                               │
│  • Branch: main (testy + deployment)                         │
└───────────────────────┬─────────────────────────────────────┘
                        │ Push / Pull Request
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                  GITHUB ACTIONS                              │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  WORKFLOW: ci-development.yml                           │ │
│  │  Trigger: push/PR → development                        │ │
│  │  • Test Backend (Django + PostgreSQL)                  │ │
│  │  • Test Frontend (React + ESLint)                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  WORKFLOW: ci-main-deploy.yml                           │ │
│  │  Trigger: push/PR → main                               │ │
│  │  1. Test Backend                                        │ │
│  │  2. Test Frontend                                       │ │
│  │  3. Build & Push Docker → ECR                         │ │
│  │  4. Build & Upload Frontend → S3                       │ │
│  │  5. Update Launch Template                            │ │
│  │  6. Deploy (ASG Instance Refresh)                      │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                      AWS CLOUD                               │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  ECR         │  │  S3           │  │  EC2 ASG     │    │
│  │  (Docker)    │  │  (Frontend)   │  │  (Instances) │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2. Strategia branchy

#### Branch: `development`
- **Cel:** Testowanie zmian przed merge do main
- **Workflow:** `ci-development.yml`
- **Akcje:**
  - Automatyczne testy backend (Django + PostgreSQL)
  - Automatyczne testy frontend (React + ESLint)
  - **Brak deploymentu** - tylko walidacja kodu

#### Branch: `main`
- **Cel:** Produkcja - automatyczny deployment
- **Workflow:** `ci-main-deploy.yml`
- **Akcje:**
  - Wszystkie testy (jak w development)
  - Build i push Docker image do ECR
  - Build i upload frontend do S3
  - Aktualizacja Launch Template
  - Automatyczny deployment (ASG Instance Refresh)

---

## 3. Szczegółowa implementacja

### 3.1. Workflow: Development (ci-development.yml)

**Trigger:**
- Push do brancha `development`
- Pull Request do brancha `development`

**Jobs:**

#### Job 1: Test Backend
```yaml
- Uruchomienie PostgreSQL (service container)
- Instalacja zależności Python
- Migracje bazy danych
- Sprawdzenie kodu (Django check)
- Linting (flake8)
- Uruchomienie testów jednostkowych
```

#### Job 2: Test Frontend
```yaml
- Instalacja Node.js 18
- Instalacja zależności (npm ci)
- Sprawdzenie kodu (ESLint przez build)
- Build aplikacji React (test)
```

**Czas wykonania:** ~3-5 minut

---

### 3.2. Workflow: Main - Deployment (ci-main-deploy.yml)

**Trigger:**
- Push do brancha `main`
- Pull Request do brancha `main`
- Merge group events

**Jobs:**

#### Job 1-2: Testy (jak w development)
- Test Backend
- Test Frontend
- **Warunek:** Muszą przejść przed deploymentem

#### Job 3: Build & Push Backend to ECR
```yaml
- Konfiguracja AWS credentials (OIDC)
- Logowanie do Amazon ECR
- Build Docker image
- Tag obrazu (SHA commit)
- Push do ECR repository
```

**Technologie:**
- Docker
- AWS ECR (Elastic Container Registry)
- AWS OIDC (OpenID Connect) dla bezpiecznego uwierzytelniania

#### Job 4: Build & Upload Frontend to S3
```yaml
- Konfiguracja AWS credentials (OIDC)
- Pobranie ALB DNS z Parameter Store
- Utworzenie .env.production
- Build aplikacji React
- Sprawdzenie czy S3 bucket istnieje
- Usunięcie poprzedniego builda
- Upload nowego builda do S3
- Utworzenie backupu
```

**Technologie:**
- Node.js / npm
- AWS S3 (Simple Storage Service)
- AWS Systems Manager Parameter Store

#### Job 5: Update Launch Template
```yaml
- Pobranie najnowszej wersji Launch Template
- Pobranie user-data z obecnej wersji
- Aktualizacja user-data z nowym ECR URI i tagiem
- Utworzenie nowej wersji Launch Template
```

**Cel:** Zapewnienie, że nowe instancje EC2 będą używać najnowszego obrazu Docker

#### Job 6: Deploy (ASG Instance Refresh)
```yaml
- Sprawdzenie czy Instance Refresh już działa
- Uruchomienie Instance Refresh w Auto Scaling Group
- Konfiguracja:
  - MinHealthyPercentage: 50%
  - InstanceWarmup: 60 sekund
  - SkipMatching: false
```

**Efekt:** 
- Stopniowa wymiana instancji EC2
- Nowe instancje używają najnowszego obrazu z ECR
- Zero-downtime deployment

#### Job 7: Notify (Status)
```yaml
- Sprawdzenie statusu deploymentu
- Wyświetlenie informacji o deployed resources
```

**Czas wykonania:** ~10-15 minut (w zależności od build time)

---

## 4. Bezpieczeństwo i uwierzytelnianie

### 4.1. AWS OIDC (OpenID Connect)

**Problem:** Statyczne klucze AWS (Access Keys) są niebezpieczne i wymagają rotacji.

**Rozwiązanie:** Użycie AWS OIDC dla bezpośredniego uwierzytelniania GitHub Actions w AWS.

**Konfiguracja:**

1. **Identity Provider w AWS IAM:**
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`

2. **IAM Role:**
   - Nazwa: `GitHubActionsRole`
   - Trust Policy: Ogranicza dostęp do konkretnego repozytorium
   - Permissions: ECR, S3, EC2, Auto Scaling, Systems Manager

3. **Workflow Configuration:**
   ```yaml
   permissions:
     id-token: write   # Wymagane dla OIDC
     contents: read
   
   - name: Configure AWS credentials
     uses: aws-actions/configure-aws-credentials@v4
     with:
       role-to-assume: arn:aws:iam::ACCOUNT_ID:role/GitHubActionsRole
       aws-region: us-east-1
   ```

**Zalety:**
- ✅ Brak statycznych kluczy
- ✅ Automatyczna rotacja tokenów
- ✅ Granularne uprawnienia
- ✅ Bezpieczniejsze niż Access Keys

---

## 5. Technologie i narzędzia

### 5.1. CI/CD Platform
- **GitHub Actions** - platforma CI/CD
- **YAML workflows** - definicja procesów

### 5.2. Testowanie
- **PostgreSQL 15** - baza danych testowa (service container)
- **Django Test Framework** - testy backend
- **ESLint** - linting frontend
- **flake8** - linting backend

### 5.3. Build i Deployment
- **Docker** - konteneryzacja backend
- **npm** - build frontend
- **AWS ECR** - Docker registry
- **AWS S3** - storage dla frontend build
- **AWS EC2 Auto Scaling Group** - infrastruktura obliczeniowa
- **AWS Launch Template** - konfiguracja instancji EC2

### 5.4. Konfiguracja i zarządzanie
- **AWS Systems Manager Parameter Store** - przechowywanie konfiguracji
- **AWS IAM** - zarządzanie dostępem
- **AWS OIDC** - bezpieczne uwierzytelnianie

---

## 6. Przepływ danych i procesów

### 6.1. Development Branch Flow

```
Developer → Push do development
    ↓
GitHub Actions uruchamia ci-development.yml
    ↓
┌─────────────────────────────────────┐
│  Test Backend                       │
│  • PostgreSQL service               │
│  • Migracje                         │
│  • Django check                     │
│  • flake8                           │
│  • Unit tests                       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Test Frontend                      │
│  • npm ci                           │
│  • ESLint (przez build)            │
│  • Build test                       │
└─────────────────────────────────────┘
    ↓
Status: ✅ Pass / ❌ Fail
```

### 6.2. Main Branch Flow (Full CI/CD)

```
Developer → Push do main / Merge PR
    ↓
GitHub Actions uruchamia ci-main-deploy.yml
    ↓
┌─────────────────────────────────────┐
│  PHASE 1: Testy                     │
│  • Test Backend                     │
│  • Test Frontend                    │
└──────────────┬──────────────────────┘
               │ ✅ Pass
               ↓
┌─────────────────────────────────────┐
│  PHASE 2: Build                     │
│  • Build Docker → ECR               │
│  • Build React → S3                 │
└──────────────┬──────────────────────┘
               │ ✅ Success
               ↓
┌─────────────────────────────────────┐
│  PHASE 3: Update Infrastructure    │
│  • Update Launch Template           │
└──────────────┬──────────────────────┘
               │ ✅ Success
               ↓
┌─────────────────────────────────────┐
│  PHASE 4: Deploy                    │
│  • ASG Instance Refresh             │
│  • Rolling deployment               │
│  • Zero-downtime                    │
└─────────────────────────────────────┘
    ↓
✅ Deployment Complete
```

---

## 7. Kluczowe funkcjonalności

### 7.1. Automatyczne testy
- ✅ Testy backend z rzeczywistą bazą PostgreSQL
- ✅ Testy frontend z weryfikacją build
- ✅ Linting kodu (flake8, ESLint)
- ✅ Sprawdzanie poprawności konfiguracji Django

### 7.2. Automatyczny build
- ✅ Build Docker image z tagiem SHA commit
- ✅ Build React aplikacji z production config
- ✅ Automatyczne tagowanie i wersjonowanie

### 7.3. Automatyczny deployment
- ✅ Push do ECR (Docker registry)
- ✅ Upload do S3 (frontend storage)
- ✅ Aktualizacja Launch Template
- ✅ Rolling deployment przez ASG Instance Refresh
- ✅ Zero-downtime deployment

### 7.4. Monitoring i notyfikacje
- ✅ Status deploymentu w GitHub Actions
- ✅ Logi wszystkich kroków
- ✅ Informacje o deployed resources

---

## 8. Metryki i wydajność

### 8.1. Czas wykonania workflow

| Workflow | Średni czas | Maksymalny czas |
|----------|-------------|-----------------|
| ci-development.yml | 3-5 min | 8 min |
| ci-main-deploy.yml | 10-15 min | 20 min |

### 8.2. Koszty

**GitHub Actions:**
- 2000 minut/miesiąc w Free Tier
- Nasze workflow: ~15 min/deployment
- **Oszacowanie:** ~130 deploymentów/miesiąc w Free Tier

**AWS:**
- ECR: $0.10/GB storage/miesiąc
- S3: $0.023/GB storage/miesiąc
- **Oszacowanie:** <$1/miesiąc dla małej aplikacji

---

## 9. Wnioski i podsumowanie

### 9.1. Osiągnięcia

✅ **Kompletny proces CI/CD** - od commita do deploymentu  
✅ **Automatyzacja** - zero manualnych kroków  
✅ **Bezpieczeństwo** - OIDC zamiast statycznych kluczy  
✅ **Zero-downtime deployment** - przez ASG Instance Refresh  
✅ **Testowanie** - automatyczne testy przed deploymentem  
✅ **Wersjonowanie** - tagowanie obrazów Docker SHA commit  

### 9.2. Wyzwania i rozwiązania

**Wyzwanie 1:** Immutable tags w ECR  
**Rozwiązanie:** Użycie tagów SHA commit zamiast `latest`

**Wyzwanie 2:** Bezpieczne uwierzytelnianie  
**Rozwiązanie:** Implementacja AWS OIDC

**Wyzwanie 3:** Zero-downtime deployment  
**Rozwiązanie:** ASG Instance Refresh z MinHealthyPercentage

### 9.3. Możliwości rozbudowy

- [ ] Dodanie testów end-to-end (E2E)
- [ ] Integracja z monitoringiem (CloudWatch)
- [ ] Automatyczne rollback w przypadku błędów
- [ ] Multi-environment (dev, staging, prod)
- [ ] Blue-Green deployment
- [ ] Canary deployments

---

## 10. Załączniki

### 10.1. Pliki workflow
- `.github/workflows/ci-development.yml` - Workflow dla brancha development
- `.github/workflows/ci-main-deploy.yml` - Workflow dla brancha main (z deploymentem)

### 10.2. Dokumentacja
- `docs/CI_CD_GUIDE.md` - Przewodnik po CI/CD
- `docs/AWS_OIDC_SETUP.md` - Instrukcja konfiguracji OIDC

### 10.3. Konfiguracja AWS
- IAM Role: `GitHubActionsRole`
- ECR Repository: `forum-backend`
- S3 Bucket: `forum-frontend-builds-kongoapp`
- ASG: `forum-asg`
- Launch Template: `forum-lt`

---

**Data utworzenia:** [Data]  
**Ostatnia aktualizacja:** [Data]  
**Status:** ✅ Kompletne


