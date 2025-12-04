# 🔧 Fix CORS Error - Cloudflare Proxy Wyłączone

## Problem

Gdy Cloudflare proxy jest **wyłączone** (DNS only), frontend na `http://kongoapp.pl` próbuje robić requesty do ALB bezpośrednio, co powoduje błąd CORS:

```
Access to XMLHttpRequest at 'http://forum-alb-1684129147.us-east-1.elb.amazonaws.com/api/categories/' 
from origin 'http://kongoapp.pl' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Rozwiązanie

### KROK 1: Zaktualizuj frontend `.env.production`

**Frontend powinien używać domeny, nie ALB DNS bezpośrednio:**

1. Otwórz `frontend/.env.production`
2. Zmień na:
   ```
   REACT_APP_API_URL=http://kongoapp.pl/api
   ```
   (lub `https://kongoapp.pl/api` jeśli masz SSL)

3. **WAŻNE:** URL musi kończyć się na `/api`!

### KROK 2: Rebuild frontend

```bash
cd frontend
npm run build
```

### KROK 3: Upload do S3

```bash
aws s3 sync build/ s3://forum-frontend-builds-kongoapp/latest/ --delete
```

### KROK 4: Instance Refresh (zaktualizuj EC2 instances)

**Django CORS został już zaktualizowany w `user_data.txt`** - nowe instancje będą miały poprawne CORS.

1. AWS Console → **EC2 → Auto Scaling Groups**
2. Wybierz `forum-asg`
3. **Actions → Instance Refresh → Start instance refresh**
4. Wybierz opcje:
   - **Instance replacement method:** Prioritize availability
   - **Instance warmup:** 60 seconds
   - Kliknij **Start instance refresh**

⏳ Poczekaj 5-10 minut aż wszystkie instancje zostaną zaktualizowane.

### KROK 5: Weryfikacja

1. Otwórz `http://kongoapp.pl` w przeglądarce
2. Otwórz DevTools (F12) → Console
3. Sprawdź czy nie ma błędów CORS
4. Sprawdź czy kategorie się ładują

**Jeśli nadal widzisz błąd CORS:**
- Sprawdź czy frontend robi requesty do `http://kongoapp.pl/api/categories/` (nie do ALB bezpośrednio)
- Sprawdź czy Instance Refresh zakończył się sukcesem
- Sprawdź logi Django: `docker logs forum-backend` na EC2

---

## Co zostało zmienione?

### 1. `user_data.txt` - CORS_ALLOWED_ORIGINS

**Przed:**
```bash
-e CORS_ALLOWED_ORIGINS="http://${ALB_DNS}"
```

**Po:**
```bash
CORS_ORIGINS="http://${ALB_DNS},http://kongoapp.pl,http://www.kongoapp.pl"
-e CORS_ALLOWED_ORIGINS="$CORS_ORIGINS"
```

Teraz Django pozwala na requesty z:
- `http://forum-alb-1684129147.us-east-1.elb.amazonaws.com` (bezpośredni dostęp do ALB)
- `http://kongoapp.pl` (domena)
- `http://www.kongoapp.pl` (www subdomain)

### 2. Dokumentacja - `DAY_2_DEPLOYMENT.md`

Zaktualizowano instrukcje dotyczące `REACT_APP_API_URL` - teraz zaleca używanie domeny zamiast ALB DNS.

---

## Dlaczego to działa?

**Gdy Cloudflare proxy jest wyłączone:**
- DNS `kongoapp.pl` wskazuje na ALB (CNAME)
- Requesty z przeglądarki idą do `kongoapp.pl`
- DNS rozwiązuje to na ALB
- ALB przekazuje do EC2
- Django musi pozwolić na CORS z origin `http://kongoapp.pl` ✅

**Gdy Cloudflare proxy jest włączone:**
- Requesty idą do Cloudflare
- Cloudflare proxy'uje do ALB
- Django musi pozwolić na CORS z origin `http://kongoapp.pl` (Cloudflare przekazuje oryginalny origin) ✅

W obu przypadkach Django musi mieć `kongoapp.pl` w CORS_ALLOWED_ORIGINS!

---

## Alternatywa: Włącz Cloudflare Proxy

Jeśli chcesz używać Cloudflare proxy (zalecane dla produkcji):

1. Cloudflare Dashboard → **DNS → Records**
2. Dla record `@` i `www`: Kliknij szarą chmurkę → zmień na pomarańczową (Proxied)
3. Frontend może używać `http://kongoapp.pl/api` lub `https://kongoapp.pl/api`
4. Cloudflare zapewni:
   - SSL/TLS (HTTPS)
   - CDN (szybsze ładowanie)
   - WAF (ochrona)
   - DDoS protection

---

**Ostatnia aktualizacja:** 2025-11-26













