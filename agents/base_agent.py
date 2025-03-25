import os

class BaseAgent:
    def __init__(self, model_name: str):
        self.schema = None
        self.model_name = model_name
        self._load_schema()

    def _load_schema(self):
        try:
            schema_file_path = os.path.join(os.path.dirname(__file__), 'schema.json')
            with open(schema_file_path, 'r') as schema_file:
                self.schema = schema_file.read()
        except Exception as e:
            print(f"Error loading schema: {e}")
    
    def generate_content(self, context: str, prompt: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")

