# 🔧 Cloudflare Error 521 - Web Server is Down - FIX

**Błąd 521** oznacza, że Cloudflare nie może połączyć się z Twoim ALB.

---

## 🔍 KROK 1: Sprawdź czy ALB działa bezpośrednio

**Otwórz w przeglądarce:**
```
http://forum-alb-1684129147.us-east-1.elb.amazonaws.com
```

**Jeśli NIE działa:**
- Problem jest z ALB/instancjami, nie z Cloudflare
- Sprawdź Target Group Health w AWS Console
- Sprawdź logi: `docker logs forum-backend` na instancjach

**Jeśli DZIAŁA:**
- Problem jest z konfiguracją Cloudflare
- Przejdź do KROKU 2

---

## 🔧 KROK 2: Sprawdź Cloudflare SSL/TLS Mode

**⚠️ TO JEST NAJCZĘSTSZA PRZYCZYNA!**

1. Idź do **Cloudflare Dashboard**: https://dash.cloudflare.com/
2. Wybierz domenę: `kongoapp.pl`
3. Idź do zakładki: **SSL/TLS**
4. Sprawdź sekcję: **SSL/TLS encryption mode**

**Musi być ustawione na:**
- ✅ **Full** (nie "Full (strict)"!)

**Dlaczego?**
- ALB ma tylko **HTTP** listener (port 80)
- Cloudflare "Full" = HTTPS między Cloudflare a użytkownikiem, HTTP między Cloudflare a ALB
- Cloudflare "Full (strict)" = wymaga HTTPS na ALB (którego nie mamy)

**Jeśli było "Full (strict)":**
1. Zmień na **Full**
2. Poczekaj 1-2 minuty
3. Odśwież stronę `https://kongoapp.pl`

---

## 🔒 KROK 3: Sprawdź Security Group ALB

**Security Group ID:** `sg-01929c8ed5d6bd382`

1. AWS Console → **EC2** → **Security Groups**
2. Znajdź: `forum-alb-sg` (ID: `sg-01929c8ed5d6bd382`)
3. Sprawdź **Inbound rules:**

**Musi być:**
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

1. Cloudflare Dashboard → **DNS** → **Records**
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

## 🔍 KROK 5: Sprawdź Cloudflare Origin Server

1. Cloudflare Dashboard → **SSL/TLS** → **Origin Server**
2. Sprawdź czy jest certyfikat (powinien być automatycznie wygenerowany)
3. Jeśli nie ma, kliknij **Create Certificate** (opcjonalne, nie jest wymagane dla "Full" mode)

---

## 🧪 KROK 6: Test z wyłączonym Cloudflare Proxy (diagnostyka)

**Tymczasowo wyłącz Cloudflare Proxy:**

1. Cloudflare Dashboard → **DNS** → **Records**
2. Kliknij na rekord `@` (root domain)
3. Zmień **Proxy status** na **DNS only** (szara chmurka)
4. Kliknij **Save**
5. Poczekaj 2-3 minuty
6. Spróbuj wejść na: `http://kongoapp.pl` (bez HTTPS!)

**Jeśli działa bez proxy:**
- Problem jest z konfiguracją Cloudflare Proxy
- Wróć do KROKU 2 (SSL/TLS mode)

**Jeśli NIE działa (błąd 521 nadal):**
- ⚠️ Problem jest z DNS lub ALB
- Przejdź do **KROKU 6A** poniżej

---

## 🔍 KROK 6A: Diagnostyka DNS (jeśli błąd 521 występuje nawet bez Proxy)

**Jeśli błąd 521 występuje nawet gdy Cloudflare Proxy jest wyłączone, problem jest z DNS lub ALB.**

### 6A.1. Sprawdź DNS Resolution

**W PowerShell (Windows):**
```powershell
nslookup kongoapp.pl
```

**Lub użyj online tool:**
- https://dnschecker.org/#A/kongoapp.pl
- https://www.whatsmydns.net/#A/kongoapp.pl

**Powinno pokazać:**
- `forum-alb-1684129147.us-east-1.elb.amazonaws.com` (CNAME)

**Jeśli pokazuje coś innego lub błąd:**
- Problem z DNS propagation
- Sprawdź KROK 6A.2

### 6A.2. Sprawdź Nameservery u Rejestratora Domeny

**Cloudflare nameservery (z Cloudflare Dashboard):**
- `denver.ns.cloudflare.com`
- `phoenix.ns.cloudflare.com`

