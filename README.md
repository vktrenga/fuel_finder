## Project Structure
fuel_finder/
├── fuel_finder_app/         # core app code
├── fuel_finder_alert/       # alert / notification module
├── fuel_finder_auth_user/   # auth / user management
├── .env_sample              # sample environment variables
├── requirements.txt
├── manage.py                # main script / entrypoint
├── README.md                # this file
└── (other helper files/modules)

## 🚀 Features

### 1. **User Authentication**

* Handles **user registration**, login, and token-based authentication (JWT).
* Supports custom claims like `user_id` and `email` in tokens.
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
  * API keys (if any)
  * Scheduler intervals

### 9. **Extensible Architecture**

* Designed for easy extension:

  * Add new **fuel types** or **amenities**
  * Add new **alert types**
  * Extend APIs with extra fields




# 📘 Project Setup Guide – Fuel Finder

## 🔧 1. Create & Activate Virtual Environment (venv)

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

## ⚙️ 2. Environment Variables

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
docker-compose build
```

##  2. Start Containers

```bash
docker-compose up
```

Run in background:

```bash
docker-compose up -d
```

##  5. Stop Containers

```bash
docker-compose down
```

Remove volumes (⚠︎ deletes DB data!):

```bash
docker-compose down -v
```


