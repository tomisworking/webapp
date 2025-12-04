# 🚨 Error 521 - Quick Fix Guide

**Error 521** = Cloudflare nie może połączyć się z ALB.

---

## ✅ KROK 1: Sprawdź czy ALB działa bezpośrednio

**Otwórz w przeglądarce:**
```
http://forum-alb-1684129147.us-east-1.elb.amazonaws.com
```

**Jeśli NIE działa:**
- Problem jest z ALB/instancjami, nie z Cloudflare
- Sprawdź Target Group Health w AWS Console
- Sprawdź logi: `docker logs forum-backend` na instancjach
- **PRZEJDŹ DO KROKU 4**

**Jeśli DZIAŁA:**
- Problem jest z konfiguracją Cloudflare
- **PRZEJDŹ DO KROKU 2**

---

## 🔧 KROK 2: Cloudflare SSL/TLS Mode - TO JEST NAJCZĘSTSZA PRZYCZYNA!

**⚠️ TO JEST NAJCZĘSTSZA PRZYCZYNA ERROR 521!**

1. Cloudflare Dashboard → Wybierz domenę `kongoapp.pl`
2. Zakładka: **SSL/TLS**
3. Sekcja: **SSL/TLS encryption mode**

**MUSI BYĆ:**
- ✅ **Full** (nie "Full (strict)"!)

**Dlaczego?**
- ALB ma tylko **HTTP** listener (port 80)
- Cloudflare "Full" = HTTPS Cloudflare ↔ User, HTTP Cloudflare ↔ ALB ✅
- Cloudflare "Full (strict)" = wymaga HTTPS na ALB (którego nie mamy) ❌

**Jeśli było "Full (strict)":**
1. Zmień na **Full**
2. Poczekaj 1-2 minuty
3. Odśwież stronę `https://kongoapp.pl`

---

## 🔒 KROK 3: Sprawdź Security Group ALB

1. AWS Console → **EC2 → Security Groups**
2. Znajdź: `forum-alb-sg`
3. Sprawdź **Inbound rules:**

**MUSI BYĆ:**
- ✅ **HTTP** (port 80) z `0.0.0.0/0` (Anywhere-IPv4)
- ✅ **HTTPS** (port 443) z `0.0.0.0/0` (Anywhere-IPv4)

**Jeśli brakuje:**
1. Kliknij **Edit inbound rules**
2. Dodaj regułę:
   - **Type:** HTTP
   - **Port:** 80
   - **Source:** `0.0.0.0/0`
   - **Description:** `Allow HTTP from Cloudflare and anywhere`
3. Dodaj regułę:
   - **Type:** HTTPS
   - **Port:** 443
   - **Source:** `0.0.0.0/0`
   - **Description:** `Allow HTTPS from Cloudflare and anywhere`
4. Kliknij **Save rules**

---

## 🌐 KROK 4: Sprawdź DNS Records w Cloudflare

1. Cloudflare Dashboard → **DNS → Records**
2. Sprawdź czy masz:

**Record 1:**
- **Type:** CNAME
- **Name:** `@` (lub `kongoapp.pl`)
- **Target:** `forum-alb-1684129147.us-east-1.elb.amazonaws.com`
- **Proxy status:** ☑️ **Proxied** (pomarańczowa chmurka)

**Record 2:**
- **Type:** CNAME
- **Name:** `www`
- **Target:** `forum-alb-1684129147.us-east-1.elb.amazonaws.com`
- **Proxy status:** ☑️ **Proxied**

**Jeśli "Proxy status" jest "DNS only" (szara chmurka):**
1. Kliknij na rekord
2. Zmień **Proxy status** na **Proxied**
3. Kliknij **Save**

---

## 🔍 KROK 5: Sprawdź Target Group Health

1. AWS Console → **EC2 → Target Groups**
2. Wybierz: `forum-tg`
3. Zakładka: **Targets**

**Sprawdź:**
- Czy wszystkie instancje są **Healthy** (zielony)?
- Czy są jakieś **Unhealthy** (czerwony)?

**Jeśli są Unhealthy:**
- Sprawdź logi: `docker logs forum-backend` na instancjach
- Sprawdź czy Nginx działa: `sudo systemctl status nginx`
- Sprawdź health check: `curl http://127.0.0.1/health` na instancji

---

## 🔍 KROK 6: Sprawdź ALB Listeners

1. AWS Console → **EC2 → Load Balancers**
2. Wybierz: `forum-alb`
3. Zakładka: **Listeners**

**MUSI BYĆ:**
- ✅ **HTTP** listener na porcie **80**
- ✅ **Default action:** Forward to `forum-tg`

**Jeśli brakuje HTTP listener:**
1. Kliknij **Add listener**
2. **Protocol:** HTTP
3. **Port:** 80
4. **Default action:** Forward to `forum-tg`
5. Kliknij **Save**

---

## 📊 KROK 7: Sprawdź Cloudflare Analytics

1. Cloudflare Dashboard → **Analytics → Web Analytics**
2. Sprawdź jakie błędy są logowane
3. Sprawdź **HTTP Status Codes**

**Jeśli widzisz dużo 521:**
- Problem jest z połączeniem Cloudflare → ALB
- Sprawdź KROK 2 (SSL/TLS mode) i KROK 3 (Security Group)

---

## 🧪 Test po naprawie

1. Poczekaj 1-2 minuty po zmianach
2. Otwórz `https://kongoapp.pl` w przeglądarce
3. Sprawdź DevTools (F12) → Network
4. Sprawdź czy requesty zwracają 200 OK

**Jeśli nadal Error 521:**
- Sprawdź czy ALB działa bezpośrednio (KROK 1)
- Sprawdź Target Group Health (KROK 5)
- Sprawdź logi na instancjach EC2

---

## 📝 Checklist

Przed zgłoszeniem problemu sprawdź:

- [ ] ALB działa bezpośrednio (`http://forum-alb-1684129147.us-east-1.elb.amazonaws.com`)
- [ ] Cloudflare SSL/TLS mode = **Full** (nie "Full (strict)")
- [ ] Security Group ALB pozwala na HTTP (80) i HTTPS (443) z `0.0.0.0/0`
- [ ] DNS Records w Cloudflare mają **Proxied** (pomarańczowa chmurka)
- [ ] Target Group ma **Healthy** instancje
- [ ] ALB ma HTTP listener na porcie 80

---

**Ostatnia aktualizacja:** 2025-11-27