**Sprawdź u rejestratora domeny (np. OVH, Namecheap, Freenom):**
1. Zaloguj się do panelu rejestratora
2. Znajdź sekcję "DNS" lub "Nameservers"
3. Sprawdź czy wskazują na Cloudflare nameservery

**Jeśli NIE wskazują na Cloudflare:**
1. Zmień nameservery na te z Cloudflare
2. Poczekaj 5-30 minut na propagację
3. Sprawdź ponownie DNS resolution

### 6A.3. Sprawdź Target Group Health

**AWS Console → EC2 → Target Groups → `forum-tg`**

**Sprawdź zakładkę "Targets":**
- Wszystkie instancje powinny być **healthy** (zielony status)
- Jeśli są **unhealthy** (czerwony status):
  - Sprawdź logi: `docker logs forum-backend` na instancjach
  - Sprawdź czy Nginx działa: `sudo systemctl status nginx`
  - Sprawdź health check endpoint: `curl http://localhost/health`

### 6A.4. Sprawdź ALB Status

**AWS Console → EC2 → Load Balancers → `forum-alb`**

**Sprawdź:**
- **State:** powinien być **Active** (nie "Failed" lub "Provisioning")
- **Security groups:** powinien mieć `forum-alb-sg` (`sg-01929c8ed5d6bd382`)
- **Listeners:** powinien mieć listener na porcie 80 (HTTP)

### 6A.5. Test bezpośredniego dostępu do ALB

**Otwórz w przeglądarce:**
```
http://forum-alb-1684129147.us-east-1.elb.amazonaws.com
```

**Jeśli NIE działa:**
- Problem jest z ALB lub instancjami
- Sprawdź Target Group Health (KROK 6A.3)
- Sprawdź Security Group ALB (KROK 3)

**Jeśli działa:**
- Problem jest z DNS
- Sprawdź DNS resolution (KROK 6A.1)
- Sprawdź nameservery (KROK 6A.2)

---

## ✅ KROK 7: Weryfikacja po naprawie

**Po wykonaniu poprawek:**

1. Poczekaj 2-5 minut (propagacja zmian)
2. Wyczyść cache przeglądarki (Ctrl+Shift+Delete)
3. Spróbuj wejść na:
   - `https://kongoapp.pl`
   - `https://www.kongoapp.pl`

**Powinieneś zobaczyć:**
- ✅ Stronę React Forum
- ✅ Kłódkę SSL w przeglądarce
- ✅ Brak błędu 521

---

## 🚨 PROBLEM: Cloudflare nie dociera do ALB (brak requestów w logach)

**Jeśli w logach Nginx NIE MA requestów z Cloudflare IP (104.21.44.121, 172.67.199.149, itp.):**

To oznacza, że Cloudflare nie może rozwiązać DNS do ALB lub nie może się połączyć.

### Rozwiązanie 1: Sprawdź DNS Resolution z różnych lokalizacji

**Użyj online tools:**
- https://dnschecker.org/#CNAME/kongoapp.pl
- https://www.whatsmydns.net/#CNAME/kongoapp.pl

**Sprawdź czy wszystkie serwery DNS pokazują:**
- `forum-alb-1684129147.us-east-1.elb.amazonaws.com`

**Jeśli NIE wszystkie pokazują poprawny CNAME:**
- Problem z DNS propagation
- Poczekaj 5-30 minut
- Sprawdź nameservery u rejestratora domeny

### Rozwiązanie 2: Sprawdź czy Cloudflare widzi poprawny CNAME

**Cloudflare Dashboard → DNS → Records**

**Sprawdź rekord CNAME:**
- **Name:** `@` (lub `kongoapp.pl`)
- **Target:** `forum-alb-1684129147.us-east-1.elb.amazonaws.com`
- **Proxy status:** ☑️ Proxied (pomarańczowa chmurka)

**Jeśli Target jest niepoprawny:**
1. Kliknij **Edit**
2. Zmień Target na: `forum-alb-1684129147.us-east-1.elb.amazonaws.com`
3. **WAŻNE:** Bez `http://` lub `https://`, bez końcowego `/`
4. Kliknij **Save**

### Rozwiązanie 3: Wyłącz i włącz ponownie Cloudflare Proxy

**Cloudflare Dashboard → DNS → Records**

1. Kliknij na rekord `@` (root domain)
2. Zmień **Proxy status** na **DNS only** (szara chmurka)
3. Kliknij **Save**
4. Poczekaj 2 minuty
5. Zmień z powrotem na **Proxied** (pomarańczowa chmurka)
6. Kliknij **Save**
7. Poczekaj 5-10 minut na propagację

