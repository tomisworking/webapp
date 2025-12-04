# Prezentacja Architektury AWS - Forum Kongoapp.pl

## Przewodnik Narracyjny do Prezentacji

---

## 1. Wprowadzenie - Czym jest ten projekt?

Zbudowałem w pełni funkcjonalne forum internetowe z wykorzystaniem nowoczesnego stosu technologicznego i infrastruktury AWS. Aplikacja składa się z trzech głównych warstw: React frontend do interfejsu użytkownika, Django REST API jako backend, oraz PostgreSQL jako baza danych. Całość została wdrożona na AWS z wykorzystaniem Auto Scaling i Load Balancing, co zapewnia wysoką dostępność i skalowalność.

Głównym celem było stworzenie production-ready aplikacji, która może obsługiwać ruch z internetu, automatycznie skalować się w zależności od obciążenia, oraz być odporna na awarie dzięki rozmieszczeniu w wielu Availability Zones.

---

## 2. Flow Aplikacji - Jak użytkownik korzysta z forum i jak system reaguje

### Scenariusz 1: Normalne użytkowanie - mały ruch

Wyobraźmy sobie typowego użytkownika, który otwiera forum po raz pierwszy. Wpisuje w przeglądarce `kongoapp.pl` i naciska Enter.

**Krok 1: Pierwszy kontakt z Cloudflare**
Przeglądarka wysyła request do Cloudflare - pierwszej warstwy infrastruktury. Cloudflare działa jak inteligentny bramkarz: sprawdza czy request nie jest atakiem, automatycznie zapewnia certyfikat SSL (użytkownik widzi kłódkę w przeglądarce), a jeśli użytkownik już wcześniej odwiedzał stronę, Cloudflare może mu zwrócić zapisane w cache statyczne pliki (JavaScript, CSS) z lokalnego serwera w jego kraju - to przyspiesza ładowanie nawet 10-krotnie.

**Krok 2: Load Balancer decyduje gdzie skierować request**
Jeśli Cloudflare nie ma strony w cache (pierwsza wizyta lub dynamiczna zawartość), request trafia do Application Load Balancer w AWS. ALB to jak inteligentny dyspozytor - widzi że mam 2 działające instancje i musi wybrać jedną. Używa algorytmu "round-robin" - pierwszy request idzie do instancji A, drugi do instancji B, trzeci znowu do A, i tak dalej. To zapewnia równomierne obciążenie obu maszyn.

**Krok 3: Instancja obsługuje request**
Wybrana instancja EC2 otrzymuje request. Na tej maszynie działa Nginx - serwer, który decyduje co zrobić z requestem. Jeśli użytkownik chce zobaczyć listę kategorii forum, Nginx przekierowuje request do Django (backend API), które pobiera dane z bazy PostgreSQL i zwraca JSON. Jeśli użytkownik chce zobaczyć stronę główną, Nginx po prostu serwuje statyczne pliki React (HTML, JavaScript) które już są na dysku.

**Krok 4: Odpowiedź wraca do użytkownika**
Dane płyną z powrotem: PostgreSQL → Django → Nginx → ALB → Cloudflare → przeglądarka użytkownika. Cały proces trwa zazwyczaj 100-200 milisekund. Użytkownik widzi forum i może zacząć korzystać.

### Scenariusz 2: Wzrost ruchu - jak system automatycznie się skaluje

Teraz wyobraźmy sobie, że forum staje się popularne. Rano było 10 użytkowników jednocześnie, a teraz jest 200. Co się dzieje?

**Monitoring obciążenia**
Auto Scaling Group (ASG) nieustannie monitoruje metryki wszystkich instancji. Sprawdza:
- **CPU utilization** - ile procent procesora jest wykorzystane
- **Network traffic** - ile danych przychodzi i wychodzi
- **Request count** - ile requestów na sekundę obsługuje każda instancja

W mojej konfiguracji mam ustawione:
- **Minimum:** 1 instancja (aplikacja nigdy się nie wyłączy)
- **Desired:** 2 instancje (normalny stan - dla redundancji)
- **Maximum:** 4 instancje (maksymalna liczba przy dużym ruchu)

**Proces skalowania w górę (Scale Up)**
Gdy ASG zauważa, że CPU na obu instancjach przekracza 70% przez dłuższy czas (np. 5 minut), uruchamia proces skalowania:

1. **Decyzja:** "Potrzebuję więcej mocy obliczeniowej"
2. **Akcja:** ASG uruchamia trzecią instancję używając Launch Template
3. **Setup:** Nowa instancja automatycznie wykonuje skrypt user-data:
   - Instaluje Docker i Nginx
   - Pobiera najnowszy obraz Django z ECR
   - Pobiera frontend z S3
   - Konfiguruje wszystko automatycznie
