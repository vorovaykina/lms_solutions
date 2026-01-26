import argparse
from database import Database
from loaders import JSONLoader
from serializers import JsonSerializer, XmlSerializer
from queries import QUERIES

DB_CONFIG = {
    "host": "localhost",
    "database": "task_python",
    "user": "postgres",
    "password": "123456" 
}

def main():
    parser = argparse.ArgumentParser(description="University ETL Tool")
    parser.add_argument("--students", required=True, help="Path to students.json")
    parser.add_argument("--rooms", required=True, help="Path to rooms.json")
    parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format")
    args = parser.parse_args()

    rooms_data = JSONLoader.load(args.rooms)
    students_data = JSONLoader.load(args.students)
    
    if not JSONLoader.validate(rooms_data, ["id", "name"], "Rooms"): return
    if not JSONLoader.validate(students_data, ["id", "name", "birthday", "sex", "room"], "Students"): return

    db = Database(DB_CONFIG)
    try:
        db.connect()
        db.insert_rooms(rooms_data)
        db.insert_students(students_data)

        serializer = JsonSerializer() if args.format == "json" else XmlSerializer()
        
        for task_name, sql in QUERIES.items():
            result = db.select(sql)
            serializer.serialize(result, task_name)
            print(f"Запрос {task_name} выполнен успешно.")

    finally:
        db.close()

if __name__ == "__main__":
    main()