### Rozwiązanie 4: Sprawdź Cloudflare Pseudo IPv4

**Cloudflare Dashboard → Network → Pseudo IPv4**

**Spróbuj zmienić na:**
- **Add header** (może pomóc z IPv6 → IPv4)

### Rozwiązanie 5: Wyczyść cache Cloudflare

**Cloudflare Dashboard → Caching → Purge Everything**

Może być stary błąd 521 w cache.

### Rozwiązanie 6: Sprawdź czy ALB obsługuje IPv6

**AWS Console → EC2 → Load Balancers → `forum-alb`**

**Sprawdź:**
- **IP address type:** Powinno być **IPv4** (nie Dualstack)

**Jeśli jest Dualstack:**
- ALB może mieć problem z IPv6
- Zmień na **IPv4 only**

---

## 🆘 Jeśli nadal nie działa

### Sprawdź CNAME Resolution

**W PowerShell:**
```powershell
nslookup -type=CNAME kongoapp.pl
```

C:\Users\TOMEK>nslookup -type=CNAME kongoapp.pl
Server:  family.cloudflare-dns.com
Address:  1.1.1.3

kongoapp.pl
        primary name server = denver.ns.cloudflare.com
        responsible mail addr = dns.cloudflare.com
        serial  = 2389683313
        refresh = 10000 (2 hours 46 mins 40 secs)
        retry   = 2400 (40 mins)
        expire  = 604800 (7 days)
        default TTL = 1800 (30 mins)


**Powinno pokazać:**
- `forum-alb-1684129147.us-east-1.elb.amazonaws.com`

**Jeśli pokazuje coś innego:**
- Cloudflare nie widzi poprawnego CNAME
- Sprawdź DNS Records w Cloudflare Dashboard
- Upewnij się, że Target w rekordzie CNAME to: `forum-alb-1684129147.us-east-1.elb.amazonaws.com`

### Sprawdź Target Group Health (NAJWAŻNIEJSZE!)

**AWS Console → EC2 → Target Groups → `forum-tg` → zakładka "Targets"**

**Jeśli instancje są UNHEALTHY (czerwony status):**

1. **Sprawdź health check endpoint na instancji:**
   ```bash
   # Przez Systems Manager Session Manager:
   curl http://localhost/health
   ```
   Powinno zwrócić: `healthy`

2. **Sprawdź czy Nginx działa:**
   ```bash
   sudo systemctl status nginx
   ```

3. **Sprawdź logi Django:**
   ```bash
   docker logs forum-backend
   ```

4. **Sprawdź Target Group Health Check Settings:**
   - AWS Console → Target Groups → `forum-tg` → Health checks
   - **Health check path:** `/health`
   - **Success codes:** `200`
   - **Interval:** 30 seconds
   - **Timeout:** 5 seconds

### Sprawdź Cloudflare Origin Certificate (opcjonalne)

**Jeśli używasz "Full (strict)" mode:**
1. Cloudflare Dashboard → **SSL/TLS** → **Origin Server**
2. Sprawdź czy jest certyfikat
3. Jeśli nie ma, kliknij **Create Certificate**
4. **Ale:** Dla "Full" mode nie jest wymagane!

### Sprawdź ALB Access Logs

1. AWS Console → **EC2** → **Load Balancers** → `forum-alb`
2. Zakładka **Monitoring** → **Access logs**
3. Sprawdź czy są requesty z Cloudflare IP

**Cloudflare IP ranges:**
- Cloudflare używa wielu IP adresów
- Security Group ALB powinien pozwalać na `0.0.0.0/0` (co już mamy)

### Sprawdź Cloudflare Analytics

1. Cloudflare Dashboard → **Analytics** → **Web Analytics**
2. Sprawdź czy są requesty i jakie błędy
3. Sprawdź **Security Events** → czy WAF nie blokuje requestów

---

## 📋 Checklist

- [✅] ALB działa bezpośrednio przez DNS
- [✅] Cloudflare SSL/TLS mode = **Full** (nie Strict)
- [✅] Security Group ALB pozwala na HTTP (80) i HTTPS (443) z `0.0.0.0/0`
- [✅] DNS Records w Cloudflare mają **Proxied** enabled
- [✅] Nameservery domeny wskazują na Cloudflare
- [✅] Poczekałeś 2-5 minut po zmianach
- [✅] Wyczyściłeś cache przeglądarki

---

**Ostatnia aktualizacja:** 2025-11-26

