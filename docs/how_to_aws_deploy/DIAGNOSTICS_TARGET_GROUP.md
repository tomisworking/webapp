# 🔍 Diagnostyka: ERR_CONNECTION_REFUSED dla /api/categories/

## Problem
- `/health` działa ✅
- `/api/categories/` zwraca `ERR_CONNECTION_REFUSED` ❌

## Przyczyna
ALB nie przekierowuje ruchu do instancji, ponieważ:
1. Instancje są **unhealthy** w Target Group
2. Instancje **nie są zarejestrowane** w Target Group
3. **Health check** jest niepoprawnie skonfigurowany

---

## ✅ KROK 1: Sprawdź Target Group Health

1. **EC2 Console** → **Target Groups** → Wybierz `forum-tg`
2. Kliknij zakładkę **Targets**
3. **Sprawdź status** każdej instancji:
   - ✅ **Healthy** = wszystko OK
   - ❌ **Unhealthy** = problem!
   - ⏳ **Initial** = czeka na health check
   - ❌ **Unused** = nie jest używana przez ALB

### Jeśli instancje są **Unhealthy**:

**Sprawdź Health Check Settings:**
- **Health check path:** `/health` (MUSI być `/health`, nie `/api/health/`)
- **Health check protocol:** HTTP
- **Health check port:** Traffic port
- **Healthy threshold:** 2
- **Unhealthy threshold:** 2
- **Timeout:** 5 seconds
- **Interval:** 30 seconds
- **Success codes:** 200

**Jeśli ustawienia są złe:**
1. Kliknij **Edit** w sekcji Health check settings
2. Ustaw **Health check path:** `/health`
3. Kliknij **Save changes**

---

## ✅ KROK 2: Sprawdź czy instancje są zarejestrowane

**W Target Group → Targets:**
- Jeśli lista jest **pusta** → instancje nie są zarejestrowane!
- Jeśli są instancje, ale status to **Unused** → problem z ASG

**Jeśli instancje nie są zarejestrowane:**
1. **EC2 Console** → **Auto Scaling Groups** → `forum-asg`
2. Sprawdź **Activity** tab → czy są błędy
3. Sprawdź **Instances** tab → czy instancje są uruchomione
4. Jeśli instancje są, ale nie w Target Group:
   - **ASG** → **Edit** → **Health checks**
   - Upewnij się, że **Health check type:** ELB (nie EC2)
   - **Health check grace period:** 300 seconds
   - Kliknij **Update**

---

## ✅ KROK 3: Sprawdź Security Groups

**ALB Security Group (`forum-alb-sg`):**
- **Inbound:** Port 80 z `0.0.0.0/0` (HTTP)
- **Outbound:** Wszystko (0.0.0.0/0)

**EC2 Security Group (`forum-ec2-sg`):**
- **Inbound:** Port 80 z ALB Security Group (nie z 0.0.0.0/0!)
- **Outbound:** Wszystko (0.0.0.0/0)

**Sprawdź:**
1. **EC2** → **Security Groups** → `forum-alb-sg`
2. **Inbound rules:** Czy port 80 jest otwarty z `0.0.0.0/0`?
3. **EC2** → **Security Groups** → `forum-ec2-sg`
4. **Inbound rules:** Czy port 80 jest otwarty z `forum-alb-sg`?

**Jeśli nie:**
- Dodaj regułę: Port 80, Source = ALB Security Group ID

---

## ✅ KROK 4: Sprawdź ALB Listener

1. **EC2** → **Load Balancers** → `forum-alb`
2. Kliknij zakładkę **Listeners**
3. Sprawdź **Listener (HTTP:80)**:
   - **Default action:** Forward to `forum-tg`
   - **Status:** Enabled

**Jeśli są dodatkowe Rules:**
- Sprawdź czy nie ma reguły dla `/api/` która przekierowuje gdzie indziej
- Jeśli są, usuń je lub ustaw na Forward to `forum-tg`

---

## ✅ KROK 5: Test z instancji EC2

Połącz się przez **Systems Manager Session Manager** i wykonaj:

```bash
# 1. Sprawdź czy Nginx odpowiada lokalnie
curl -v http://127.0.0.1/health
curl -v http://127.0.0.1/api/categories/

# 2. Sprawdź logi Nginx
sudo tail -50 /var/log/nginx/error.log
sudo tail -20 /var/log/nginx/access.log

# 3. Sprawdź czy Django odpowiada
docker logs forum-backend --tail 50

# 4. Test bezpośrednio Django
curl -v http://127.0.0.1:8000/api/categories/
```

---

## ✅ KROK 6: Wymuś rejestrację instancji

Jeśli instancje są healthy lokalnie, ale nie w Target Group:

```bash
# Z AWS CLI (lub przez Console):
# 1. Zarejestruj instancję ręcznie w Target Group
aws elbv2 register-targets \
  --target-group-arn <TARGET_GROUP_ARN> \
  --targets Id=<INSTANCE_ID>

# 2. Sprawdź status
aws elbv2 describe-target-health \
  --target-group-arn <TARGET_GROUP_ARN>
```

**LUB przez Console:**
1. **Target Group** → **Targets** → **Register targets**
2. Wybierz instancje → **Include as pending below**
3. Kliknij **Register pending targets**

---

## ✅ KROK 7: Instance Refresh (jeśli wszystko inne zawodzi)

Jeśli instancje są stale unhealthy:

1. **EC2** → **Auto Scaling Groups** → `forum-asg`
2. **Actions** → **Start instance refresh**
3. **Minimum healthy percentage:** 50%
4. **Instance warmup:** 300 seconds
5. Kliknij **Start instance refresh**

To zastąpi wszystkie instancje nowymi z poprawną konfiguracją.

---

## 📋 Checklist

- [ ] Target Group health check path = `/health`
- [ ] Instancje są zarejestrowane w Target Group
- [ ] Status instancji = **Healthy** (nie Unhealthy)
- [ ] Security Groups pozwalają na ruch ALB → EC2
- [ ] ALB Listener ma default action = Forward to `forum-tg`
- [ ] Nginx odpowiada lokalnie na `/health` i `/api/categories/`
- [ ] Django container jest healthy (`docker ps`)

---

## 🚨 Najczęstsze rozwiązania

### Problem: Instancje są Unhealthy
**Rozwiązanie:** 
- Sprawdź health check path = `/health` (nie `/api/health/`)
- Sprawdź czy Nginx odpowiada: `curl http://127.0.0.1/health`

### Problem: Instancje nie są zarejestrowane
**Rozwiązanie:**
- ASG → Edit → Health checks → Type = ELB (nie EC2)
- Wykonaj Instance Refresh

### Problem: Security Groups blokują ruch
**Rozwiązanie:**
- EC2 SG → Inbound → Port 80 z ALB SG (nie z 0.0.0.0/0)

---

## 📞 Jeśli nadal nie działa

Prześlij:
1. Screenshot Target Group → Targets (status instancji)
2. Screenshot Target Group → Health check settings
3. Output z: `curl -v http://127.0.0.1/health` i `curl -v http://127.0.0.1/api/categories/`
4. Output z: `docker ps | grep forum-backend`














