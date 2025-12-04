# 🔒 HTTPS między Cloudflare a ALB - Konfiguracja

**Cel:** Skonfigurować HTTPS między Cloudflare a ALB (end-to-end encryption).

---

## 📋 Wymagania

- ✅ Domena `kongoapp.pl` już w Cloudflare
- ✅ ALB już utworzony (`forum-alb`)
- ✅ Security Group ALB już pozwala na HTTPS (port 443) ✅

---

## 🔐 KROK 1: Utwórz certyfikat SSL w AWS Certificate Manager (ACM)

### 1.1. Przejdź do Certificate Manager

1. AWS Console → Wyszukaj: **Certificate Manager** (lub **ACM**)
2. Upewnij się, że jesteś w regionie: **us-east-1** ⚠️ WAŻNE!
3. Kliknij: **Request a certificate**

### 1.2. Request public certificate

**Certificate type:**
- Wybierz: **Request a public certificate**
- Kliknij **Next**

**Domain names:**
- **Fully qualified domain name:** `kongoapp.pl`
- Kliknij **Add another name to this certificate**
- **Fully qualified domain name:** `www.kongoapp.pl`
- Kliknij **Next**

**Validation method:**
- Wybierz: **DNS validation** (zalecane)
- Kliknij **Next**

**Tags:**
- Opcjonalne, możesz pominąć
- Kliknij **Next**

**Review:**
- Sprawdź domeny: `kongoapp.pl`, `www.kongoapp.pl`
- Kliknij **Confirm and request**

### 1.3. Zweryfikuj domenę (DNS validation)

**ACM pokaże CNAME records do dodania w Cloudflare:**

1. Skopiuj **Name** i **Value** z każdego CNAME record
2. Idź do **Cloudflare Dashboard → DNS → Records**
3. Kliknij **Add record**
4. Dla każdego CNAME z ACM:
   - **Type:** CNAME
   - **Name:** (wklej Name z ACM, np. `_abc123.kongoapp.pl`)
   - **Target:** (wklej Value z ACM, np. `_xyz789.acm-validations.aws.`)
   - **Proxy status:** DNS only (szara chmurka) ⚠️ WAŻNE!
   - **TTL:** Auto
   - Kliknij **Save**

5. Wróć do **ACM → Certificates**
6. Poczekaj 5-10 minut aż status zmieni się na **Issued** ✅

**💾 ZAPISZ Certificate ARN** (będzie potrzebny w następnym kroku)

---

## ⚖️ KROK 2: Dodaj HTTPS Listener do ALB

### 2.1. Przejdź do ALB

1. AWS Console → **EC2 → Load Balancers**
2. Kliknij na `forum-alb`
3. Zakładka: **Listeners**
4. Kliknij **Add listener**

### 2.2. Konfiguracja HTTPS Listener

**Protocol & Port:**
- **Protocol:** HTTPS
- **Port:** 443

**Default action:**
- **Action type:** Forward to
- **Target group:** `forum-tg`
- **Weight:** 1

**Security policy:**
- Zostaw domyślne (ELBSecurityPolicy-TLS13-1-2-2021-06)

**Default SSL certificate:**
- **From:** Certificate Manager (ACM)
- **Certificate:** Wybierz certyfikat dla `kongoapp.pl` (ten który właśnie utworzyłeś)
- **Certificate name:** Powinno pokazać `kongoapp.pl`

**Additional certificates:**
- Opcjonalne, możesz pominąć

Kliknij **Add**

⏳ Poczekaj 1-2 minuty aż listener będzie **Active**

---

## 🔄 KROK 3: Dodaj redirect HTTP → HTTPS (opcjonalne, ale zalecane)

### 3.1. Edytuj HTTP Listener

1. W zakładce **Listeners**, znajdź HTTP listener (port 80)
2. Kliknij **Edit**

### 3.2. Zmień action na Redirect

**Default action:**
- **Action type:** Zmień z "Forward to" na **Redirect to URL**
- **Protocol:** HTTPS
- **Port:** 443
- **Status code:** 301 - Permanently moved

Kliknij **Save changes**

**Teraz wszystkie requesty HTTP będą automatycznie przekierowane na HTTPS!**

---

## ☁️ KROK 4: Zmień Cloudflare SSL/TLS Mode na "Full (strict)"

### 4.1. Cloudflare Dashboard

