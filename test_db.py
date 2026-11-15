import sqlite3
import os

DB_NAME = "test.db"

# Удаляем старую БД, если она есть
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    print(f"Старая БД '{DB_NAME}' удалена.")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# --- Таблица 1: users ---
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    city TEXT,
    email TEXT
)
""")

users_data = [
    ('Иван Иванов', 25, 'Москва', 'ivan@mail.ru'),
    ('Мария Петрова', 30, 'Санкт-Петербург', 'maria@mail.ru'),
    ('Алексей Сидоров', 28, 'Казань', 'alex@mail.ru'),
    ('Елена Смирнова', 35, 'Новосибирск', 'elena@mail.ru'),
    ('Дмитрий Кузнецов', 22, 'Екатеринбург', 'dmitry@mail.ru'),
]
cursor.executemany(
    "INSERT INTO users (name, age, city, email) VALUES (?, ?, ?, ?)",
    users_data
)

# --- Таблица 2: products ---
cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL,
    category TEXT,
    stock INTEGER
)
""")

products_data = [
    ('Ноутбук', 55000.0, 'Электроника', 10),
    ('Мышь', 800.5, 'Периферия', 50),
    ('Клавиатура', 2500.0, 'Периферия', 30),
    ('Монитор', 18000.0, 'Электроника', 15),
    ('Наушники', 3500.0, 'Аудио', 25),
    ('Веб-камера', 4200.0, 'Периферия', 20),
]
cursor.executemany(
    "INSERT INTO products (title, price, category, stock) VALUES (?, ?, ?, ?)",
    products_data
)

# --- Таблица 3: orders ---
cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

orders_data = [
    (1, 1, 2, '2026-10-15'),
    (2, 3, 1, '2026-10-18'),
    (3, 2, 3, '2026-10-20'),
    (1, 5, 1, '2026-10-22'),
    (4, 1, 1, '2026-10-25'),
    (5, 4, 2, '2026-11-01'),
    (2, 6, 1, '2026-11-03'),
]
cursor.executemany(
    "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)",
    orders_data
)

conn.commit()
conn.close()

print(f"База данных '{DB_NAME}' успешно создана!")
print(f"   - Таблица 'users': 5 записей")
print(f"   - Таблица 'products': 6 записей")
print(f"   - Таблица 'orders': 7 записей")
print(f"\nТеперь запустите main.py и выберите файл '{DB_NAME}' через меню Set connection.")