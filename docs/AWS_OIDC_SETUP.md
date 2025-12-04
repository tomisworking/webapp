# 🔐 AWS OIDC Setup dla GitHub Actions

## 📋 Przegląd

OIDC (OpenID Connect) pozwala GitHub Actions na bezpośrednie uwierzytelnianie w AWS bez przechowywania statycznych kluczy dostępu. To bardziej bezpieczne rozwiązanie niż Access Keys.

### Zalety OIDC:
- ✅ **Brak statycznych kluczy** - nie musisz przechowywać Access Keys
- ✅ **Automatyczne rotowanie** - AWS zarządza tokenami
- ✅ **Lepsze bezpieczeństwo** - tokeny są tymczasowe
- ✅ **Granularne uprawnienia** - możesz ograniczyć dostęp do konkretnych repozytoriów/branchy

---

## 🎯 Krok 1: Utwórz Identity Provider w AWS

### 1.1. Przejdź do IAM w AWS Console

1. AWS Console → Wyszukaj: **IAM**
2. W lewym menu kliknij: **Identity providers**
3. Kliknij: **Add provider**

### 1.2. Konfiguracja Provider

**Provider type:**
- Wybierz: **OpenID Connect**

**Provider URL:**
```
https://token.actions.githubusercontent.com
```

**Audience:**
```
sts.amazonaws.com
```

**Description (opcjonalne):**
```
GitHub Actions OIDC Provider
```

4. Kliknij: **Add provider**

**💾 ZAPISZ Provider ARN** (będzie potrzebny w następnym kroku)

Przykład ARN:
```
arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com
```

---

## 🎯 Krok 2: Utwórz IAM Role dla GitHub Actions

### 2.1. Przejdź do Roles

1. IAM → **Roles** (w lewym menu)
2. Kliknij: **Create role**

### 2.2. Trust Policy (kto może używać roli)

**Trusted entity type:**
- Wybierz: **Web identity**

**Identity provider:**
- Wybierz: `token.actions.githubusercontent.com` (ten który właśnie utworzyłeś)

**Audience:**
- Powinno być automatycznie: `sts.amazonaws.com`

Kliknij: **Next**

### 2.3. Warunki (Conditions) - WAŻNE!

**Dodaj warunki, żeby tylko Twój repozytorium mógł używać roli:**

Kliknij: **Add condition**

**Condition 1: Repository**
- **Condition key:** `token.actions.githubusercontent.com:sub`
- **Operator:** `StringEquals`
- **Value:** `repo:TOMEK_USERNAME/WEBAPP_REPO_NAME:*`
  - Zamień `TOMEK_USERNAME` na Twoją nazwę użytkownika GitHub
  - Zamień `WEBAPP_REPO_NAME` na nazwę repozytorium

Przykład:
```
repo:tomisworking/webapp:*
```

**Condition 2: Branch (opcjonalne, ale zalecane)**
- **Condition key:** `token.actions.githubusercontent.com:ref`
- **Operator:** `StringLike`
- **Value:** `refs/heads/main` lub `refs/heads/development`

**LUB dla wielu branchy:**
```
refs/heads/main
refs/heads/development
```

Kliknij: **Next**

### 2.4. Permissions (Uprawnienia)

**Dodaj uprawnienia potrzebne dla CI/CD:**

Kliknij: **Create policy** (custom policy) lub użyj istniejących:

**Potrzebne uprawnienia:**
- ECR (Elastic Container Registry)
- S3
- EC2 (Auto Scaling, Launch Templates)
- Systems Manager (Parameter Store)

**Przykładowa polityka (JSON):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::forum-frontend-builds",
        "arn:aws:s3:::forum-frontend-builds/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeLaunchTemplates",
        "ec2:DescribeLaunchTemplateVersions",
        "ec2:CreateLaunchTemplateVersion",
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeInstanceRefreshes",
        "autoscaling:StartInstanceRefresh"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters"
      ],
      "Resource": "arn:aws:ssm:eu-central-1:*:parameter/forum/*"
    }
  ]
}
```

**LUB użyj gotowych AWS Managed Policies:**
- `AmazonEC2ContainerRegistryFullAccess` (ECR)
- `AmazonS3FullAccess` (S3) - lub bardziej restrykcyjna
- `AmazonEC2FullAccess` (EC2, Auto Scaling)
- `AmazonSSMReadOnlyAccess` (Parameter Store)

Kliknij: **Next**

### 2.5. Role Details

**Role name:**
```
GitHubActionsRole
```

**Description:**
```
Role for GitHub Actions to deploy to AWS
```

Kliknij: **Create role**

**💾 ZAPISZ Role ARN** (będzie potrzebny w workflow)

Przykład ARN:
```
arn:aws:iam::123456789012:role/GitHubActionsRole
```

---

## 🎯 Krok 3: Zaktualizuj GitHub Actions Workflow

### 3.1. Zmień konfigurację AWS credentials

W pliku `.github/workflows/ci-main-deploy.yml`:

**PRZED (ze statycznymi kluczami):**
```yaml
- name: Konfiguruj AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: ${{ env.AWS_REGION }}
```

**PO ZMIANIE (z OIDC):**
```yaml
- name: Konfiguruj AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::ACCOUNT_ID:role/GitHubActionsRole
    aws-region: ${{ env.AWS_REGION }}
```

**Gdzie:**
- `ACCOUNT_ID` = Twój AWS Account ID (12 cyfr)
- `GitHubActionsRole` = Nazwa roli którą utworzyłeś

### 3.2. Dodaj permissions do workflow

Na początku pliku workflow, dodaj:

```yaml
name: CI/CD - Main (Testy + Deployment)