4. **Weryfikacja:** ALB zaczyna wysyłać health checks do nowej instancji
5. **Gotowość:** Po 2-3 minutach nowa instancja jest gotowa i ALB zaczyna do niej kierować ruch
6. **Rezultat:** Teraz mam 3 instancje, każda obsługuje ~67 użytkowników zamiast 2 instancje po 100 użytkowników

**Load Balancer automatycznie rozdziela ruch**
ALB natychmiast zauważa nową instancję i zaczyna do niej kierować część ruchu. Teraz zamiast "round-robin" między 2 instancjami, robi to między 3. Obciążenie na każdej maszynie spada, CPU wraca do normalnego poziomu (np. 50%), a użytkownicy nie zauważają żadnej różnicy - wszystko działa płynnie.

### Scenariusz 3: Szczyt ruchu - maksymalne obciążenie

Forum staje się naprawdę popularne - 500 użytkowników jednocześnie! System reaguje:

**Kolejne skalowanie**
ASG widzi że 3 instancje są przeciążone (CPU > 80%), więc uruchamia czwartą instancję. Teraz mam maksymalną liczbę instancji (4), każda obsługuje ~125 użytkowników. ALB automatycznie rozdziela ruch między wszystkie 4 maszyny.

**Co jeśli to nie wystarczy?**
Jeśli nawet 4 instancje nie wystarczą (np. 1000+ użytkowników), mogę:
- Zwiększyć **Maximum** w ASG (np. do 8 instancji)
- Zmienić typ instancji z t3.micro na większy (np. t3.small lub t3.medium)
- Dodać caching (Redis) żeby zmniejszyć obciążenie bazy danych

### Scenariusz 4: Spadek ruchu - automatyczne skalowanie w dół (Scale Down)

Wieczorem ruch spada - z 500 użytkowników do 50. System automatycznie reaguje:

**Proces skalowania w dół**
ASG monitoruje że CPU na wszystkich instancjach spadło poniżej 30% i utrzymuje się tak przez dłuższy czas (np. 15 minut). To sygnał że nie potrzebuję tylu maszyn.

1. **Decyzja:** "Mam za dużo mocy obliczeniowej, mogę oszczędzić koszty"
2. **Akcja:** ASG oznacza jedną z instancji jako "do usunięcia"
3. **Graceful shutdown:** ALB przestaje kierować nowy ruch do tej instancji, ale pozwala dokończyć istniejące requesty
4. **Terminacja:** Po kilku minutach instancja jest bezpiecznie wyłączona
5. **Rezultat:** Wracam do 3 instancji, a potem (jeśli ruch dalej spada) do 2

**Dlaczego to ważne?**
Skalowanie w dół oszczędza koszty - nie płacę za nieużywane maszyny. W AWS płacisz za każdą godzinę działania instancji, więc jeśli mam 4 instancje przez 8 godzin zamiast 2 przez 24 godziny, oszczędzam ~$10 dziennie.

### Scenariusz 5: Awaria instancji - automatyczne naprawianie (Self-Healing)

Co się dzieje gdy jedna z instancji się zawiesza lub przestaje odpowiadać?

**Wykrywanie problemu**
ALB co 30 sekund wysyła health check do każdej instancji - prosty request do `/api/health/` który sprawdza czy Django i baza danych działają. Jeśli instancja nie odpowie dwa razy z rzędu (60 sekund), ALB oznacza ją jako "unhealthy".

**Automatyczna reakcja**
1. **ALB:** Przestaje kierować ruch do chorej instancji
2. **ASG:** Zauważa że instancja jest unhealthy
3. **Terminacja:** ASG automatycznie wyłącza złą instancję
4. **Zastąpienie:** ASG natychmiast uruchamia nową instancję (używając Launch Template)
5. **Setup:** Nowa instancja automatycznie się konfiguruje (2-3 minuty)
6. **Gotowość:** ALB weryfikuje że nowa instancja działa i zaczyna do niej kierować ruch

**Rezultat dla użytkownika**
Użytkownicy nie zauważają awarii! ALB automatycznie przekierował ich na działające instancje. Maksymalny czas "przerwy" to te 2-3 minuty gdy nowa instancja się uruchamia, ale w tym czasie pozostałe instancje obsługują cały ruch. To tzw. "self-healing" - system sam się naprawia bez interwencji człowieka.

### Podsumowanie flow - dlaczego to działa

