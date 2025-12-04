# 🚀 CI/CD Setup - Development i Main Branch

## 📋 Przegląd

Projekt ma dwa workflow CI/CD:

1. **Development Branch** - Tylko testy (bez deploymentu)
2. **Main Branch** - Testy + Pełny deployment na AWS

---

## 🔄 Development Branch Workflow

**Plik:** `.github/workflows/ci-development.yml`

### Kiedy się uruchamia:
- Push do brancha `development`
- Pull Request do brancha `development`

### Co robi:
1. ✅ Testy Django backend (z PostgreSQL)
2. ✅ Testy React frontend (build check)
3. ✅ Sprawdzanie jakości kodu (flake8, ESLint)

### Co NIE robi:
- ❌ Nie buduje Docker images
- ❌ Nie pushuje do ECR
- ❌ Nie wdraża na AWS

---

## 🚀 Main Branch Workflow

**Plik:** `.github/workflows/ci-main-deploy.yml`

### Kiedy się uruchamia:
- Push do brancha `main`
- Pull Request do brancha `main`
- Merge z `development` do `main`

### Co robi:

#### 1. Testy (muszą przejść przed deploymentem)
- ✅ Testy Django backend
- ✅ Testy React frontend

#### 2. Build i Push Backend do ECR
- ✅ Buduje Docker image z Django
- ✅ Taguje jako `latest` i `{commit-sha}`
- ✅ Pushuje do Amazon ECR

#### 3. Build i Upload Frontend do S3
- ✅ Buduje React aplikację
- ✅ **Kasuje poprzedni build** z S3
- ✅ Uploaduje nowy build do `s3://{bucket}/latest/`
- ✅ Tworzy backup w `s3://{bucket}/backups/{timestamp}/`

#### 4. Update Launch Template
- ✅ Pobiera obecną wersję Launch Template
- ✅ Aktualizuje user-data z nowym ECR URI
- ✅ Tworzy nową wersję Launch Template

#### 5. Deploy (Instance Refresh)
- ✅ Uruchamia Instance Refresh w Auto Scaling Group
- ✅ Nowe instancje pobierają nowy Docker image z ECR
- ✅ Nowe instancje pobierają nowy React build z S3

---

## ⚙️ Konfiguracja

### Sekrety w GitHub (Settings → Secrets and variables → Actions)

Musisz dodać:

1. **AWS_ACCESS_KEY_ID** - Twój AWS Access Key
2. **AWS_SECRET_ACCESS_KEY** - Twój AWS Secret Key

### Zmienne środowiskowe w workflow

W pliku `.github/workflows/ci-main-deploy.yml` możesz zmienić:

```yaml
env:
  AWS_REGION: eu-central-1  # Twój region AWS
  ECR_REPOSITORY_BACKEND: forum-backend  # Nazwa ECR repository
  S3_BUCKET_FRONTEND: forum-frontend-builds  # Nazwa S3 bucket
  ASG_NAME: forum-asg  # Nazwa Auto Scaling Group
  LAUNCH_TEMPLATE_NAME: forum-lt  # Nazwa Launch Template
```

---

## 📊 Przepływ pracy

### Development Branch:

```
Push do development
  ↓
Testy backendu ✅
Testy frontendu ✅
  ↓
KONIEC (brak deploymentu)
```

### Main Branch:

```
Push do main
  ↓
Testy backendu ✅
Testy frontendu ✅
  ↓
Build Docker → Push do ECR ✅
Build React → Upload do S3 (kasuje poprzedni) ✅
Update Launch Template ✅
Instance Refresh ASG ✅
  ↓
DEPLOYMENT GOTOWY! 🚀
```

---

## 🔍 Jak sprawdzić czy działa

### 1. Sprawdź workflow w GitHub

1. Idź do repozytorium na GitHubie
2. Kliknij zakładkę **Actions**
3. Powinieneś zobaczyć workflow runs

### 2. Test Development Branch

```bash
git checkout development
git commit --allow-empty -m "Test CI"
git push
```

Sprawdź w GitHub Actions - powinny uruchomić się tylko testy.

### 3. Test Main Branch

```bash
git checkout main
git commit --allow-empty -m "Test deployment"
git push
```

Sprawdź w GitHub Actions - powinny uruchomić się testy + deployment.

---

## 🐛 Troubleshooting

### Problem: "AWS credentials not found"

**Rozwiązanie:**
- Sprawdź czy dodałeś sekrety w GitHub (Settings → Secrets)
- Sprawdź czy nazwy sekretów są dokładnie: `AWS_ACCESS_KEY_ID` i `AWS_SECRET_ACCESS_KEY`

### Problem: "S3 bucket not found"

**Rozwiązanie:**
- Workflow automatycznie utworzy bucket jeśli nie istnieje
- Lub zmień `S3_BUCKET_FRONTEND` w workflow na istniejący bucket

### Problem: "ECR repository not found"

**Rozwiązanie:**
- Utwórz ECR repository w AWS Console
- Nazwa musi być taka sama jak `ECR_REPOSITORY_BACKEND` w workflow

### Problem: "Launch Template not found"

**Rozwiązanie:**
- Sprawdź czy Launch Template istnieje w AWS
- Sprawdź czy nazwa w workflow (`LAUNCH_TEMPLATE_NAME`) jest poprawna

### Problem: "Instance Refresh fails"

**Rozwiązanie:**
- Sprawdź czy ASG ma healthy instances
- Sprawdź Target Group health
- Sprawdź logi w AWS Console (EC2 → Auto Scaling Groups → Activity)

---

## 📝 Checklist przed użyciem

- [ ] Sekrety AWS dodane w GitHub (Settings → Secrets)
- [ ] Zmienne w `ci-main-deploy.yml` zaktualizowane (S3 bucket, ASG name, itp.)
- [ ] ECR repository istnieje w AWS
- [ ] Launch Template istnieje w AWS
- [ ] Auto Scaling Group istnieje w AWS
- [ ] S3 bucket istnieje (lub zostanie utworzony automatycznie)
- [ ] Parameter Store ma `/forum/ALB_DNS` (lub użyje domyślnie `kongoapp.pl`)

---

## 🎯 Najlepsze praktyki

### 1. Używaj Pull Requests

```bash
# Development → Main przez PR
git checkout development
# ... zrób zmiany ...
git push origin development
# Utwórz PR na GitHubie
# Po review → merge do main
```

### 2. Testuj lokalnie przed push

```bash
# Backend
cd backend
python manage.py check
python manage.py test

# Frontend
cd frontend
npm run build
```

### 3. Sprawdzaj logi w GitHub Actions

- Jeśli workflow failuje, sprawdź logi w GitHub Actions
- Każdy step pokazuje co się stało

---

## 📚 Dodatkowe zasoby

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Auto Scaling Instance Refresh](https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-instance-refresh.html)

---

**Ostatnia aktualizacja:** 2025-01-XX




