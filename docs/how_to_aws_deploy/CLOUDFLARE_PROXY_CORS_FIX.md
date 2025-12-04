# 🔧 Fix CORS Error - Cloudflare Proxy Włączone

## Problem

Gdy Cloudflare proxy jest **włączone** (Proxied), przeglądarka automatycznie używa **HTTPS**, więc origin jest `https://kongoapp.pl`, ale Django CORS miał tylko `http://kongoapp.pl`.

**Błąd:**
```
Access to XMLHttpRequest at 'https://kongoapp.pl/api/categories/' 
from origin 'https://kongoapp.pl' has been blocked by CORS policy
```

## Przyczyna

**Gdy Cloudflare proxy jest włączone:**
1. Cloudflare automatycznie przekierowuje HTTP → HTTPS
2. Przeglądarka robi requesty z origin `https://kongoapp.pl` (HTTPS!)
3. Django CORS sprawdza origin i nie znajduje `https://kongoapp.pl` w dozwolonych originach
4. ❌ CORS blokuje request

**Gdy Cloudflare proxy jest wyłączone:**
1. Przeglądarka robi requesty z origin `http://kongoapp.pl` (HTTP)
2. Django CORS ma `http://kongoapp.pl` ✅
3. Działa poprawnie

## Rozwiązanie

### ✅ Zaktualizowano `user_data.txt`

Dodano **HTTPS wersje** do `CORS_ALLOWED_ORIGINS`:

**Przed:**
```bash
CORS_ORIGINS="http://${ALB_DNS},http://kongoapp.pl,http://www.kongoapp.pl"
```

**Po:**
```bash
CORS_ORIGINS="http://${ALB_DNS},http://kongoapp.pl,http://www.kongoapp.pl,https://kongoapp.pl,https://www.kongoapp.pl"
```

Teraz Django pozwala na requesty z:
- ✅ `http://forum-alb-1684129147.us-east-1.elb.amazonaws.com` (bezpośredni ALB)
- ✅ `http://kongoapp.pl` (domena, bez proxy)
- ✅ `http://www.kongoapp.pl` (www, bez proxy)
- ✅ `https://kongoapp.pl` (domena, z proxy - **NOWE!**)
- ✅ `https://www.kongoapp.pl` (www, z proxy - **NOWE!**)

---

## Co musisz zrobić

### KROK 1: Instance Refresh (zaktualizuj EC2 instances)

Nowe instancje będą miały poprawne CORS (z HTTPS), ale istniejące instancje muszą zostać zaktualizowane:

1. AWS Console → **EC2 → Auto Scaling Groups**
2. Wybierz `forum-asg`
3. **Actions → Instance Refresh → Start instance refresh**
4. Wybierz opcje:
   - **Instance replacement method:** Prioritize availability
   - **Instance warmup:** 60 seconds
5. Kliknij **Start instance refresh**

⏳ Poczekaj 5-10 minut aż wszystkie instancje zostaną zaktualizowane.

### KROK 2: Sprawdź frontend `.env.production`

**Frontend powinien używać HTTPS gdy Cloudflare proxy jest włączone:**

Otwórz `frontend/.env.production` i upewnij się, że masz:
```
REACT_APP_API_URL=https://kongoapp.pl/api
```

**WAŻNE:** 
- Gdy Cloudflare proxy jest **włączone** → użyj `https://kongoapp.pl/api`
- Gdy Cloudflare proxy jest **wyłączone** → użyj `http://kongoapp.pl/api`

### KROK 3: Rebuild frontend (jeśli zmieniłeś API URL)

```bash
cd frontend
npm run build
aws s3 sync build/ s3://forum-frontend-builds-kongoapp/latest/ --delete
```

### KROK 4: Weryfikacja

1. Otwórz `https://kongoapp.pl` w przeglądarce
2. Otwórz DevTools (F12) → Console
3. Sprawdź czy nie ma błędów CORS
4. Sprawdź czy kategorie się ładują

**Jeśli nadal widzisz błąd CORS:**
- Sprawdź czy frontend robi requesty do `https://kongoapp.pl/api/categories/` (nie HTTP)
- Sprawdź czy Instance Refresh zakończył się sukcesem
- Sprawdź logi Django: `docker logs forum-backend` na EC2
- Sprawdź czy Cloudflare proxy jest włączone (pomarańczowa chmurka w DNS records)

---

## Dlaczego Cloudflare automatycznie używa HTTPS?

**Cloudflare proxy (Proxied) automatycznie:**
1. Przekierowuje HTTP → HTTPS (301 redirect)
2. Dodaje SSL/TLS certyfikat (Let's Encrypt)
3. Szyfruje komunikację między przeglądarką a Cloudflare
4. Przekazuje requesty do ALB jako HTTP (jeśli SSL/TLS mode = "Full")

**Więc:**
- Użytkownik → Cloudflare: **HTTPS** (`https://kongoapp.pl`)
- Cloudflare → ALB: **HTTP** (jeśli SSL/TLS mode = "Full")
- Origin header w requestach: `https://kongoapp.pl` (HTTPS!)

Dlatego Django musi mieć `https://kongoapp.pl` w CORS_ALLOWED_ORIGINS!

---

## Porównanie: Proxy Włączone vs Wyłączone

| Aspekt | Proxy Włączone (Proxied) | Proxy Wyłączone (DNS only) |
|--------|--------------------------|----------------------------|
| **Origin w requestach** | `https://kongoapp.pl` | `http://kongoapp.pl` |
| **Frontend API URL** | `https://kongoapp.pl/api` | `http://kongoapp.pl/api` |
| **CORS_ALLOWED_ORIGINS** | `https://kongoapp.pl` ✅ | `http://kongoapp.pl` ✅ |
| **SSL/TLS** | ✅ Automatyczny (Cloudflare) | ❌ Brak (chyba że ALB ma certyfikat) |
| **CDN** | ✅ Tak (Cloudflare) | ❌ Nie |
| **WAF** | ✅ Tak (Cloudflare) | ❌ Nie |
| **DDoS Protection** | ✅ Tak (Cloudflare) | ❌ Nie |

---

## Zalecana konfiguracja

**Dla produkcji - ZALECANE:**
- ✅ Cloudflare proxy **WŁĄCZONE** (Proxied)
- ✅ Frontend API URL: `https://kongoapp.pl/api`
- ✅ Django CORS: `https://kongoapp.pl`, `https://www.kongoapp.pl`
- ✅ SSL/TLS mode: "Full" (Cloudflare → ALB: HTTP, Cloudflare → User: HTTPS)

**Korzyści:**
- ✅ Automatyczny SSL/TLS (darmowy certyfikat)
- ✅ CDN (szybsze ładowanie)
- ✅ WAF (ochrona przed atakami)
- ✅ DDoS protection
- ✅ Rate limiting

---

**Ostatnia aktualizacja:** 2025-11-26













