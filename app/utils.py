import json

class Utils:
    @staticmethod
    def load_data(data_file):
        """Load data from the JSON file."""
        with open(data_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def save_data(data, data_file):
        """Save data to the JSON file."""
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
