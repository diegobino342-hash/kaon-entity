import sqlite3

def save_result(data):
    conn = sqlite3.connect("app/storage/kaon.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS history (asset, action, result)")
    c.execute("INSERT INTO history VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()
