# 🚀 Quick Start - Przygotowanie do AWS Deployment

## ✅ Co zostało zrobione?

Twoja aplikacja jest już **gotowa do deploymentu na AWS**! Oto lista zmian:

### Pliki utworzone:

1. **`backend/Dockerfile`** - kontener Docker dla Django
2. **`backend/docker-entrypoint.sh`** - skrypt startowy
3. **`backend/nginx/nginx.conf`** - konfiguracja Nginx
4. **`backend/.env.example`** - template zmiennych środowiskowych
5. **`docker-compose.yml`** - do lokalnych testów z PostgreSQL
6. **`.github/workflows/deploy-aws.yml`** - CI/CD pipeline
7. **`scripts/migrate_sqlite_to_postgres.py`** - migracja danych
8. **`README_AWS_DEPLOYMENT.md`** - **GŁÓWNY PRZEWODNIK** 📖

### Pliki zaktualizowane:

1. **`backend/config/settings.py`** - wsparcie dla PostgreSQL + security
2. **`backend/config/urls.py`** - health check endpoint `/api/health/`
3. **`backend/requirements.txt`** - dodane pakiety produkcyjne

---

## 🎯 Odpowiedź na Twoje pytanie

### **Czy musisz setupować PostgreSQL lokalnie?**

**NIE!** Masz 2 opcje:

### Opcja A: SQLite lokalnie → PostgreSQL na AWS (ZALECANE)

```bash
# Pracujesz jak dotychczas
cd backend
python manage.py runserver
```

- ✅ Najprostsze
- ✅ Nie trzeba nic instalować
- ✅ Na AWS automatycznie przełączy się na RDS PostgreSQL

### Opcja B: PostgreSQL lokalnie przez Docker (opcjonalnie)

Jeśli chcesz przetestować PostgreSQL PRZED AWS:

```bash
# 1. Utwórz plik .env w backend/
copy backend\.env.example backend\.env

# 2. Edytuj backend/.env - zmień na:
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/forumdb

# 3. Uruchom Docker Compose
docker-compose up -d

# 4. Aplikacja teraz działa z PostgreSQL lokalnie!
```

**Moja rekomendacja:** Zostań przy SQLite lokalnie, a PostgreSQL tylko na AWS.

---

## 📝 Co dalej - Następne kroki

### Krok 1: Przeczytaj główny przewodnik

```bash
# Otwórz ten plik i czytaj krok po kroku:
README_AWS_DEPLOYMENT.md
```

To jest **KOMPLETNY** przewodnik od zera do działającej aplikacji na AWS.

### Krok 2: Przetestuj lokalnie z Docker (opcjonalnie)

```bash
# Sprawdź czy Dockerfile działa
cd backend
docker build -t forum-backend .
docker run -p 8000:8000 -e DEBUG=True forum-backend

# Test health check
curl http://localhost:8000/api/health/
```

### Krok 3: Załóż konto AWS

Idź na: https://aws.amazon.com/free

### Krok 4: Wykonaj przewodnik `README_AWS_DEPLOYMENT.md`

W przewodniku znajdziesz:
- ✅ Jak utworzyć VPC i Subnets
- ✅ Jak utworzyć RDS PostgreSQL
- ✅ Jak skonfigurować Load Balancer
- ✅ Jak uruchomić Auto Scaling
- ✅ Jak wdrożyć aplikację
- ✅ Jak przenieść dane z SQLite

---

## 🔐 Zmienne środowiskowe

### Dla rozwoju lokalnego (SQLite)

Utwórz `backend/.env`:

```env
DEBUG=True
SECRET_KEY=dev-secret-key-min-50-chars
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000
```

### Dla AWS (PostgreSQL na RDS)

Zmienne będą w **AWS Systems Manager Parameter Store**:

```
/forum/DATABASE_URL = postgresql://user:pass@rds-endpoint/forumdb
/forum/SECRET_KEY = [długi losowy string]
/forum/ALLOWED_HOSTS = twoja-domena.com
```

---

## 🧪 Testowanie przed AWS

### Test 1: Sprawdź czy Django działa

```bash
cd backend
python manage.py check
python manage.py migrate
python manage.py runserver
```

### Test 2: Sprawdź health check endpoint

```bash
# Uruchom serwer, potem:
curl http://localhost:8000/api/health/

# Powinno zwrócić:
# {"status": "healthy", "service": "forum-backend"}
```

### Test 3: Test Docker image

```bash
cd backend
docker build -t forum-backend .
docker run -p 8000:8000 -e DEBUG=True -e SECRET_KEY=test forum-backend

# W drugim terminalu:
curl http://localhost:8000/api/health/
```

---

## 📚 Struktura dokumentacji

```
WEBAPP/
├── README_AWS_DEPLOYMENT.md  ← GŁÓWNY PRZEWODNIK (czytaj TO!)
├── docs/
│   └── QUICK_START.md        ← Ten plik (szybki start)
└── backend/
    └── .env.example          ← Template zmiennych
```

---

## ❓ FAQ

### Czy mogę dalej pracować lokalnie z SQLite?

**TAK!** Nic się nie zmienia w lokalnym developmencie.

### Kiedy aplikacja przełączy się na PostgreSQL?

Automatycznie gdy ustawisz zmienną środowiskową `DATABASE_URL`.

### Czy muszę używać Docker lokalnie?

**NIE!** Docker jest tylko do:
1. Testowania przed AWS (opcjonalnie)
2. Deploymentu na AWS (wymagane)

### Co jeśli mam problem?

1. Sprawdź `README_AWS_DEPLOYMENT.md` → sekcja "Troubleshooting"
2. Pytaj na zespołowym chacie
3. Sprawdź logi: `docker logs forum-backend`

---

## 🎯 Podsumowanie

### Co masz teraz:

✅ Aplikacja gotowa do deploymentu  
✅ Dockerfile i konfiguracja Nginx  
✅ CI/CD pipeline (GitHub Actions)  
✅ Wsparcie dla SQLite (dev) i PostgreSQL (prod)  
✅ Health check endpoint dla ALB  
✅ Kompletna dokumentacja  

### Co musisz zrobić:

1. 📖 Przeczytać `README_AWS_DEPLOYMENT.md`
2. ☁️ Założyć konto AWS
3. 🏗️ Wykonać przewodnik krok po kroku
4. 🚀 Wdrożyć aplikację

---

**Powodzenia! 🎉**

Jeśli masz pytania, patrz do przewodnika lub pytaj zespół!

