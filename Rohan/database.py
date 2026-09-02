import oracledb

DB_USERNAME = "Whatsapp"
DB_PASSWORD = "app123"
DB_DSN = "localhost:1521/XEPDB1"


def get_connection():
    try:
        connection = oracledb.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )

        print("Oracle database connected successfully!")
        return connection

    except oracledb.Error as e:
        print("Database connection error:", e)
        return None