Cały system jest zaprojektowany tak, żeby:
- **Użytkownik nie zauważał** co się dzieje w tle - zawsze widzi działającą stronę
- **System automatycznie reagował** na zmiany obciążenia - więcej użytkowników = więcej maszyn
- **Koszty były optymalne** - mniej użytkowników = mniej maszyn
- **Aplikacja była zawsze dostępna** - awaria jednej maszyny nie zatrzymuje całego forum

To wszystko dzieje się automatycznie, bez mojej interwencji. Mogę spać spokojnie wiedząc, że system sam zarządza zasobami i naprawia problemy.

### Struktura sieci VPC

Cała infrastruktura znajduje się w dedykowanym Virtual Private Cloud (VPC) o nazwie "forum-vpc" z blokiem CIDR 10.0.0.0/16. VPC to zasadniczo nasza prywatna, odizolowana sieć w chmurze AWS.

W ramach tego VPC stworzyłem 6 subnetów rozdzielonych na trzy kategorie:

**Public subnets (10.0.1.0/24 i 10.0.2.0/24)** - tutaj znajduje się Application Load Balancer. Te subnety mają route do Internet Gateway, co oznacza, że zasoby w nich mogą być dostępne z internetu. Każdy z tych subnetów jest w innej Availability Zone (us-east-1a i us-east-1b), co zapewnia redundancję.

**Private subnets (10.0.10.0/24 i 10.0.11.0/24)** - tutaj znajdują się instancje EC2 z aplikacją. Te subnety mają route do NAT Gateway zamiast Internet Gateway. NAT Gateway pozwala instancjom inicjować połączenia wychodzące do internetu (np. żeby pobrać pakiety, Docker images), ale blokuje połączenia przychodzące z internetu. Także te subnety są rozproszone między dwie Availability Zones.

**Database subnets (10.0.20.0/24 i 10.0.21.0/24)** - tutaj znajduje się RDS PostgreSQL. Te subnety są jeszcze bardziej izolowane i komunikują się tylko z private subnets. RDS automatycznie replikuje dane między strefami dla redundancji.

---

## 3. Struktura sieci VPC - Jak infrastruktura jest zorganizowana

Cała infrastruktura znajduje się w dedykowanym Virtual Private Cloud (VPC) o nazwie "forum-vpc" z blokiem CIDR 10.0.0.0/16. VPC to zasadniczo nasza prywatna, odizolowana sieć w chmurze AWS.

W ramach tego VPC stworzyłem 6 subnetów rozdzielonych na trzy kategorie:

**Public subnets (10.0.1.0/24 i 10.0.2.0/24)** - tutaj znajduje się Application Load Balancer. Te subnety mają route do Internet Gateway, co oznacza, że zasoby w nich mogą być dostępne z internetu. Każdy z tych subnetów jest w innej Availability Zone (us-east-1a i us-east-1b), co zapewnia redundancję.

**Private subnets (10.0.10.0/24 i 10.0.11.0/24)** - tutaj znajdują się instancje EC2 z aplikacją. Te subnety mają route do NAT Gateway zamiast Internet Gateway. NAT Gateway pozwala instancjom inicjować połączenia wychodzące do internetu (np. żeby pobrać pakiety, Docker images), ale blokuje połączenia przychodzące z internetu. Także te subnety są rozproszone między dwie Availability Zones.

**Database subnets (10.0.20.0/24 i 10.0.21.0/24)** - tutaj znajduje się RDS PostgreSQL. Te subnety są jeszcze bardziej izolowane i komunikują się tylko z private subnets. RDS automatycznie replikuje dane między strefami dla redundancji.

---

## 4. Bezpieczeństwo - Jak aplikacja jest chroniona

### Security Groups - firewall na poziomie instancji

Security Groups to wirtualne firewall'e, które kontrolują ruch sieciowy do i z zasobów AWS. Zaimplementowałem trzy Security Groups:

**forum-alb-sg** (dla Application Load Balancer):
- **Inbound:** Pozwala HTTP (port 80) i HTTPS (port 443) z całego internetu (0.0.0.0/0)
- **Outbound:** Pozwala cały ruch wychodzący
- To jest publiczny punkt wejścia do aplikacji

**forum-ec2-sg** (dla instancji EC2):
- **Inbound:** Pozwala HTTP (port 80) TYLKO z forum-alb-sg
- To jest tzw. "security group reference" - zamiast podawać zakres IP, wskazuję konkretny Security Group
- Oznacza to, że tylko ALB może wysyłać requesty HTTP do instancji
- Dodatkowo pozwala SSH (port 22) z mojego IP dla administracji
- **Outbound:** Pozwala cały ruch (potrzebny do połączenia z RDS, pobierania z ECR/S3)

