# 🛠️ Troubleshooting Guide: PostgreSQL with Docker (Port 5432)

This guide helps you resolve common PostgreSQL + Docker issues when running your ETL project.

---

## 1. ❌ Problem: `Connection refused` or container not running

**Typical error message:**

```bash
connection to server at "127.0.0.1", port 5432 failed: Connection refused
```

✅ **Steps to fix:**

- Go to the `/docker` folder:

```bash
cd docker
```

- Start Docker services:

```bash
docker-compose up -d
```

- Verify if the container is running:

```bash
docker ps
```

You should see something like:

```
PORTS                    NAMES
0.0.0.0:5432->5432/tcp   hotel_postgres
```

---

## 2. ❌ Problem: `FATAL: database "hotel_dw" does not exist`

✅ **Steps to fix:**

- Connect to the running container:

```bash
docker exec -it hotel_postgres psql -U postgres
```

- Or recreate Docker volumes to force automatic creation:

```bash
docker-compose down -v
cd docker
docker-compose up -d
```

✅ **Always check if the database exists:**

```bash
docker exec -it hotel_postgres psql -U postgres -l
```

---

## 3. ❌ Problem: Port 5432 occupied by local PostgreSQL

✅ **Check if something is already using port 5432:**

```bash
lsof -i :5432
```

If you see a `postgres` process (e.g., `postgres 12449 brunoribeiro ...`), you need to free the port.

### If managed by Homebrew (MacOS):

- Stop the PostgreSQL service:

```bash
brew services stop postgresql@17
```

- Confirm the port is now free:

```bash
lsof -i :5432
```

### If NOT managed by Homebrew (manual process):

- Kill the process manually:

```bash
kill 12449
```

Or force kill if needed:

```bash
kill -9 12449
```

✅ After stopping the local PostgreSQL, re-run:

```bash
cd docker
docker-compose up -d
```

✅ Confirm only Docker is using port 5432:

```bash
lsof -i :5432
```

Expected result:

```
com.docker.backend ... *:postgresql (LISTEN)
```

---

## 4. ✅ Correct Execution Paths

| Task                     | Where to execute           |
| ------------------------ | -------------------------- |
| Start Docker containers  | Inside `/docker` folder    |
| Run ETL connection tests | At the project root folder |

### Examples:

```bash
# Start containers
cd docker
docker-compose up -d

# Run ETL connection test
cd ..
python -m etl.tests.test_connection
```

---

## 5. ✅ Quick Reference

```bash
# Check Docker container
$ docker ps

# Verify DB exists
$ docker exec -it hotel_postgres psql -U postgres -l

# Force recreate Docker volumes
$ cd docker && docker-compose down -v && docker-compose up -d

# Test ETL DB connection
$ python -m etl.tests.test_connection

# Check if port 5432 is occupied
$ lsof -i :5432

# Stop local PostgreSQL service (if managed by Homebrew)
$ brew services stop postgresql@17

# Kill PostgreSQL manually if not managed
$ kill -9 <pid>
```

✅ Now you're fully set up to debug PostgreSQL + Docker like a pro!
