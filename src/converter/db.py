import os
from datetime import datetime

import psycopg2
from loguru import logger

DB_URL = os.environ["DATABASE_URL"]

class DB:
    def __init__(self) -> None:
        self.conn = self.get_conn()

    def __del__(self) -> None:
        self.conn.close()

    def get_conn(self):
        conn = psycopg2.connect(DB_URL)
        return conn
    
    def create_db(self):
        q = ""
        dump_path = os.path.join("src", "converter", "sql", "pg_dump.sql")

        with open(dump_path, "r") as f: 
            q = f.read()
        
        try: 
            with self.conn.cursor() as cursor:
                cursor.execute(q)
                self.conn.commit()
        except Exception as exc:
            logger.error(exc)

    def show_currencies(self):
        self.cursor.execute("SELECT * FROM currencies_rub")
        res = self.cursor.fetchall()
        print(res) 
         
    def update_all_currencies(self, rates: dict, updated_at: datetime): 
        try: 
            with self.conn.cursor() as cursor:
                for cur_name, rate in rates.items():
                    query = """
                        INSERT INTO currencies_rub (name, to_rub, updated_at) 
                        VALUES (%s, %s, %s)
                        ON CONFLICT (name) DO UPDATE SET
                        (to_rub, updated_at) = (EXCLUDED.to_rub, EXCLUDED.updated_at);
                    """
                    cursor.execute(query, (cur_name, rate, updated_at)) 
                    self.conn.commit()
        except psycopg2.DatabaseError as exc:
            if self.conn:
                self.conn.rollback()
            logger.error(exc)

    def get_last_updated_at(self): 
        query = "SELECT updated_at FROM currencies_rub LIMIT 1;"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                res = cursor.fetchone()[0]
                return res 
        except psycopg2.DatabaseError as exc:
            logger.error(exc)

    def get_rates(self, curs: list) -> dict:
        curs_names = ",".join([f"'{cur}'" for cur in curs])
        query = f"""
            SELECT name, to_rub FROM currencies_rub WHERE name in ({','.join(['%s' for _ in range(len(curs))])});
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, curs)
                res = cursor.fetchall()
                rates = {**dict(res), **{"RUB": 1.0}}
                return rates 
        except psycopg2.DatabaseError as exc:
            logger.error(exc)

    def get_currencies_list(self) -> list:
        query = f"SELECT name FROM currencies_rub;"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                res = cursor.fetchall()
                return [cur for cur, in res] + ["RUB"]
        except psycopg2.DatabaseError as exc:
            logger.error(exc)