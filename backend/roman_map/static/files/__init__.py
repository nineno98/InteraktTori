import json
import os

# Elérési út a schema.json fájlhoz
schema_file_path = os.path.join(
    os.path.dirname(__file__), 'schema.json'
)

def load_schema():
    with open(schema_file_path, 'r') as f:
        schema_data = json.load(f)
    return schema_data

# Ha azt szeretnéd, hogy a schema elérhető legyen közvetlenül is
schema = load_schema()