on:
  push:
    branches: [ main ]
  # ...

permissions:
  id-token: write   # Wymagane dla OIDC
  contents: read    # Wymagane do checkout kodu

jobs:
  # ...
```

---

## 🎯 Krok 4: Usuń sekrety AWS z GitHub (opcjonalne)

Jeśli używasz OIDC, nie potrzebujesz już sekretów:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Możesz je usunąć z GitHub Secrets (Settings → Secrets and variables → Actions)

---

## 📋 Checklist konfiguracji

### AWS:
- [ ] Identity Provider utworzony (`token.actions.githubusercontent.com`)
- [ ] IAM Role utworzona (`GitHubActionsRole`)
- [ ] Trust Policy skonfigurowana z warunkami (repo, branch)
- [ ] Permissions Policy dodana (ECR, S3, EC2, SSM)
- [ ] Role ARN zapisany

### GitHub:
- [ ] Workflow zaktualizowany (używa `role-to-assume`)
- [ ] Permissions dodane (`id-token: write`)
- [ ] Stare sekrety usunięte (opcjonalnie)

---

## 🔍 Jak znaleźć AWS Account ID

### Metoda 1: AWS Console
1. Kliknij na swoją nazwę użytkownika (prawy górny róg)
2. Account ID jest wyświetlony

### Metoda 2: AWS CLI
```bash
aws sts get-caller-identity --query Account --output text
```

### Metoda 3: Z ARN
ARN ma format: `arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME`
- `ACCOUNT_ID` to 12 cyfr w środku

---

## 🎯 Przykładowa konfiguracja Trust Policy

Pełna Trust Policy dla roli (możesz skopiować i dostosować):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:TOMEK_USERNAME/WEBAPP_REPO_NAME:*"
        }
      }
    }
  ]
}
```

**Dla konkretnych branchy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": [
            "repo:TOMEK_USERNAME/WEBAPP_REPO_NAME:ref:refs/heads/main",
            "repo:TOMEK_USERNAME/WEBAPP_REPO_NAME:ref:refs/heads/development"
          ]
        }
      }
    }
  ]
}
```

---

## 🔧 Aktualizacja workflow - pełny przykład

### Przed (ze statycznymi kluczami):

```yaml
name: CI/CD - Main

on:
  push:
    branches: [ main ]

jobs:
  build-and-push-backend:
    steps:
      - name: Konfiguruj AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-central-1
```

### Po (z OIDC):

```yaml
name: CI/CD - Main

on:
  push:
    branches: [ main ]

permissions:
  id-token: write
  contents: read

jobs:
  build-and-push-backend:
    steps:
      - name: Konfiguruj AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: eu-central-1
```

---

## 🧪 Testowanie

### 1. Push do main

```bash
git checkout main
git commit --allow-empty -m "Test OIDC authentication"
git push origin main
```

### 2. Sprawdź workflow

GitHub Actions → Sprawdź czy workflow przechodzi

### 3. Sprawdź logi

W logach workflow powinieneś zobaczyć:
```
Successfully assumed role: arn:aws:iam::123456789012:role/GitHubActionsRole
```

---

## 🐛 Troubleshooting

### Problem: "Not authorized to perform sts:AssumeRoleWithWebIdentity"

**Przyczyna:** Trust Policy nie pozwala na assume role

**Rozwiązanie:**
- Sprawdź Trust Policy roli
- Upewnij się, że `sub` condition pasuje do Twojego repo
- Sprawdź czy Identity Provider jest poprawnie skonfigurowany

### Problem: "Access Denied" przy operacjach AWS

**Przyczyna:** Role nie ma odpowiednich uprawnień

**Rozwiązanie:**
- Sprawdź Permissions Policy roli
- Dodaj brakujące uprawnienia (ECR, S3, EC2, SSM)

### Problem: "Invalid identity token"

**Przyczyna:** Identity Provider nie jest poprawnie skonfigurowany

**Rozwiązanie:**
- Sprawdź Provider URL: `https://token.actions.githubusercontent.com`
- Sprawdź Audience: `sts.amazonaws.com`

---

## 🔒 Bezpieczeństwo - Best Practices

### 1. Ogranicz dostęp do konkretnych repozytoriów

W Trust Policy użyj:
```json
"token.actions.githubusercontent.com:sub": "repo:TOMEK_USERNAME/WEBAPP_REPO_NAME:*"
```

### 2. Ogranicz dostęp do konkretnych branchy

```json
"token.actions.githubusercontent.com:ref": "refs/heads/main"
```

### 3. Użyj najmniejszych uprawnień (Principle of Least Privilege)

Zamiast `*` w Resource, użyj konkretnych ARN:
```json
"Resource": [
  "arn:aws:s3:::forum-frontend-builds",
  "arn:aws:s3:::forum-frontend-builds/*"
]
```

### 4. Regularnie przeglądaj uprawnienia

- Sprawdź czy wszystkie uprawnienia są potrzebne
- Usuń nieużywane uprawnienia

---

## 📊 Porównanie: Access Keys vs OIDC

| Aspekt | Access Keys | OIDC |
|--------|-------------|------|
| **Bezpieczeństwo** | ⚠️ Statyczne klucze | ✅ Tymczasowe tokeny |
| **Rotacja** | ❌ Ręczna | ✅ Automatyczna |
| **Setup** | ✅ Prosty | ⚠️ Wymaga konfiguracji |
| **Koszt** | $0 | $0 |
| **Zalecane** | ❌ Nie | ✅ Tak |

---

## 📚 Dodatkowe zasoby

- [AWS OIDC Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [AWS IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)

---

**Ostatnia aktualizacja:** 2025-01-XX


