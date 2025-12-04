# 📋 ALB Access Logs - Jak sprawdzić logi requestów

## 🔍 Gdzie sprawdzić logi requestów w AWS

### 1. ALB Access Logs (najbardziej szczegółowe)

**ALB Access Logs pokazują każdy request do ALB z pełnymi szczegółami.**

#### Włącz ALB Access Logs (jeśli nie są włączone):

1. **AWS Console → S3**
2. Utwórz bucket (lub użyj istniejący) dla logów:
   - **Bucket name:** `forum-alb-access-logs-[TWOJA-UNIKALNA-NAZWA]`
   - **Region:** `us-east-1`
   - **Block Public Access:** Zostaw zaznaczone (logi nie powinny być publiczne)
3. Kliknij **Create bucket**

4. **AWS Console → EC2 → Load Balancers → `forum-alb`**
5. Zakładka: **Attributes** → **Edit attributes**
6. Włącz **Access logs:**
   - **Enable access logs:** ☑️ Enabled
   - **S3 location:** `s3://forum-alb-access-logs-[TWOJA-UNIKALNA-NAZWA]/alb/`
   - Kliknij **Save changes**

⏳ **Poczekaj 5-10 minut** - logi mogą pojawić się z opóźnieniem.

#### Sprawdź ALB Access Logs:

1. **AWS Console → S3**
2. Kliknij na bucket: `forum-alb-access-logs-[TWOJA-UNIKALNA-NAZWA]`
3. Przejdź do: `alb/AWSLogs/311603531332/elasticloadbalancing/us-east-1/`
4. Wybierz datę (folder z datą)
5. Otwórz plik `.log` (możesz pobrać i otworzyć w edytorze tekstu)

**Format logów:**
```
type time client:port target:port request_processing_time target_processing_time response_processing_time elb_status_code target_status_code received_bytes sent_bytes "request" "user_agent" ssl_cipher ssl_protocol target_group_arn "trace_id" "domain" "chosen_cert_arn" matched_rule_priority request_creation_time "actions_executed" "redirect_url" "error_reason" "target:port_list" "target_status_code_list" "classification" "classification_reason"
```

**Przykład:**
```
http 2025-11-26T21:00:00.123456Z app/forum-alb/1234567890abcdef 104.21.44.121:12345 10.0.10.217:80 0.001 0.083 0.000 200 200 1234 5678 "GET https://kongoapp.pl/ HTTP/1.1" "Mozilla/5.0..." ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2 arn:aws:elasticloadbalancing:us-east-1:311603531332:targetgroup/forum-tg/abcdef "Root=1-12345678-abcdef" "kongoapp.pl" - 0 2025-11-26T21:00:00.123456Z "forward" "-" "-" "10.0.10.217:80" "200" "-" "-"
```

**Co sprawdzić:**
- **client:port** - IP Cloudflare (powinno być z zakresu Cloudflare IP)
- **elb_status_code** - kod odpowiedzi ALB (200 = OK, 502/503/504 = błąd)
- **target_status_code** - kod odpowiedzi z instancji (200 = OK)
- **request** - pełny request (URL, method, protocol)

---

### 2. CloudWatch Logs (jeśli masz CloudWatch agent na EC2)

1. **AWS Console → CloudWatch → Log groups**
2. Szukaj log groups związanych z ALB lub EC2
3. Kliknij na log group → **Log streams**
4. Wybierz stream i zobacz logi

**Jeśli nie masz log groups:**
- CloudWatch agent nie jest zainstalowany na EC2
- To jest opcjonalne, nie jest wymagane

---

### 3. Logi Nginx na instancjach EC2

**Przez Systems Manager Session Manager:**

```bash
# Sprawdź access logi Nginx
sudo tail -f /var/log/nginx/access.log

# Sprawdź error logi Nginx
sudo tail -f /var/log/nginx/error.log

# Sprawdź ostatnie 100 linii
sudo tail -n 100 /var/log/nginx/access.log
```

**Format logów Nginx:**
```
IP_ADDRESS - - [DATE] "METHOD /path HTTP/1.1" STATUS_CODE SIZE "REFERER" "USER_AGENT"
```

