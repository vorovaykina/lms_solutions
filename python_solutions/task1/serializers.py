import json
import dicttoxml
from abc import ABC, abstractmethod

class BaseSerializer(ABC):
    @abstractmethod
    def serialize(self, data, filename):
        pass

class JsonSerializer(BaseSerializer):
    def serialize(self, data, filename):
        with open(f"{filename}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)

class XmlSerializer(BaseSerializer):
    def serialize(self, data, filename):
        xml_bytes = dicttoxml.dicttoxml(data, custom_root='results', attr_type=False)
        with open(f"{filename}.xml", "wb") as f:
            f.write(xml_bytes)