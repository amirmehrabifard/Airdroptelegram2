import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        referrer_id INTEGER,
        referrals INTEGER DEFAULT 0,
        rewarded INTEGER DEFAULT 0,
        wallet TEXT
    )''')
    conn.commit()
    conn.close()

def add_user(user_id, username, referrer_id=None):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)",
              (user_id, username, referrer_id))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "user_id": row[0],
            "username": row[1],
            "referrer_id": row[2],
            "referrals": row[3],
            "rewarded": row[4],
            "wallet": row[5]
        }
    return None

def update_referrals(user_id, rewarded=False):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    if rewarded:
        c.execute("UPDATE users SET rewarded = 1 WHERE user_id = ?", (user_id,))
    else:
        c.execute("UPDATE users SET referrals = referrals + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_referral_count(user_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT referrals FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def save_wallet(user_id, wallet):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("UPDATE users SET wallet = ? WHERE user_id = ?", (wallet, user_id))
    conn.commit()
    conn.close()

def get_wallet(user_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