**Przykład:**
```
10.0.10.217 - - [26/Nov/2025:21:00:00 +0000] "GET /health HTTP/1.1" 200 7 "-" "ELB-HealthChecker/2.0"
104.21.44.121 - - [26/Nov/2025:21:00:01 +0000] "GET / HTTP/1.1" 200 1234 "https://kongoapp.pl" "Mozilla/5.0..."
```

**Co sprawdzić:**
- **IP_ADDRESS** - czy są requesty z Cloudflare IP (104.21.44.121, 172.67.199.149, itp.)
- **STATUS_CODE** - kod odpowiedzi (200 = OK, 404 = Not Found, 502 = Bad Gateway)
- **PATH** - jaki endpoint jest wywoływany

---

### 4. Logi Django na instancjach EC2

**Przez Systems Manager Session Manager:**

```bash
# Sprawdź logi Django kontenera
docker logs forum-backend --tail 100

# Sprawdź logi w czasie rzeczywistym
docker logs forum-backend -f

# Sprawdź logi z ostatnich 50 linii
docker logs forum-backend --tail 50
```

**Co sprawdzić:**
- Błędy Django (500, 502, 503)
- Błędy połączenia z bazą danych
- Błędy CORS
- Błędy ALLOWED_HOSTS

---

### 5. CloudWatch Metrics (już sprawdziłeś)

**AWS Console → CloudWatch → Dashboards**

Widziałeś już:
- **Requests:** 26 (ALB otrzymuje requesty)
- **Target 4XXs:** 17 (błędy 4XX z instancji)
- **ELB 4XXs:** 3 (błędy 4XX z ALB)
- **Target 5XXs:** Brak danych (brak błędów 5XX) ✅

---

## 🔍 Co sprawdzić w logach dla problemu 521

### W ALB Access Logs:

1. **Czy są requesty z Cloudflare IP?**
   - Cloudflare IP ranges: https://www.cloudflare.com/ips/
   - Jeśli NIE MA requestów z Cloudflare IP → Cloudflare nie dociera do ALB (problem z DNS/routingiem)

2. **Jaki jest elb_status_code?**
   - 200 = OK
   - 502/503/504 = błąd ALB
   - Jeśli są błędy 502/503/504 → problem z Target Group/instancjami

3. **Jaki jest target_status_code?**
   - 200 = OK
   - 4XX = błąd aplikacji (404, 403, itp.)
   - 5XX = błąd serwera (500, 502, itp.)

### W Nginx Access Logs:

1. **Czy są requesty z Cloudflare IP?**
   - Jeśli NIE MA → Cloudflare nie dociera do instancji (problem z ALB/Target Group)

2. **Jaki jest STATUS_CODE?**
   - 200 = OK
   - 404 = Not Found (może być problem z routingiem)
   - 502 = Bad Gateway (Django nie odpowiada)

---

## 🚀 Szybkie komendy do sprawdzenia logów

### Na instancji EC2 (przez Systems Manager):

```bash
# Nginx access logi (ostatnie 50 linii)
sudo tail -n 50 /var/log/nginx/access.log

# Nginx error logi (ostatnie 50 linii)
sudo tail -n 50 /var/log/nginx/error.log

# Django logi (ostatnie 50 linii)
docker logs forum-backend --tail 50

# Sprawdź czy Nginx działa
sudo systemctl status nginx

# Sprawdź czy Django kontener działa
docker ps | grep forum-backend
```

---

## 📊 Interpretacja wyników

### Jeśli w ALB Access Logs NIE MA requestów z Cloudflare IP:
- Problem z DNS/routingiem Cloudflare
- Cloudflare nie może rozwiązać DNS do ALB
- Sprawdź DNS Records w Cloudflare

### Jeśli w ALB Access Logs SĄ requesty z Cloudflare IP, ale elb_status_code = 502/503/504:
- Problem z Target Group/instancjami
- Sprawdź Target Group Health
- Sprawdź logi Nginx/Django na instancjach

### Jeśli w ALB Access Logs SĄ requesty z Cloudflare IP i elb_status_code = 200:
- ALB działa poprawnie
- Problem może być z Cloudflare cache lub konfiguracją Cloudflare

---

**Ostatnia aktualizacja:** 2025-11-26