**forum-rds-sg** (dla bazy danych RDS):
- **Inbound:** Pozwala PostgreSQL (port 5432) TYLKO z forum-ec2-sg
- Oznacza to, że tylko instancje EC2 mogą łączyć się z bazą danych
- **Outbound:** Domyślny

To tzw. "defense in depth" - wiele warstw bezpieczeństwa. Nawet jeśli ktoś zhackuje ALB, nie może bezpośrednio dostać się do bazy danych. Musiałby najpierw przejąć kontrolę nad instancją EC2.

### IAM Role i zarządzanie sekretami

Instancje EC2 mają przypisaną rolę IAM o nazwie "forum-ec2-role", która nadaje im uprawnienia do:
- Pobierania obrazów Docker z ECR
- Odczytu plików z S3 (frontend builds)
- Odczytu parametrów z Systems Manager Parameter Store
- Wysyłania logów do CloudWatch
- Połączenia przez Session Manager (bezpieczny SSH)

Wszystkie sekrety (klucze, hasła, connection strings) są przechowywane w AWS Systems Manager Parameter Store, nie w kodzie. Gdy instancja się uruchamia, user-data script pobiera te parametry używając AWS CLI i IAM role. Dzięki temu nie ma żadnych sekretów zapisanych na dysku w plain text ani w zmiennych środowiskowych widocznych dla innych procesów.

---

## 5. Proces Deployment - Jak wdrażam nowe wersje

### Build i Push

Gdy chcę wdrożyć nowe wersje aplikacji, wykonuję dwa kroki:

**Backend:**
1. Buduję obraz Docker lokalnie: `docker build -t forum-backend .`
2. Taguję obraz: `docker tag forum-backend:latest 311603531332.dkr.ecr.us-east-1.amazonaws.com/forum-backend:latest`
3. Pushuję do ECR: `docker push ...`

**Frontend:**
1. Buduję produkcyjną wersję React: `npm run build`
2. Upload'uję do S3: `aws s3 sync build/ s3://forum-frontend-builds-kongoapp/latest/ --delete`
   - Flag `--delete` zapewnia, że stare pliki JS zostaną usunięte

### Instance Refresh - Zero-downtime deployment

Instance Refresh to proces, który zastępuje wszystkie instancje w ASG nowymi instancjami używającymi najnowszego Launch Template.

Wybrałem strategię "Prioritize availability", która działa następująco:

1. **Faza 1:** ASG uruchamia nową instancję (teraz mamy 3 instancje: 2 stare + 1 nowa)
2. Nowa instancja wykonuje user-data script (instaluje wszystko, pobiera najnowsze obrazy z ECR i S3)
3. Po około 2-3 minutach nowa instancja jest gotowa
4. ALB zaczyna health checks na nowej instancji
5. Po 2 udanych health checks (60 sekund) ALB oznacza ją jako "healthy"
6. Instance warmup period (60 sekund) - dodatkowy czas na "rozgrzanie"
7. **Faza 2:** ASG terminuje jedną ze starych instancji (teraz: 1 stara + 1 nowa + 1 w procesie)
8. Powtarza kroki 1-7 dla drugiej instancji
9. **Faza 3:** Wszystkie instancje zaktualizowane, ASG wraca do desired capacity (2)

Kluczowe jest to, że w każdym momencie mamy przynajmniej 2 działające instancje obsługujące ruch. To zapewnia "zero-downtime deployment" - użytkownicy nie zauważają przerwy w dostępności.

---

## 6. Cloudflare Integration - SSL, CDN i bezpieczeństwo

Cloudflare pełni kilka ważnych ról:

### DNS Management
Cloudflare jest authoritative DNS serverem dla domeny kongoapp.pl. Początkowo próbowałem używać CNAME records wskazujących na DNS ALB, ale napotkałem problemy z propagacją DNS. Rozwiązaniem było użycie A records bezpośrednio wskazujących na IP Cloudflare proxy, które następnie przekazują ruch do ALB.

### SSL/TLS Termination
Cloudflare automatycznie zapewnia certyfikat SSL/TLS dla domeny. Konfiguracja SSL/TLS Mode jest ustawiona na "Full", co oznacza:
- Użytkownik → Cloudflare: HTTPS (szyfrowane)
- Cloudflare → ALB: HTTP (nieszyfrowane, ale w zaufanej sieci AWS)

Początkowo próbowałem "Full (strict)", co wymagałoby certyfikatu SSL także na ALB, ale to komplikowało konfigurację. "Full" mode jest wystarczający, ponieważ połączenie Cloudflare-ALB odbywa się w backbone'ie AWS, który jest bezpieczny.

