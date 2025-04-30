# 🧠 PostgreSQL (psql) Cheatsheet for Docker ETL Projects

This cheatsheet provides a quick reference for using `psql` inside your PostgreSQL Docker container.

---

## 🐳 Entering the PostgreSQL Container

```bash
docker exec -it hotel_postgres psql -U postgres -d hotel_dw
```

- `hotel_postgres`: name of the Docker container
- `postgres`: database user
- `hotel_dw`: database name

---

## 📋 Table and Schema Inspection

| Command         | Description                                |
| --------------- | ------------------------------------------ |
| `\dt`           | List all tables in the current schema      |
| `\d table_name` | Describe table structure (columns + types) |
| `\conninfo`     | Show current connection info               |

---

## 🔍 Querying Data

| Command                         | Description                   |
| ------------------------------- | ----------------------------- |
| `SELECT * FROM table LIMIT 10;` | View first 10 rows of a table |
| `SELECT COUNT(*) FROM table;`   | Count total rows in a table   |

---

## ⚙️ Miscellaneous

| Command           | Description                             |
| ----------------- | --------------------------------------- |
| `\pset pager off` | Disable pager (avoids "(END)" view)     |
| `\q`              | Exit psql and return to terminal prompt |

---

✅ Use this reference to quickly inspect, query, and validate your PostgreSQL data during ETL development. Keep it versioned under `/docs` for consistency across your team.
