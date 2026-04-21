# 🛒 Ecommerce Project — React + Django + PostgreSQL

A full-stack ecommerce application built with a **React** frontend, **Django REST Framework** backend, and **PostgreSQL** database — fully containerized with Docker.

> **Forked from** [mohitdjcet/ecommerce-project-react-django](https://github.com/mohitdjcet/ecommerce-project-react-django)

---

## 🧱 Tech Stack

| Layer      | Technology                                      |
|------------|-------------------------------------------------|
| Frontend   | React 19, React Router v7, Tailwind CSS v4, Vite|
| Backend    | Django 6, Django REST Framework, SimpleJWT      |
| Database   | PostgreSQL 16                                   |
| API Docs   | drf-spectacular (Swagger UI + ReDoc)            |
| Container  | Docker, Docker Compose                          |

---

## 📁 Project Structure

```
ecommerce-project-react-django/
├── docker-compose.yml
├── scripts/
│   └── seed_postgres.sql      # Raw SQL seed script
├── backend/
│   ├── Dockerfile
│   ├── entrypoint.sh          # Waits for DB, runs migrations, starts server
│   ├── requirements.txt       # Local dev dependencies
│   ├── requirements-docker.txt# Docker-specific dependencies (includes psycopg2)
│   ├── .env                   # Environment variables (not committed)
│   ├── backend/               # Django project settings & URL config
│   └── store/                 # Main app
│       └── management/        # Custom management commands (seed_data)
└── frontend/
    ├── Dockerfile
    ├── src/                   # React source (pages, components, API client)
    └── vite.config.js
```

---

## 🚀 Running with Docker (Recommended)

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### 1. Clone the repo

```bash
git clone https://github.com/Gkodkod/ecommerce-project-react-django.git
cd ecommerce-project-react-django
```

### 2. Configure environment variables

Create `backend/.env` (copy and fill in values):

```env
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### 3. Build and start all services

```bash
docker-compose up --build
```

This will:
- Start **PostgreSQL** on host port `5433` (internal: `5432`)
- Wait for the database to be healthy
- Automatically run **Django migrations**
- Start the **Django backend** at `http://localhost:8000`
- Start the **React frontend** at `http://localhost:5173`

### 4. Subsequent starts (no rebuild needed)

```bash
docker-compose up
```

### 5. Stop all services

```bash
docker-compose down
```

To also remove the database volume:

```bash
docker-compose down -v
```

---

## 🌱 Seeding the Database

Populate the database with realistic demo data (Categories, Products, Users, Carts, and Orders). This process is handled differently depending on your environment:

| Environment | Seeding Type | How it Works |
| :--- | :--- | :--- |
| **Docker** | **Automatic** | Runs via `entrypoint.sh` on startup if `SEED_DATA=True`. |
| **Local Dev** | **Manual** | Run `python manage.py seed_data` after migrations. |

### 1. Using Django Management Command (Recommended)
This uses your Django models and handles relationships (like password hashing) correctly.

```bash
# In Docker (Automatic by default, but can be run manually)
docker exec django_backend python manage.py seed_data

# In Docker (Wipe and re-seed)
docker exec django_backend python manage.py seed_data --flush

# In Local Dev (Non-Docker)
python manage.py seed_data
```

### 2. Automatic Seeding (Docker Only)
Automatic seeding is enabled by default in `docker-compose.yml`. To toggle this, modify the environment variable:

```yaml
backend:
  environment:
    - SEED_DATA=True  # Change to False to disable
```

### 3. Using SQL Script (Alternative)
A raw SQL script is provided for direct PostgreSQL interaction. This is useful for manual database initialization.

```powershell
# PowerShell
Get-Content scripts\seed_postgres.sql | docker exec -i ecommerce_db psql -U postgres -d ecommerce_db
```

### 🔑 Demo Credentials
- **Admin**: `admin` / `Admin1234!`
- **Users**: `alice_shop`, `bob_buys`, `carol_carts` (Password: `SecurePass123!`)

---

## 🔧 Useful Docker Commands

| Task                              | Command                                                            |
|-----------------------------------|--------------------------------------------------------------------|
| View live logs                    | `docker-compose logs -f`                                          |
| Open Django shell                 | `docker exec -it django_backend python manage.py shell`           |
| Run migrations manually           | `docker exec -it django_backend python manage.py migrate`         |
| Create a superuser                | `docker exec -it django_backend python manage.py createsuperuser` |
| Connect to PostgreSQL             | `docker exec -it ecommerce_db psql -U postgres -d ecommerce_db`  |
| Rebuild a single service          | `docker-compose up --build backend`                               |

---

## 🌐 API Endpoints

Base URL: `http://localhost:8000/api/`

### Auth
| Method | Endpoint                    | Description            | Auth Required |
|--------|-----------------------------|------------------------|---------------|
| POST   | `/api/register/`            | Register new user      | No            |
| POST   | `/api/token/`               | Obtain JWT token pair  | No            |
| POST   | `/api/token/refresh/`       | Refresh access token   | No            |

### Products
| Method | Endpoint                    | Description            | Auth Required |
|--------|-----------------------------|------------------------|---------------|
| GET    | `/api/products/`            | List all products      | No            |
| GET    | `/api/products/<id>/`       | Get product detail     | No            |
| GET    | `/api/categories/`          | List all categories    | No            |

### Cart
| Method | Endpoint                    | Description            | Auth Required |
|--------|-----------------------------|------------------------|---------------|
| GET    | `/api/cart/`                | Get current user cart  | ✅ Yes        |
| POST   | `/api/cart/add/`            | Add item to cart       | ✅ Yes        |
| POST   | `/api/cart/update/`         | Update item quantity   | ✅ Yes        |
| POST   | `/api/cart/remove/`         | Remove item from cart  | ✅ Yes        |

### Orders
| Method | Endpoint                    | Description            | Auth Required |
|--------|-----------------------------|------------------------|---------------|
| POST   | `/api/orders/create/`       | Place a new order      | ✅ Yes        |

### API Documentation
| URL                          | Description             |
|------------------------------|-------------------------|
| `http://localhost:8000/api/docs/`   | Swagger UI             |
| `http://localhost:8000/api/redoc/`  | ReDoc                  |
| `http://localhost:8000/api/schema/` | Raw OpenAPI schema     |

---

## 💻 Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🗄️ Data Models

```
Category ──< Product
User ── Cart ──< CartItem >── Product
User ──< Order ──< OrderItem >── Product
User ── UserProfile
```

---

## 🔐 Authentication

JWT-based authentication via `djangorestframework-simplejwt`.

- **Access token** lifetime: 60 minutes
- **Refresh token** lifetime: 1 day
- Include the access token in requests as:  
  `Authorization: Bearer <access_token>`