### CDN i Cache
Cloudflare cache'uje statyczne zasoby (JS, CSS, obrazy) na swoich edge serverach na całym świecie. To oznacza, że użytkownik z Polski otrzyma pliki z serwera Cloudflare w Warszawie, a nie z us-east-1 w Virginii, co znacznie przyspiesza ładowanie.

### WAF i DDoS Protection
Cloudflare automatycznie filtruje złośliwy ruch, ataki SQL injection, XSS, i inne. Dodatkowo chroni przed atakami DDoS - jeśli ktoś spróbuje zalać moją stronę milionami requestów, Cloudflare to zablokuje zanim dotrze do AWS.

---

## 7. Szczegóły techniczne aplikacji

### Frontend - React SPA

Frontend to Single Page Application zbudowana w React. Po zbudowaniu (`npm run build`) otrzymuję statyczne pliki HTML, CSS, i JavaScript. Te pliki są upload'owane do S3, a następnie pobierane przez instancje EC2 podczas user-data script.

Kluczowa decyzja: `REACT_APP_API_URL=/api`

Używam relative URL zamiast pełnego `https://kongoapp.pl/api`. Dzięki temu:
- Frontend automatycznie używa tej samej domeny i protokołu co strona
- Brak problemów z Mixed Content (HTTPS frontend → HTTP API)
- Brak problemów z CORS
- Działa zarówno przez Cloudflare jak i bezpośrednio przez ALB

### Backend - Django REST API

Django działa w kontenerze Docker na porcie 8000. Container jest zbudowany z multi-stage Dockerfile, który:
1. Używa Python 3.11 slim jako base image
2. Instaluje dependencies z requirements.txt
3. Kopiuje kod aplikacji
4. Ustawia non-root użytkownika "django" (bezpieczeństwo)
5. Uruchamia Gunicorn z 3 workerami

Django używa django-environ do zarządzania zmiennymi środowiskowymi. Wszystkie konfiguracje (SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS) są przekazywane jako env vars podczas `docker run`.

Ważne ustawienia:
- `DEBUG=False` - w produkcji debug musi być wyłączony
- `ALLOWED_HOSTS` - zawiera DNS ALB i domenę kongoapp.pl
- `CORS_ALLOWED_ORIGINS` - zawiera zarówno HTTP jak HTTPS wersje domeny (dla Cloudflare proxy i direct access)
- `COOKIE_SECURE=False` - cookies nie wymagają HTTPS, ponieważ komunikacja ALB→EC2 jest HTTP
- `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` - Django rozpoznaje że oryginalny request był HTTPS na podstawie headera od Nginx

### Database - RDS PostgreSQL

Używam managed PostgreSQL z RDS. Zalety:
- Automatyczne backupy (7 dni retention)
- Automatyczne minor version updates
- Multi-AZ redundancja
- Managed przez AWS (nie muszę ręcznie instalować, konfigurować)

Connection string jest przechowywany w Parameter Store i przekazywany do Django jako DATABASE_URL.

---

## 8. Monitoring i Debugging

### CloudWatch Metrics
AWS automatycznie zbiera metryki:
- CPU utilization instancji EC2
- Network in/out
- ALB request count, latency, HTTP response codes
- RDS connections, CPU, storage

### CloudWatch Logs - Jak sprawdzić logi aplikacji

CloudWatch Logs to centralne miejsce gdzie możesz zobaczyć wszystkie logi z aplikacji bez logowania się na instancje.

#### 1. ALB Access Logs (logi Application Load Balancer)

**Gdzie znaleźć:**
1. AWS Console → **S3** → znajdź bucket z ALB access logs (zwykle nazwa zawiera "alb-access-logs")
2. Struktura: `AWSLogs/[Account-ID]/elasticloadbalancing/[region]/[year]/[month]/[day]/`
3. Pliki są w formacie tekstowym, jeden request = jedna linia

**Co zawierają:**
- IP użytkownika (przez Cloudflare)
- URL który został wywołany
- Kod odpowiedzi (200, 404, 500, itp.)
- Czas odpowiedzi
- Target (która instancja obsłużyła request)

**Jak używać:**
- Sprawdź czy Cloudflare dociera do ALB (szukaj IP z zakresu Cloudflare)
- Zobacz które endpointy są najczęściej wywoływane
- Znajdź błędy (kody 4XX, 5XX)

#### 2. CloudWatch Log Groups (jeśli masz CloudWatch Agent)

**Gdzie znaleźć:**
1. AWS Console → **CloudWatch** → **Log groups**
2. Szukaj log groups związanych z aplikacją (np. `/aws/ec2/forum-nginx`, `/aws/ec2/forum-django`)

