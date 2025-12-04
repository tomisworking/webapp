# 🔍 Polecenia diagnostyczne dla EC2 (Session Manager)

## Jak połączyć się z EC2

1. AWS Console → **EC2 → Instances**
2. Wybierz jedną z instancji `forum-ec2-instance`
3. Kliknij **Connect** → **Session Manager** → **Connect**

---

## Polecenia do wykonania

### 1. Sprawdź czy frontend ma poprawny build

```bash
# Lista plików frontend
ls -lh /var/www/frontend/

# Sprawdź index.html - który main.js jest używany
cat /var/www/frontend/index.html | grep 'main\.'

# Sprawdź czy są stare pliki JS
ls -lh /var/www/frontend/static/js/
```

**Co szukać:**
- Czy jest tylko jeden `main.*.js` czy wiele?
- Czy `index.html` wskazuje na najnowszy `main.*.js`?

---

### 2. Sprawdź Django container

```bash
# Status containera
docker ps | grep forum-backend

# Django logs (ostatnie 50 linii)
docker logs forum-backend --tail 50

# Sprawdź CORS configuration
docker exec forum-backend printenv CORS_ALLOWED_ORIGINS

# Sprawdź ALLOWED_HOSTS
docker exec forum-backend printenv ALLOWED_HOSTS
```

**Co szukać:**
- Czy container jest "healthy"?
- Czy CORS_ALLOWED_ORIGINS zawiera `https://kongoapp.pl`?
- Czy ALLOWED_HOSTS zawiera `kongoapp.pl`?

---

### 3. Test API bezpośrednio

```bash
# Test health endpoint
curl -I http://127.0.0.1/health

# Test API categories (przez Nginx)
curl -I http://127.0.0.1/api/categories/

# Test API categories (bezpośrednio Django)
curl -I http://127.0.0.1:8000/api/categories/
```

**Oczekiwane wyniki:**
- `/health` → `200 OK`
- `/api/categories/` → `200 OK` (lub `301` jeśli Django redirectuje do trailing slash)

---

### 4. Sprawdź Nginx logs

```bash
# Access log (ostatnie 50 linii)
sudo tail -50 /var/log/nginx/access.log

# Error log (ostatnie 50 linii)
sudo tail -50 /var/log/nginx/error.log

# Live monitoring (Ctrl+C aby zatrzymać)
sudo tail -f /var/log/nginx/access.log
```

**Co szukać:**
- Czy są requesty do `/api/categories/`?
- Jakie status codes (200, 301, 404, 500)?
- Czy są błędy CORS?

---

### 5. Sprawdź user-data log

```bash
# Sprawdź logi z inicjalizacji instancji
sudo tail -100 /var/log/user-data.log

# Sprawdź czy S3 sync się udał
sudo grep "s3 sync" /var/log/user-data.log

# Sprawdź czy Nginx został skonfigurowany
sudo grep "Nginx" /var/log/user-data.log
```

---

### 6. Sprawdź Nginx configuration

```bash
# Wyświetl konfigurację Nginx
sudo cat /etc/nginx/conf.d/forum.conf

# Test konfiguracji Nginx
sudo nginx -t

# Status Nginx
sudo systemctl status nginx
```

---

### 7. Ręczny test CORS

```bash
# Test CORS z curl
curl -I -H "Origin: https://kongoapp.pl" \
     -H "Access-Control-Request-Method: GET" \
     http://127.0.0.1/api/categories/
```

**Szukaj nagłówka:**
```
Access-Control-Allow-Origin: https://kongoapp.pl
```

Jeśli go nie ma → CORS nie jest skonfigurowany poprawnie.

---

## Najczęstsze problemy i rozwiązania

### Problem: Stary main.js w /var/www/frontend/

**Przyczyna:** S3 sync bez `--delete` flagi

**Rozwiązanie:**
1. Ręczne wyczyszczenie:
   ```bash
   sudo rm -rf /var/www/frontend/*
   aws s3 sync s3://forum-frontend-builds-kongoapp/latest/ /var/www/frontend/ --delete
   ```

2. Restart Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

### Problem: Django nie odpowiada

**Sprawdź:**
```bash
docker logs forum-backend --tail 100
```

**Restart containera:**
```bash
docker restart forum-backend
```

### Problem: CORS errors

**Sprawdź CORS configuration:**
```bash
docker exec forum-backend printenv CORS_ALLOWED_ORIGINS
```

**Powinno zawierać:**
```
http://forum-alb-1684129147.us-east-1.elb.amazonaws.com,http://kongoapp.pl,http://www.kongoapp.pl,https://kongoapp.pl,https://www.kongoapp.pl
```

---

**Ostatnia aktualizacja:** 2025-11-27












