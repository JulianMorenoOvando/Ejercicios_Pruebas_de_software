"""
Data Manager Module.

Provides generic data loading and saving capabilities for JSON files.
"""

import json
import os
from typing import Dict


class DataManager:
    """Class to manage loading and saving JSON data."""

    @staticmethod
    def load_data(file_path: str, entity_name: str = "file") -> Dict:
        """
        Load data from a JSON file.

        Args:
            file_path: Path to the JSON file.
            entity_name: Name of the entity being loaded (for error messages).

        Returns:
            Dict: Dictionary containing the loaded data.
        """
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            print(f"Error loading {entity_name}: {error}")
            return {}

    @staticmethod
    def save_data(file_path: str, data: Dict,
                  entity_name: str = "file") -> None:
        """
        Save data to a JSON file.

        Args:
            file_path: Path to the JSON file.
            data: Dictionary containing the data to save.
            entity_name: Name of the entity being saved (for error messages).
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
        except IOError as error:
            print(f"Error saving {entity_name}: {error}")