**Jak skonfigurować (opcjonalnie):**
CloudWatch Agent można zainstalować na instancjach EC2, żeby automatycznie wysyłał logi do CloudWatch. Obecnie nie jest to skonfigurowane, ale można to dodać.

**Jak używać:**
- Kliknij na log group → **Log streams**
- Wybierz stream (każda instancja ma swój stream)
- Zobacz logi w czasie rzeczywistym lub przeszukaj historyczne logi

#### 3. Logi na instancjach EC2 (przez Systems Manager Session Manager)

**Jak się połączyć:**
1. AWS Console → **EC2** → **Instances**
2. Wybierz instancję → **Connect** → **Session Manager** → **Connect**
3. Otworzy się terminal w przeglądarce

**Główne lokalizacje logów:**

**User-data logs** (skrypt inicjalizacyjny):
```bash
sudo cat /var/log/user-data.log
```
Pokazuje co się działo podczas pierwszego uruchomienia instancji - instalacja Docker, Nginx, pobieranie obrazów z ECR, itp.

**Docker logs** (logi Django):
```bash
docker logs forum-backend --tail 100
docker logs forum-backend -f  # w czasie rzeczywistym
```
Pokazuje logi Django/Gunicorn - wszystkie requesty do API, błędy, połączenia z bazą danych.

**Nginx access logs** (wszystkie requesty):
```bash
sudo tail -n 100 /var/log/nginx/access.log
sudo tail -f /var/log/nginx/access.log  # w czasie rzeczywistym
```
Pokazuje każdy request który trafił do Nginx - IP, URL, kod odpowiedzi, czas.

**Nginx error logs** (błędy):
```bash
sudo tail -n 100 /var/log/nginx/error.log
```
Pokazuje błędy Nginx - problemy z proxy do Django, timeouty, itp.

#### 4. CloudWatch Insights - Zaawansowane przeszukiwanie logów

CloudWatch Insights pozwala przeszukiwać logi używając zapytań SQL-like.

**Przykładowe zapytania:**

Znajdź wszystkie błędy 500:
```
fields @timestamp, @message
| filter @message like /500/
| sort @timestamp desc
```

Znajdź requesty z konkretnego IP:
```
fields @timestamp, @message
| filter @message like /104.21.44.121/
| sort @timestamp desc
```

Statystyki requestów na godzinę:
```
fields @timestamp
| stats count() by bin(1h)
```

### AWS Systems Manager Session Manager
Zamiast tradycyjnego SSH, używam Session Manager do logowania się na instancje. Zalety:
- Nie wymaga otwierania portu 22 na stałe
- Wszystkie sesje są logowane w CloudTrail
- Działa przez IAM role, nie wymaga kluczy SSH
- Bezpieczniejsze (nie ma ryzyka zgubienia klucza prywatnego)

---

## 9. Wyzwania napotkane podczas wdrożenia

### Problem 1: CORS Errors

**Objaw:** Frontend nie mógł wykonywać requestów do API, przeglądarki blokowały przez CORS policy.

**Przyczyna:** Django wymaga explicit konfiguracji CORS_ALLOWED_ORIGINS. Początkowo miałem tylko DNS ALB, ale Cloudflare proxy zmienia origin na domenę kongoapp.pl.

**Rozwiązanie:** Skonfigurowałem CORS_ALLOWED_ORIGINS w user-data script aby zawierało:
- `http://[ALB-DNS]`
- `http://kongoapp.pl`
- `http://www.kongoapp.pl`
- `https://kongoapp.pl`
- `https://www.kongoapp.pl`

To pokrywa wszystkie możliwe scenariusze (direct access, Cloudflare proxy, z/bez www).

### Problem 2: Django zwracał 301 redirects zamiast 200 OK

**Objaw:** Wszystkie requesty do `/api/categories/` zwracały 301 Moved Permanently zamiast danych JSON.

**Przyczyna:** Django ma ustawienie `SECURE_SSL_REDIRECT` oraz mechanizm, który redirect'uje HTTP → HTTPS. Django myślało, że request jest przez HTTP (bo komunikacja ALB→Nginx→Django jest HTTP) i próbowało redirect'ować na HTTPS.

**Rozwiązanie:** Skonfigurowałem Nginx aby wysyłał header `X-Forwarded-Proto: https` do Django (zamiast `X-Forwarded-Proto: $scheme` co by wysłało "http"). Django sprawdza ten header i rozpoznaje że oryginalny request był przez HTTPS, więc nie robi redirecta.

### Problem 3: Cloudflare Error 521 - Web server is down

