### Step 1: Clone the Repository
```
https://github.com/midhun98/ewireApp.git
cd ewireApp
```

### Step 2: Create the .env File in Project Root
```
SECRET_KEY=your_secret_key
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### Step 3. Building a Docker Image
```
docker build -t ewire-app-image .
```

### Step 4. Build and Run the Containers.
```
docker-compose -f docker-compose-local.yml up --build
```
### Step 5. Apply the migrations.
```
docker-compose exec app python manage.py migrate
```
### Step 5. Create Superuser..
```
docker-compose exec app python manage.py createsuperuser
```


