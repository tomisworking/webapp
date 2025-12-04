# 🔧 Fix: CNAME nie rozwiązują się globalnie - Error 521

## Problem

CNAME records dla `kongoapp.pl` nie rozwiązują się globalnie (wszystkie czerwone X na dnschecker.org). To powoduje Error 521, bo Cloudflare nie może znaleźć IP ALB.

---

## 🔍 Diagnostyka

### KROK 1: Sprawdź czy Cloudflare widzi CNAME

**Cloudflare Dashboard → DNS → Records**

**Sprawdź rekord:**
- **Type:** CNAME
- **Name:** `@` (lub `kongoapp.pl`)
- **Target:** `forum-alb-1684129147.us-east-1.elb.amazonaws.com`
- **Proxy status:** Proxied (pomarańczowa chmurka)

**WAŻNE:** Target musi być **dokładnie** taki sam jak ALB DNS, bez:
- `http://` lub `https://`
- Końcowego `/`
- Spacji

### KROK 2: Sprawdź czy Cloudflare DNS jest włączone

**Cloudflare Dashboard → DNS → Settings**

**Sprawdź:**
- **DNS:** Powinno być **ON** (włączone)
- **DNS over HTTPS (DoH):** Może być włączone
- **DNS over TLS (DoT):** Może być włączone

**Jeśli DNS jest wyłączone:**
1. Włącz DNS
2. Poczekaj 5-10 minut

### KROK 3: Sprawdź czy ALB DNS rozwiązuje się

**W terminalu/PowerShell:**
```bash
nslookup forum-alb-1684129147.us-east-1.elb.amazonaws.com
```

**Powinieneś zobaczyć IP adresy ALB:**
```
Name:    forum-alb-1684129147.us-east-1.elb.amazonaws.com
Addresses:  54.158.162.197
           3.211.103.212
```

**Jeśli NIE widzisz IP:**
- Problem jest z ALB DNS (nie z Cloudflare)
- Sprawdź czy ALB jest Active w AWS Console

---

## 🔧 Rozwiązania

### Rozwiązanie 1: Usuń i dodaj ponownie CNAME record

**Czasami Cloudflare cache'uje stary rekord.**

1. **Cloudflare Dashboard → DNS → Records**
2. Kliknij na rekord `@` (root domain)
3. Kliknij **Delete**
4. Poczekaj 1 minutę
5. Kliknij **Add record**
6. **Type:** CNAME
7. **Name:** `@`
8. **Target:** `forum-alb-1684129147.us-east-1.elb.amazonaws.com`
9. **Proxy status:** Proxied (pomarańczowa chmurka)
10. **TTL:** Auto
11. Kliknij **Save**
12. Poczekaj 5-10 minut na propagację

### Rozwiązanie 2: Sprawdź czy nie ma konfliktu z innymi rekordami

**Cloudflare Dashboard → DNS → Records**

**Sprawdź czy NIE MA:**
- A record dla `@` (root domain) - **KONFLIKT!**
- AAAA record (IPv6) - może powodować problemy
- Inne CNAME records dla `@`

**Jeśli są inne rekordy:**
1. Usuń wszystkie rekordy dla `@` oprócz CNAME
2. Zostaw tylko CNAME z Proxied

### Rozwiązanie 3: Wyłącz IPv6 w Cloudflare

**Cloudflare Dashboard → Network → IPv6 Compatibility**

1. Kliknij **Off** (wyłącz IPv6)
2. Poczekaj 2-3 minuty

**Dlaczego?**
- ALB używa tylko IPv4
- IPv6 może powodować problemy z DNS resolution

### Rozwiązanie 4: Wyłącz Cloudflare Proxy tymczasowo (test)

**To pomoże zdiagnozować czy problem jest z proxy czy z DNS:**

1. **Cloudflare Dashboard → DNS → Records**
2. Kliknij na rekord `@`
3. Zmień **Proxy status** na **DNS only** (szara chmurka)
4. Kliknij **Save**
5. Poczekaj 5 minut
6. Sprawdź: https://dnschecker.org/#CNAME/kongoapp.pl

**Jeśli teraz CNAME rozwiązują się:**
- Problem jest z Cloudflare Proxy
- Przejdź do Rozwiązania 5

**Jeśli nadal nie rozwiązują się:**
- Problem jest z DNS/nameservery
- Przejdź do Rozwiązania 6

