import json
from typing import List, Dict

class JSONLoader:
    @staticmethod
    def load(file_path: str) -> List[Dict]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON должен содержать массив объектов")
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка в JSON: {e}")

    @staticmethod
    def validate(data: List[Dict], expected_fields: List[str], data_type: str) -> bool:
        for i, item in enumerate(data):
            for field in expected_fields:
                if field not in item:
                    print(f"Ошибка в {data_type}: в записи {i} отсутствует поле '{field}'")
                    return False
        return True