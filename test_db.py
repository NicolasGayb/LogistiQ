import sqlite3, os

db_path = r"C:\Projetos\LogistiQ\instance\test_logistiq.db"
print("📄 Tentando abrir:", db_path)

try:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    print("✅ Conseguiu abrir e criar o banco SQLite normalmente.")
    conn.close()
except Exception as e:
    print("❌ Erro ao abrir:", e)