**Objaw:** Przy próbie dostępu przez kongoapp.pl, Cloudflare zwracało Error 521.

**Przyczyna:** 
1. Początkowo miałem CNAME record wskazujący na ALB DNS, ale CNAME nie rozwiązywał się globalnie
2. Cloudflare SSL/TLS mode był początkowo na "Flexible" co powodowało błędy

**Rozwiązanie:**
1. Zmieniłem CNAME na A records wskazujące bezpośrednio na IP Cloudflare proxy
2. Zmieniłem SSL/TLS mode na "Full"
3. Zaktualizowałem CORS_ALLOWED_ORIGINS aby zawierało HTTPS origins

### Problem 4: Frontend służył stare pliki JavaScript

**Objaw:** Po wdrożeniu nowej wersji frontendu, instancje EC2 nadal serwowały stare pliki JS. `index.html` wskazywał na `main.abc123.js` zamiast nowego `main.xyz789.js`.

**Przyczyna:** Komenda `aws s3 sync` domyślnie tylko dodaje nowe pliki i aktualizuje zmienione, ale nie usuwa starych. S3 zawierało zarówno stare jak i nowe pliki JS, a user-data script pobierało wszystkie.

**Rozwiązanie:** Dodałem flagę `--delete` do `aws s3 sync`:
```bash
aws s3 sync s3://forum-frontend-builds-kongoapp/latest/ /var/www/frontend/ --delete
```
To zapewnia, że stare pliki są usuwane z local directory na instancji.

### Problem 5: Mixed Content Error

**Objaw:** Gdy Cloudflare proxy było włączone, frontend (HTTPS) próbował robić requesty do `http://alb-dns.amazonaws.com/api/`, co było blokowane przez przeglądarki.

**Przyczyna:** Frontend miał hardcoded `REACT_APP_API_URL=http://alb-dns...`.

**Rozwiązanie:** Zmieniłem na relative URL: `REACT_APP_API_URL=/api`. Frontend automatycznie używa tego samego protokołu co strona (HTTPS przez Cloudflare, HTTP przez direct ALB).

### Problem 6: Security Group i Subnet z różnych VPC

**Objaw:** Instance Refresh failował z błędem "Security group and subnet belong to different networks".

**Przyczyna:** W Launch Template wybrałem konkretny subnet. ASG ma swoje subnety skonfigurowane. Gdy te nie matchowały, AWS rzucał błąd.

