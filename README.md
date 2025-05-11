# Secret Sender

Secret Sender è un’applicazione web che permette di condividere messaggi e file sensibili in modalità **one-time view**: ogni secret viene cifrato, memorizzato temporaneamente in Redis e può essere visualizzato una sola volta. Ideale per condividere credenziali temporanee, documenti riservati o qualunque contenuto “usa e getta”.

---

## Caratteristiche Principali

- **One-Time View**  
  Il secret si autodistrugge dopo la prima lettura.
- **End-to-End Encryption**  
  Cifratura AES-GCM dei payload (confidenzialità + autenticità).
- **Password-Protected**  
  KDF Scrypt (N=2¹⁴, r=8, p=1) per derivare la chiave dalla password utente.
- **TTL Configurabile**  
  1h, 24h, 1d, 30d o senza scadenza via Redis `SETEX`.
- **Allegati**  
  File multipart con limite dimensione configurabile via `MAX_UPLOAD_MB`.
- **Frontend Leggero**  
  HTMX per aggiornamenti AJAX senza scrivere JS complesso.

---

## Architettura

- **FastAPI** + **Uvicorn**  
  Server ASGI Python ad alte prestazioni.
- **Redis**  
  Data store in-memory, protetto da password/ACL, TTL nativo.
- **Cryptography**  
  - AES-GCM per cifratura.  
  - Scrypt KDF per password.
- **Jinja2 + Bootstrap**  
  UI responsiva e pulita.

---

## Struttura del Repository

```
secret_sender/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── app/
    ├── main.py
    ├── config.py
    ├── db.py
    ├── crypto.py
    ├── routers/
    │   ├── secrets.py
    │   ├── view.py
    │   └── about.py
    ├── schemas.py
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── fragment.html
    │   ├── view.html
    │   └── about.html
    └── static/
        ├── bootstrap.min.css
        ├── htmx.min.js
        └── logo.png
```

---

## Installazione & Avvio

1. **Clona il repository**  
   ```bash
   git clone https://github.com/nicontinisio/secret-sender.git
   cd secret-sender
   ```
2. **Configura l’ambiente**  
   Se desideri, crea un `.env` nella root:
   ```dotenv
   REDIS_HOST=redis
   REDIS_PORT=6379
   REDIS_PASSWORD=secretpass
   MAX_UPLOAD_MB=125
   SECRET_LOGO=/static/logo.png
   ```
3. **Avvia con Docker Compose**  
   ```bash
   docker-compose down --remove-orphans
   docker-compose up --build -d
   ```
4. **Visita l’app**  
   Apri `https://secret.your.domain/` (o `http://localhost:8000` in sviluppo).

---

## Traefik come Reverse Proxy (esempio)

In produzione è consigliato un reverse proxy per SSL, load-balancing e header di sicurezza. Di seguito un esempio di configurazione Traefik via Docker Compose:

```yaml

services:
  traefik:
    image: traefik:v2.10
    command:
      - "--entryPoints.web.address=:80"
      - "--entryPoints.websecure.address=:443"
      - "--providers.docker=true"
      - "--certificatesResolvers.le.acme.tlsChallenge=true"
      - "--certificatesResolvers.le.acme.email=tuo@email.it"
      - "--certificatesResolvers.le.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt

  secret-web:
    build: .
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.secret.rule=Host(`secret.your.domain`)"
      - "traefik.http.routers.secret.entrypoints=websecure"
      - "traefik.http.routers.secret.tls.certresolver=le"
    environment:
      REDIS_HOST: redis
      REDIS_PASSWORD: secretpass
      MAX_UPLOAD_MB: 125
      SECRET_LOGO: /static/logo.png
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    command: ["redis-server", "--requirepass", "secretpass"]
    environment:
      - REDIS_PASSWORD=secretpass
```

---

## Contribuire

1. Fork & clone  sono i benvenuti
2. Crea una branch del progetto
3. Committa le modifiche  
4. Apri una Pull Request  

---

## Licenza

Distribuito sotto licenza GPL