### Rozwiązanie 5: Problem z Cloudflare Proxy - użyj A record (tymczasowo)

**⚠️ UWAGA:** To jest **tymczasowe rozwiązanie**. ALB ma dynamiczne IP, więc A record może przestać działać gdy ALB się zmieni.

**KROK 1: Pobierz IP ALB:**
```bash
nslookup forum-alb-1684129147.us-east-1.elb.amazonaws.com
```

**KROK 2: Dodaj A record w Cloudflare:**
1. **Cloudflare Dashboard → DNS → Records**
2. Usuń CNAME record dla `@`
3. Kliknij **Add record**
4. **Type:** A
5. **Name:** `@`
6. **IPv4 address:** (wklej pierwszy IP z nslookup, np. `54.158.162.197`)
7. **Proxy status:** Proxied (pomarańczowa chmurka)
8. **TTL:** Auto
9. Kliknij **Save**

**KROK 3: Test:**
- Poczekaj 2-3 minuty
- Sprawdź: `https://kongoapp.pl`

**Jeśli działa:**
- Problem był z CNAME resolution w Cloudflare
- Możesz zostawić A record (ale pamiętaj, że może przestać działać gdy ALB się zmieni)
- LUB spróbuj ponownie dodać CNAME po 24 godzinach (propagacja DNS)

### Rozwiązanie 6: Problem z Nameservery

**Jeśli CNAME nie rozwiązują się nawet z DNS only:**

1. **Sprawdź nameservery u rejestratora domeny:**
   - Idź do rejestratora (np. Freenom, Namecheap)
   - Sprawdź czy nameservery wskazują na Cloudflare
   - Powinny być np.:
     - `alice.ns.cloudflare.com`
     - `bob.ns.cloudflare.com`

2. **Sprawdź czy nameservery są poprawne:**
   ```bash
   nslookup -type=NS kongoapp.pl
   ```

   **Powinieneś zobaczyć Cloudflare nameservery**

3. **Jeśli nameservery są niepoprawne:**
   - Zmień je u rejestratora na Cloudflare nameservery
   - Poczekaj 24-48 godzin na propagację

### Rozwiązanie 7: Wyczyść Cloudflare Cache

**Cloudflare Dashboard → Caching → Purge Everything**

1. Kliknij **Purge Everything**
2. Poczekaj 2-3 minuty
3. Sprawdź ponownie: https://dnschecker.org/#CNAME/kongoapp.pl

---

## 🧪 Test po naprawie

1. **Sprawdź CNAME resolution:**
   - https://dnschecker.org/#CNAME/kongoapp.pl
   - Powinny być zielone ✓ (nie czerwone X)

2. **Test strony:**
   - Otwórz `https://kongoapp.pl`
   - Powinno działać (nie Error 521)

3. **Test z Cloudflare proxy:**
   - Cloudflare Dashboard → DNS → Records
   - Upewnij się, że Proxy status = **Proxied** (pomarańczowa chmurka)
   - Sprawdź czy działa `https://kongoapp.pl`

---

## 📋 Checklist

- [ ] Cloudflare widzi poprawny CNAME record
- [ ] Cloudflare DNS jest włączone
- [ ] ALB DNS rozwiązuje się (nslookup pokazuje IP)
- [ ] Nie ma konfliktujących rekordów (A, AAAA)
- [ ] IPv6 jest wyłączone w Cloudflare
- [ ] Nameservery wskazują na Cloudflare
- [ ] Cache Cloudflare wyczyszczony
- [ ] Poczekałeś 5-10 minut po zmianach

---

## 🆘 Jeśli nadal nie działa

### Opcja A: Użyj A record (tymczasowo)

Zobacz **Rozwiązanie 5** powyżej.

### Opcja B: Skontaktuj się z Cloudflare Support

1. Cloudflare Dashboard → **Help Center**
2. **Contact Support**
3. Opisz problem: "CNAME records not resolving globally, Error 521"

### Opcja C: Użyj Route 53 zamiast Cloudflare DNS

**AWS Route 53:**
1. Utwórz Hosted Zone dla `kongoapp.pl`
2. Dodaj A record (alias) wskazujący na ALB
3. Zmień nameservery u rejestratora na Route 53

**To jest bardziej niezawodne, ale kosztuje ~$0.50/miesiąc za hosted zone.**

---

**Ostatnia aktualizacja:** 2025-11-27

