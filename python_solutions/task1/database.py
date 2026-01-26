import psycopg2
from psycopg2.extras import execute_values

class Database:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn = psycopg2.connect(**self.config)
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def insert_rooms(self, rooms):
        with self.conn.cursor() as cur:
            query = "INSERT INTO rooms (id, name) VALUES %s ON CONFLICT (id) DO NOTHING"
            data = [(r['id'], r['name']) for r in rooms]
            execute_values(cur, query, data)
        self.conn.commit()

    def insert_students(self, students):
        with self.conn.cursor() as cur:
            query = "INSERT INTO students (id, name, birthday, sex, room_id) VALUES %s ON CONFLICT (id) DO NOTHING"
            data = [(s['id'], s['name'], s['birthday'], s['sex'], s['room']) for s in students]
            execute_values(cur, query, data)
        self.conn.commit()

    def select(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]