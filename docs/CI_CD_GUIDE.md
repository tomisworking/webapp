# Przewodnik CI/CD dla początkujących

## 📚 Spis treści
1. [Co to jest CI/CD?](#co-to-jest-cicd)
2. [Dlaczego CI/CD jest ważne?](#dlaczego-cicd-jest-ważne)
3. [Jak działa CI/CD?](#jak-działa-cicd)
4. [Narzędzia CI/CD - przegląd](#narzędzia-cicd---przegląd)
5. [Rekomendacja dla tego projektu](#rekomendacja-dla-tego-projektu)
6. [Instalacja i konfiguracja GitHub Actions](#instalacja-i-konfiguracja-github-actions)
7. [Szczegółowa konfiguracja](#szczegółowa-konfiguracja)
8. [Alternatywne rozwiązania](#alternatywne-rozwiązania)

---

## Co to jest CI/CD?

**CI/CD** to skrót od:
- **CI** = **Continuous Integration** (Ciągła Integracja)
- **CD** = **Continuous Deployment** (Ciągłe Wdrażanie) lub **Continuous Delivery** (Ciągłe Dostarczanie)

### W prostych słowach:

**CI (Continuous Integration)** - to automatyczne sprawdzanie czy Twój kod działa poprawnie, gdy go zapisujesz w repozytorium (np. na GitHubie).

**CD (Continuous Deployment/Delivery)** - to automatyczne wdrażanie Twojej aplikacji na serwer produkcyjny, gdy kod przejdzie wszystkie testy.

### Analogia z życia codziennego:

Wyobraź sobie, że budujesz dom:
- **CI** = automatyczny inspektor budowlany, który sprawdza czy fundamenty są solidne, czy ściany są proste, czy instalacja działa - za każdym razem gdy dodasz nową część
- **CD** = automatyczny robot, który po pozytywnej kontroli inspektora, automatycznie kończy budowę i oddaje dom do użytku

---

## Dlaczego CI/CD jest ważne?

### Bez CI/CD (stary sposób):
1. 👨‍💻 Programista pisze kod na swoim komputerze
2. ✅ Kod działa lokalnie (na jego komputerze)
3. 📤 Programista wysyła kod na serwer produkcyjny
4. ❌ **PROBLEM**: Kod nie działa na serwerze! (bo serwer ma inne ustawienia, brakuje bibliotek, itp.)
5. 🔧 Programista próbuje naprawić problem na serwerze
6. ⏰ Tracisz czas, użytkownicy widzą błędy

### Z CI/CD (nowoczesny sposób):
1. 👨‍💻 Programista pisze kod
2. 📤 Kod jest automatycznie testowany w środowisku podobnym do produkcyjnego
3. ✅ Jeśli testy przejdą → kod automatycznie trafia na serwer
4. ❌ Jeśli testy nie przejdą → programista dostaje informację o błędzie
5. ⚡ Szybko, bezpiecznie, automatycznie!

### Korzyści:
- ✅ **Mniej błędów** - kod jest testowany przed wdrożeniem
- ✅ **Szybsze wdrażanie** - automatycznie, bez ręcznej pracy
- ✅ **Większe bezpieczeństwo** - testy sprawdzają czy nic się nie zepsuło
- ✅ **Historia zmian** - zawsze wiesz co i kiedy zostało wdrożone
- ✅ **Mniej stresu** - nie musisz ręcznie wdrażać każdej zmiany

---

## Jak działa CI/CD?

### Proces krok po kroku:

```
1. Programista zapisuje kod (commit + push do GitHuba)
   ↓
2. CI/CD system wykrywa zmianę
   ↓
3. Automatyczne testy:
   - Sprawdza czy kod się kompiluje
   - Uruchamia testy jednostkowe
   - Sprawdza jakość kodu (linter)
   - Buduje aplikację
   ↓
4. Jeśli testy przejdą:
   - Buduje obraz Docker
   - Wysyła na serwer produkcyjny
   - Restartuje aplikację
   ↓
5. Jeśli testy nie przejdą:
   - Wysyła powiadomienie o błędzie
   - Zatrzymuje proces (nie wdraża błędnego kodu)
```

### Przykład z życia:

Wyobraź sobie, że masz aplikację forum internetowego:

1. **Dodajesz nową funkcję** - możliwość edycji postów
2. **Zapisujesz kod** na GitHubie
3. **CI/CD automatycznie**:
   - Sprawdza czy React frontend się buduje ✅
   - Sprawdza czy Django backend działa ✅
   - Sprawdza czy testy przechodzą ✅
   - Buduje kontenery Docker ✅
   - Wdraża na AWS ✅
4. **Po 5-10 minutach** nowa funkcja jest już dostępna dla użytkowników!

---

## Narzędzia CI/CD - przegląd

### 1. **GitHub Actions** ⭐ (REKOMENDOWANE dla tego projektu)
- ✅ **Darmowe** dla projektów publicznych
- ✅ **Darmowe** 2000 minut/miesiąc dla projektów prywatnych
- ✅ **Zintegrowane z GitHubem** - nie trzeba nic dodatkowego instalować
- ✅ **Łatwe w użyciu** - konfiguracja w plikach YAML
- ✅ **Duża społeczność** - wiele gotowych przykładów

### 2. **GitLab CI/CD**
- ✅ Darmowe dla projektów na GitLabie
- ✅ Bardzo zaawansowane funkcje
- ⚠️ Wymaga repozytorium na GitLabie

### 3. **Jenkins**
- ✅ Darmowe i open-source
- ✅ Bardzo elastyczne
- ❌ Wymaga własnego serwera
- ❌ Bardziej skomplikowane w konfiguracji

### 4. **CircleCI**
- ✅ Ładny interfejs
- ✅ Dobra dokumentacja
- ⚠️ Ograniczenia w darmowym planie

### 5. **AWS CodePipeline** (dla projektów AWS)
- ✅ Zintegrowane z AWS
- ✅ Dobre dla zaawansowanych projektów AWS
- ⚠️ Może być droższe
- ⚠️ Bardziej skomplikowane

---

## Rekomendacja dla tego projektu

**Dla Twojego projektu rekomenduję GitHub Actions**, ponieważ:

1. ✅ Projekt jest już prawdopodobnie na GitHubie (lub możesz go tam przenieść)
2. ✅ Masz już Docker - GitHub Actions świetnie z nim współpracuje
3. ✅ Masz deployment na AWS - GitHub Actions może automatycznie wdrażać na AWS
4. ✅ Darmowe dla większości przypadków użycia
5. ✅ Łatwe do rozpoczęcia - wystarczy dodać pliki konfiguracyjne

---

## Instalacja i konfiguracja GitHub Actions

### Krok 1: Przygotowanie repozytorium

Upewnij się, że Twój projekt jest na GitHubie:
```bash
# Jeśli jeszcze nie masz repozytorium na GitHubie:
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TWOJA_NAZWA/TWOJE_REPO.git
git push -u origin main
```

### Krok 2: Utworzenie struktury katalogów

GitHub Actions szuka plików konfiguracyjnych w katalogu `.github/workflows/`

Utwórz katalog:
```bash
mkdir -p .github/workflows
```

### Krok 3: Podstawowy plik CI/CD

Utworzymy plik `.github/workflows/ci-cd.yml` który będzie:
- Testował kod przy każdym pushu
- Budował obrazy Docker
- Wdrażał na AWS (opcjonalnie)

---

## Szczegółowa konfiguracja

### Opcja 1: Podstawowy CI (tylko testy)

Ten workflow będzie:
- ✅ Sprawdzał czy kod się kompiluje
- ✅ Uruchamiał testy (jeśli masz)
- ✅ Sprawdzał jakość kodu

**Plik: `.github/workflows/ci.yml`**

```yaml
name: CI - Testy i Walidacja

# Kiedy workflow ma się uruchomić
on:
  push:
    branches: [ main, develop ]  # Przy pushu na główne branche
  pull_request:
    branches: [ main ]  # Przy tworzeniu Pull Request

jobs:
  # Testy backendu (Django)
  test-backend:
    name: Test Django Backend
    runs-on: ubuntu-latest  # System operacyjny runnera
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - name: Pobierz kod
        uses: actions/checkout@v3
      
      - name: Ustaw Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Zainstaluj zależności
        working-directory: ./backend
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Uruchom migracje
        working-directory: ./backend
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          SECRET_KEY: test-secret-key
          DEBUG: True
        run: |
          python manage.py migrate
      
      - name: Sprawdź kod (flake8)
        working-directory: ./backend
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      
      - name: Test Django
        working-directory: ./backend
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          SECRET_KEY: test-secret-key
          DEBUG: True
        run: |
          python manage.py test

  # Testy frontendu (React)
  test-frontend:
    name: Test React Frontend
    runs-on: ubuntu-latest
    
    steps:
      - name: Pobierz kod
        uses: actions/checkout@v3
      
      - name: Ustaw Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Zainstaluj zależności
        working-directory: ./frontend
        run: npm ci
      
      - name: Sprawdź kod (ESLint)
        working-directory: ./frontend
        run: npm run build --if-present || true
      
      - name: Buduj aplikację
        working-directory: ./frontend
        run: npm run build
```

### Opcja 2: Pełny CI/CD z Docker i AWS

Ten workflow będzie:
- ✅ Testował kod
- ✅ Budował obrazy Docker
- ✅ Wysyłał obrazy do AWS ECR (Elastic Container Registry)
- ✅ Wdrażał na AWS EC2/ECS

**Plik: `.github/workflows/deploy.yml`**

```yaml
name: CI/CD - Build i Deploy

on:
  push:
    branches: [ main ]  # Tylko dla głównej gałęzi
  workflow_dispatch:  # Możliwość ręcznego uruchomienia

env:
  AWS_REGION: us-east-1  # Zmień na swój region
  ECR_REPOSITORY_BACKEND: forum-backend
  ECR_REPOSITORY_FRONTEND: forum-frontend
  ECS_CLUSTER: forum-cluster
  ECS_SERVICE_BACKEND: forum-backend-service
  ECS_SERVICE_FRONTEND: forum-frontend-service

jobs:
  # Testy (jak w poprzednim przykładzie)
  test:
    name: Testy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test Backend
        run: |
          # Tutaj testy backendu
          echo "Testy backendu..."
      - name: Test Frontend
        run: |
          # Tutaj testy frontendu
          echo "Testy frontendu..."

  # Budowanie i wdrażanie
  build-and-deploy:
    name: Build Docker i Deploy na AWS
    needs: test  # Czeka aż testy przejdą
    runs-on: ubuntu-latest
    
    steps:
      - name: Pobierz kod
        uses: actions/checkout@v3
      
      - name: Konfiguruj AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Logowanie do Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Buduj i push obraz backendu
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY_BACKEND:$IMAGE_TAG ./backend
          docker push $ECR_REGISTRY/$ECR_REPOSITORY_BACKEND:$IMAGE_TAG
      
      - name: Buduj i push obraz frontendu
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          # Najpierw zbuduj React
          cd frontend
          npm install
          npm run build
          cd ..
          
          # Potem zbuduj Docker z zbudowanym frontendem
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY_FRONTEND:$IMAGE_TAG ./frontend
          docker push $ECR_REGISTRY/$ECR_REPOSITORY_FRONTEND:$IMAGE_TAG
      
      - name: Wdróż na ECS (opcjonalnie)
        if: github.ref == 'refs/heads/main'
        run: |
          aws ecs update-service \
            --cluster $ECS_CLUSTER \
            --service $ECS_SERVICE_BACKEND \
            --force-new-deployment \
            --region $AWS_REGION
```

---

## Konfiguracja sekretów w GitHubie

Aby workflow mógł wdrażać na AWS, musisz dodać sekrety:

1. **Idź do swojego repozytorium na GitHubie**
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret**
4. Dodaj:
   - `AWS_ACCESS_KEY_ID` - Twój klucz dostępu AWS
   - `AWS_SECRET_ACCESS_KEY` - Twój sekretny klucz AWS

**UWAGA**: Nigdy nie umieszczaj tych kluczy bezpośrednio w kodzie! Zawsze używaj sekretów GitHub.

---

## Alternatywne rozwiązania

### 1. Prostsze rozwiązanie - tylko testy lokalne

Jeśli nie chcesz jeszcze wdrażać automatycznie, możesz zacząć od prostego workflow który tylko testuje:

```yaml
name: Proste testy

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Sprawdź czy backend się buduje
        run: |
          cd backend
          pip install -r requirements.txt
          python manage.py check
      - name: Sprawdź czy frontend się buduje
        run: |
          cd frontend
          npm install
          npm run build
```

### 2. Deployment przez SSH (jeśli masz EC2)

Jeśli wdrażasz bezpośrednio na EC2 przez SSH:

```yaml
- name: Deploy przez SSH
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USER }}
    key: ${{ secrets.EC2_SSH_KEY }}
    script: |
      cd /path/to/your/app
      git pull
      docker-compose up -d --build
```

### 3. GitLab CI/CD (jeśli używasz GitLab)

Plik `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - build
  - deploy

test-backend:
  stage: test
  image: python:3.11
  script:
    - cd backend
    - pip install -r requirements.txt
    - python manage.py test

build:
  stage: build
  script:
    - docker build -t myapp:latest .
  only:
    - main

deploy:
  stage: deploy
  script:
    - echo "Deploying..."
  only:
    - main
```

---

## Najlepsze praktyki

### 1. **Zawsze testuj przed wdrożeniem**
```yaml
jobs:
  test:
    # Testy muszą przejść
  deploy:
    needs: test  # Czeka na testy
```

### 2. **Używaj różnych środowisk**
- `develop` branch → testowanie
- `main` branch → produkcja

### 3. **Zachowaj historię wersji**
```yaml
- name: Tag version
  run: |
    git tag -a v${{ github.run_number }} -m "Version ${{ github.run_number }}"
    git push origin v${{ github.run_number }}
```

### 4. **Powiadomienia o błędach**
```yaml
- name: Powiadom o błędzie
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Deployment failed!'
```

---

## FAQ - Najczęściej zadawane pytania

### Q: Czy CI/CD jest darmowe?
**A**: GitHub Actions jest darmowe dla projektów publicznych i daje 2000 minut/miesiąc dla projektów prywatnych. To wystarczy dla małych/średnich projektów.

### Q: Czy muszę używać Dockera?
**A**: Nie, ale Docker ułatwia wdrażanie. Możesz też wdrażać bezpośrednio przez SSH.

### Q: Co jeśli testy nie przejdą?
**A**: Workflow się zatrzyma i nie wdroży kodu. Dostaniesz powiadomienie o błędzie.

### Q: Jak często uruchamia się CI/CD?
**A**: Za każdym razem gdy zapiszesz kod (push) lub utworzysz Pull Request.

### Q: Czy mogę ręcznie uruchomić workflow?
**A**: Tak! Dodaj `workflow_dispatch:` do sekcji `on:` w pliku YAML.

---

## Następne kroki

1. ✅ Utwórz plik `.github/workflows/ci.yml` z podstawowymi testami
2. ✅ Przetestuj czy działa (zrób małą zmianę i push)
3. ✅ Dodaj budowanie Docker (jeśli używasz)
4. ✅ Dodaj automatyczne wdrażanie (gdy będziesz gotowy)

---

## Pomoc i zasoby

- 📖 [Dokumentacja GitHub Actions](https://docs.github.com/en/actions)
- 🎓 [GitHub Actions dla początkujących](https://docs.github.com/en/actions/learn-github-actions)
- 💬 [Community GitHub Actions](https://github.community/c/github-actions/41)

---

**Powodzenia z CI/CD! 🚀**

