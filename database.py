import sqlite3

def init_db():
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            user_id INTEGER,
            description TEXT,
            amount REAL,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def update_balance(user_id, amount):
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        new_balance = result[0] + amount
        cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (new_balance, user_id))
    else:
        cursor.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, amount))
    conn.commit()
    conn.close()

def add_payment(user_id, description, amount):
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO payments (user_id, description, amount, status) VALUES (?, ?, ?, ?)',
                   (user_id, description, amount, 'pending'))
    conn.commit()
    conn.close()

def update_payment_status(description, status):
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE payments SET status = ? WHERE description = ?', (status, description))
    conn.commit()
    conn.close()

def get_payment(description):
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments WHERE description = ?', (description,))
    result = cursor.fetchone()
    conn.close()
    return result
