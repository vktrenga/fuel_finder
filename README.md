## Project Structure

```bash
fuel_finder/
├── fuel_finder_app/          # Core app code
│   ├── management/           # Custom Django management commands
│   └── scripts/              # Helper scripts (e.g., initial_data.py)
├── fuel_finder_alert/        # Alert / notification module
│   └── cron/                 # Scheduled tasks / cron jobs
├── fuel_finder_auth_user/    # Authentication / user management module
├── .env_sample               # Sample environment variables
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script / entrypoint
├── README.md                 # Project documentation
└── (other helper files/modules) # Utilities, config files, etc.
```

##  Django Admin

### **Admin URL**

```
http://localhost:8000/admin/
```

### **Default Superuser (from initial_data or setup)**

| Username | Email                                         | Password |
| -------- | --------------------------------------------- | -------- |
| admin    | [admin@example.com](mailto:admin@example.com) | admin123 |


---

##  Sample User Accounts

| Username | Email                                         | Password    | Role         |
| -------- | --------------------------------------------- | ----------- | ------------ |
| user1    | [user1@example.com](mailto:user1@example.com) | password123 | Regular user |
| user2    | [user2@example.com](mailto:user2@example.com) | password123 | Regular user |

> These users are for testing purposes upto 20 user

---

## 📄 API Documentation (Swagger / OpenAPI)

| Type             | URL            | Description                        |
| ---------------- | -------------- | ---------------------------------- |
| **OpenAPI JSON** | `/api/schema/` | Full OpenAPI 3 schema              |
| **Swagger UI**   | `/api/docs/`   | Interactive API explorer           |
| **ReDoc UI**     | `/api/redoc/`  | Clean documentation for developers |

**Example:**

```
Swagger: http://localhost:8000/api/docs/
ReDoc:   http://localhost:8000/api/redoc/
OpenAPI: http://localhost:8000/api/schema/
```

---

## 🐳 Docker Notes

* Start services:

```bash
docker-compose up -d
```

* Run management commands:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py truncate_db
docker-compose exec web python manage.py runscript initial_data
```

* Collect static files for Swagger / ReDoc:

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

---



## Features

### 1. **User Authentication**

* Handles **user registration**, login, and token-based authentication (JWT).
* User profile management including optional fields like address, gender, and location (`lat`/`lng`).

### 2. **Fuel Station Management**

* Models and APIs for managing **fuel stations**, including:

  * Station details (name, address, coordinates)
  * Station services (Petrol, Diesel)
  * Station prices linked to fuel services
  * Station amenities and operating timings
* CRUD operations for stations with DRF serializers and viewsets.

### 3. **Alerts & Notifications**

* Automatic alerts for **open/close status** of fuel stations.
* Can track changes in **fuel prices** or station status.
* Background jobs using **cron or Django `BackgroundScheduler`** to check for updates at intervals.

### 4. **Initial Setup Scripts**

* Scripts to **populate initial data** such as:

  * Cities
  * Fuel types
  * Amenities
  * Default users
* Scripts handle database creation and initial data insertion without cascade issues.

### 5. **Pagination**

* DRF-powered **pagination** for APIs returning lists of stations, prices, or alerts.
* Supports **page size** and **page number** parameters to control API responses efficiently.

### 6. **Django REST Framework (DRF) Integration**

* All main models exposed via DRF viewsets and serializers.
* Supports **filtering, searching, and ordering** of fuel stations and related entities.
* Proper HTTP response codes and error handling.

### 7. **Models**

* Key models in the project include:

  * `Cities` – stores city name and coordinates.
  * `FuelTypes` – defines types of fuel available (Petrol, Diesel, etc.).
  * `Amenities` – station facilities (e.g., restrooms, cafes).
  * `FuelStation` – main station info, linked to services, amenities, and prices.
  * `StationServices` – fuel types provided by stations.
  * `StationPrices` – price per fuel type.
  * `StationAmenities` – amenities offered by a station.
  * `StationTiming` – opening and closing times.

### 8. **Environment Configuration**

* `.env_sample` for environment variables such as:

  * Database connection
  



## Installed Packages & Purpose
| Package                      | Purpose                           | When You Use It                |
| ---------------------------- | --------------------------------- | ------------------------------ |
| **rest_framework**           | Build APIs in Django              | All API development            |
| **rest_framework_simplejwt** | JWT authentication                | Secure login, token-based auth |
| **django_extensions**        | Developer utilities               | Run scripts
| **drf_spectacular**          | API documentation auto-generation | Creating Swagger/OpenAPI docs  |
| **drf_spectacular_sidecar**  | Local API documentation assets    | Offline Swagger/Redoc support  |


## API Documentation

The project includes automatic API documentation generated using DRF-Spectacular (OpenAPI 3).

## Available API Docs
| Type                      | URL            | Description                                          |
| ------------------------- | -------------- | ---------------------------------------------------- |
| **OpenAPI Schema (JSON)** | `/api/schema/` | The full OpenAPI 3 schema used by Swagger & ReDoc    |
| **Swagger UI**            | `/api/docs/`   | Interactive API explorer with authentication support |
| **ReDoc UI**              | `/api/redoc/`  | Clean, responsive API documentation for developers   |



# Project Setup Guide – Fuel Finder

## 1. Create & Activate Virtual Environment (venv)

### **Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### **macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Requirements

```bash
pip install -r requirements.txt
```

---

## 2. Environment Variables

Create a `.env` file in the project root:

```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432

POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_USER=
DEBUG=True
```

---

##  3. Database Setup (Local)

```bash
python manage.py makemigrations
python manage.py migrate
```

##  4. Initial data setup

```bash
python manage.py runscript initial_data

```

##  5. Truncate all data

```bash
 python manage.py truncate_db
```

## 6. Run the Project Locally

```bash
python manage.py runserver
```

Static files (only when deploying):

```bash
python manage.py collectstatic
```

---

#  Docker Setup

##  1. Build Docker Images

```bash
docker-compose build --no-cache
```

##  2. Start Containers

```bash
docker-compose up
```

Run in background:

```bash
docker-compose up -d
```

##  3. Stop Containers

```bash
docker-compose down
```

Remove volumes ( deletes DB data!):

```bash
docker-compose down -v
```

truncate all existing data from db

```bash
docker compose up -d
docker compose exec web python manage.py truncate_db
```