1. Cloudflare Dashboard → Wybierz domenę `kongoapp.pl`
2. Zakładka: **SSL/TLS**
3. Sekcja: **SSL/TLS encryption mode**

### 4.2. Zmień na Full (strict)

- Wybierz: **Full (strict)**
- Cloudflare automatycznie zapisze zmiany

**Dlaczego "Full (strict)":**
- Wymaga ważnego certyfikatu SSL na origin (ALB)
- Teraz mamy certyfikat z ACM ✅
- Zapewnia end-to-end encryption

---

## ✅ KROK 5: Weryfikacja

### 5.1. Test HTTPS bezpośrednio na ALB

**Otwórz w przeglądarce:**
```
https://forum-alb-1684129147.us-east-1.elb.amazonaws.com
```

**Powinieneś zobaczyć:**
- ✅ Stronę React Forum
- ✅ Kłódkę SSL w przeglądarce (certyfikat z ACM)

### 5.2. Test przez Cloudflare

**Otwórz w przeglądarce:**
```
https://kongoapp.pl
```

**Powinieneś zobaczyć:**
- ✅ Stronę React Forum
- ✅ Kłódkę SSL w przeglądarce
- ✅ Brak błędów SSL

### 5.3. Test redirect HTTP → HTTPS

**Otwórz w przeglądarce:**
```
http://kongoapp.pl
```

**Powinieneś zostać automatycznie przekierowany na:**
```
https://kongoapp.pl
```

---

## 🔍 Troubleshooting

### Problem: Certyfikat nie jest "Issued"

**Sprawdź:**
1. Czy dodałeś CNAME records w Cloudflare?
2. Czy Proxy status jest "DNS only" (szara chmurka) dla CNAME validation?
3. Poczekaj 5-10 minut na propagację DNS

### Problem: "Certificate not found" w ALB Listener

**Sprawdź:**
1. Czy certyfikat jest w regionie **us-east-1**? (ALB musi być w tym samym regionie)
2. Czy certyfikat ma status "Issued"?
3. Czy wybrałeś poprawny certyfikat w ALB Listener?

### Problem: Cloudflare błąd 526 (Invalid SSL certificate)

**Sprawdź:**
1. Czy certyfikat jest ważny (nie wygasł)?
2. Czy certyfikat obejmuje domenę `kongoapp.pl`?
3. Czy ALB HTTPS listener jest "Active"?

### Problem: Mixed Content warnings

**To jest normalne** - frontend może ładować zasoby przez HTTP. Jeśli chcesz to naprawić:
- Upewnij się, że wszystkie requesty w React używają HTTPS
- Sprawdź `REACT_APP_API_URL` w `.env.production`

---

## 📊 Porównanie: HTTP vs HTTPS między Cloudflare a ALB

| Aspekt | HTTP (obecna konfiguracja) | HTTPS (po tej konfiguracji) |
|--------|----------------------------|------------------------------|
| **Cloudflare → ALB** | HTTP (port 80) | HTTPS (port 443) |
| **Cloudflare SSL/TLS Mode** | Full | Full (strict) |
| **Certyfikat na ALB** | Nie wymagany | Wymagany (ACM) |
| **Bezpieczeństwo** | ✅ HTTPS użytkownik ↔ Cloudflare<br>⚠️ HTTP Cloudflare ↔ ALB | ✅ HTTPS end-to-end |
| **Koszt** | Darmowe | Darmowe (ACM certyfikaty są darmowe) |
| **Złożoność** | Prosta | Średnia (wymaga certyfikatu) |

---

## 🎯 Zalety HTTPS między Cloudflare a ALB

1. **End-to-end encryption** - cała komunikacja jest szyfrowana
2. **Lepsze bezpieczeństwo** - dane nie są przesyłane w plain text między Cloudflare a ALB
3. **Compliance** - niektóre standardy wymagają end-to-end encryption
4. **Full (strict) mode** - Cloudflare weryfikuje certyfikat origin

---

## ⚠️ Uwagi

1. **Region ACM:** Certyfikat MUSI być w regionie **us-east-1** (ten sam co ALB)
2. **DNS Validation:** CNAME records w Cloudflare MUSZĄ mieć Proxy status = "DNS only"
3. **Propagacja:** Zmiany mogą zająć 5-10 minut
4. **Koszt:** Certyfikaty ACM są darmowe, ale ALB HTTPS listener nie ma dodatkowych kosztów

---

**Ostatnia aktualizacja:** 2025-11-26