**Rozwiązanie:** W Launch Template zostawiłem subnet field pusty (Don't include in launch template). ASG automatycznie wybiera odpowiednie subnety z swojej konfiguracji.

---

## 10. Decyzje architektoniczne i ich uzasadnienie

### Dlaczego Auto Scaling zamiast pojedynczej instancji?

- **High Availability:** Jeśli jedna instancja padnie, druga nadal obsługuje ruch
- **Zero-downtime deployments:** Mogę aktualizować instancje bez przerwy w dostępności
- **Skalowalność:** Jeśli ruch wzrośnie, ASG automatycznie uruchomi dodatkowe instancje
- **Self-healing:** Unhealthy instancje są automatycznie zastępowane

### Dlaczego ALB zamiast pojedynczego Elastic IP?

- **Load balancing:** Ruch jest równomiernie rozdzielany między instancje
- **Health checks:** ALB automatycznie wykrywa i omija niesprawne instancje
- **Scaling:** Może obsługiwać ruch do wielu instancji jednocześnie
- **Managed service:** AWS zarządza dostępnością i redundancją ALB

### Dlaczego private subnets dla EC2?

- **Bezpieczeństwo:** Instancje nie są bezpośrednio dostępne z internetu
- **Defense in depth:** Dodatkowa warstwa ochrony
- **NAT Gateway:** Instancje nadal mogą inicjować połączenia wychodzące (updates, ECR, S3)
- **Best practice:** Tylko load balancery powinny być w public subnets

### Dlaczego Docker dla Django?

- **Consistency:** Ten sam obraz działa lokalnie i w produkcji
- **Isolation:** Django jest izolowane od systemu operacyjnego
- **Versioning:** Każdy build ma unikalny tag, mogę łatwo rollback
- **Portability:** Mogę łatwo przenieść aplikację do innego providera (ECS, Kubernetes)

### Dlaczego Nginx zamiast serwowania Django bezpośrednio?

- **Performance:** Nginx jest szybszy w serwowaniu statycznych plików
- **Security:** Nginx dodaje warstwę ochrony przed niektórymi atakami
- **Flexibility:** Nginx może routować do wielu backend services
- **Best practice:** W produkcji zawsze używa się reverse proxy przed application server

### Dlaczego RDS zamiast PostgreSQL na EC2?

- **Managed service:** AWS zarządza backupami, updates, patches
- **High availability:** Multi-AZ replikacja out-of-the-box
- **Backups:** Automatyczne daily backups z 7-day retention
- **Mniej pracy:** Nie muszę ręcznie konfigurować i monitorować PostgreSQL

---

## 11. Metryki i wydajność

### Czas ładowania strony
- First Contentful Paint: ~1.2s
- Time to Interactive: ~2.5s
- Dzięki Cloudflare CDN statyczne zasoby są serwowane z lokalnych edge servers

### API Response Time
- Średni response time: ~100-200ms
- Health check endpoint: ~50ms
- Database query time: ~20-50ms

### Dostępność (Availability)
- Teoretyczna dostępność z Multi-AZ: 99.99% (około 4 minuty downtime miesięcznie)
- ALB sama ma SLA 99.99%
- RDS Multi-AZ ma SLA 99.95%

### Koszty miesięczne
W ramach Free Tier (pierwsze 12 miesięcy):
- EC2 t3.micro: Free (750h/miesiąc)
- RDS db.t3.micro: Free (750h/miesiąc)
- ALB: ~$16/miesiąc (nie jest w Free Tier)
- NAT Gateway: ~$32/miesiąc (nie jest w Free Tier)
- S3: ~$0.50/miesiąc
- Cloudflare: Free plan

**Total:** ~$50/miesiąc w pierwszym roku

Po Free Tier (~$70-100/miesiąc):
- EC2: ~$15/miesiąc (2x t3.micro)
- RDS: ~$15/miesiąc
- Pozostałe koszty bez zmian

---

## 12. Możliwe ulepszenia i dalszy rozwój

### Obecnie brakuje:

**CI/CD Pipeline:**
- Automatyczne buildowanie i deployment przy push do GitHub
- Automatyczne testy przed deployment
- Można użyć GitHub Actions + AWS CodeDeploy

**HTTPS na ALB:**
- Dodać certyfikat SSL do ALB
- Zmienić Cloudflare na "Full (strict)"
- Bezpieczniejsza komunikacja Cloudflare↔ALB

**Monitoring i Alerting:**
- CloudWatch Alarms dla CPU, memory, error rates
- SNS notifications na email/SMS przy problemach
- Dashboard z kluczowymi metrykami

**Database backups:**
- Obecnie daily backups przez RDS
- Można dodać cross-region backups dla disaster recovery

**Caching:**
- Redis/ElastiCache dla session storage i database query caching
- Zwiększyłoby wydajność API

**Container orchestration:**
- Migracja z EC2 + Docker do ECS Fargate
- Lepsza izolacja i zarządzanie kontenerami
- Auto-scaling na poziomie kontenerów

**Separate static file serving:**
- CloudFront distribution dla statycznych plików
- S3 jako origin zamiast serwowania przez EC2
- Jeszcze szybsze ładowanie i niższe koszty

---

## 13. Podsumowanie

Zbudowałem production-ready forum internetowe z wykorzystaniem nowoczesnej architektury cloud-native w AWS. Kluczowe elementy to:

✅ **High Availability** - Multi-AZ deployment, redundantne instancje, auto-healing
✅ **Scalability** - Auto Scaling Group może skalować od 1 do 4 instancji w zależności od obciążenia
✅ **Security** - VPC z private subnets, Security Groups, IAM roles, secrets w Parameter Store
✅ **Zero-downtime deployments** - Instance Refresh z prioritize availability strategy
✅ **Automation** - User-data script automatyzuje cały setup nowych instancji
✅ **Performance** - Cloudflare CDN, Nginx reverse proxy, RDS managed database
✅ **Monitoring** - CloudWatch metrics, health checks, comprehensive logging

Aplikacja jest dostępna pod adresem **https://kongoapp.pl** i obsługuje użytkowników z całego świata dzięki Cloudflare CDN i AWS global infrastructure.

Najtrudniejszymi wyzwaniami były konfiguracja CORS dla różnych origins (direct ALB vs Cloudflare), rozwiązanie problemu Django redirectów 301 przez konfigurację Nginx headers, oraz debugowanie problemu ze starymi plikami JS przez dodanie `--delete` flag do S3 sync.

Architektura jest skalowalna i gotowa do obsługi produkcyjnego ruchu. Przy minimalnych modyfikacjach (dodanie Redis, CloudFront, CI/CD) może obsługiwać dziesiątki tysięcy użytkowników jednocześnie.

---

**Koniec prezentacji**

Czas prezentacji: ~10-15 minut (w zależności od tempa i pytań)


