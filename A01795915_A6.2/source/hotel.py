"""
Hotel Reservation System Module.
Hotel Class
This module implements a hotel class for the hotel reservation system.
It provides persistent storage using JSON files and includes error handling for invalid data.
"""

import json
import os
from typing import Dict, Optional


class Hotel:
    """Represents a hotel in the reservation system."""

    DATA_FILE = os.path.join(os.path.dirname(__file__), "../tests/hotels.json")

    def __init__(self, hotel_id: str, name: str, location: str,
                 total_rooms: int):
        """
        Initialize a Hotel instance.

        Args:
            hotel_id: Unique identifier for the hotel
            name: Hotel's name
            location: Hotel's location/address
            total_rooms: Total number of rooms in the hotel
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms

    def to_dict(self) -> Dict:
        """Convert hotel to dictionary format."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Hotel':
        """Create a Hotel instance from dictionary data."""
        hotel = cls(
            hotel_id=data["hotel_id"],
            name=data["name"],
            location=data["location"],
            total_rooms=data["total_rooms"]
        )
        hotel.available_rooms = data.get("available_rooms",
                                         data["total_rooms"])
        return hotel

    @classmethod
    def create_hotel(cls, hotel_id: str, name: str, location: str,
                     total_rooms: int) -> 'Hotel':
        """
        Create a new hotel and save to file.

        Args:
            hotel_id: Unique identifier for the hotel
            name: Hotel's name
            location: Hotel's location/address
            total_rooms: Total number of rooms in the hotel

        Returns:
            Hotel: The created hotel instance
        """
        hotel = cls(hotel_id, name, location, total_rooms)
        hotels = cls._load_all_hotels()
        hotels[hotel_id] = hotel.to_dict()
        cls._save_all_hotels(hotels)
        return hotel

    @classmethod
    def delete_hotel(cls, hotel_id: str) -> bool:
        """
        Delete a hotel from the system.

        Args:
            hotel_id: ID of the hotel to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        hotels = cls._load_all_hotels()
        if hotel_id in hotels:
            del hotels[hotel_id]
            cls._save_all_hotels(hotels)
            return True
        return False

    @classmethod
    def display_hotel_information(cls, hotel_id: str) -> Optional[str]:
        """
        Display hotel information.

        Args:
            hotel_id: ID of the hotel to display

        Returns:
            str: Formatted hotel information or None if not found
        """
        hotels = cls._load_all_hotels()
        if hotel_id in hotels:
            hotel_data = hotels[hotel_id]
            return (
                f"Hotel ID: {hotel_data['hotel_id']}\n"
                f"Name: {hotel_data['name']}\n"
                f"Location: {hotel_data['location']}\n"
                f"Total Rooms: {hotel_data['total_rooms']}\n"
                f"Available Rooms: {hotel_data['available_rooms']}"
            )
        return None

    @classmethod
    def modify_hotel_information(cls, hotel_id: str,
                                  name: Optional[str] = None,
                                  location: Optional[str] = None,
                                  total_rooms: Optional[int] = None) -> bool:
        """
        Modify hotel information.

        Args:
            hotel_id: ID of the hotel to modify
            name: New name (optional)
            location: New location (optional)
            total_rooms: New total rooms count (optional)

        Returns:
            bool: True if modified successfully, False otherwise
        """
        hotels = cls._load_all_hotels()
        if hotel_id in hotels:
            if name is not None:
                hotels[hotel_id]["name"] = name
            if location is not None:
                hotels[hotel_id]["location"] = location
            if total_rooms is not None:
                old_total = hotels[hotel_id]["total_rooms"]
                available = hotels[hotel_id]["available_rooms"]
                difference = total_rooms - old_total
                hotels[hotel_id]["total_rooms"] = total_rooms
                hotels[hotel_id]["available_rooms"] = available + difference
            cls._save_all_hotels(hotels)
            return True
        return False

    @classmethod
    def reserve_room(cls, hotel_id: str) -> bool:
        """
        Reserve a room in the hotel.

        Args:
            hotel_id: ID of the hotel

        Returns:
            bool: True if room reserved successfully, False otherwise
        """
        hotels = cls._load_all_hotels()
        if hotel_id in hotels:
            if hotels[hotel_id]["available_rooms"] > 0:
                hotels[hotel_id]["available_rooms"] -= 1
                cls._save_all_hotels(hotels)
                return True
        return False

    @classmethod
    def cancel_reservation(cls, hotel_id: str) -> bool:
        """
        Cancel a reservation and free up a room.

        Args:
            hotel_id: ID of the hotel

        Returns:
            bool: True if reservation cancelled successfully, False otherwise
        """
        hotels = cls._load_all_hotels()
        if hotel_id in hotels:
            total = hotels[hotel_id]["total_rooms"]
            available = hotels[hotel_id]["available_rooms"]
            if available < total:
                hotels[hotel_id]["available_rooms"] += 1
                cls._save_all_hotels(hotels)
                return True
        return False

    @classmethod
    def _load_all_hotels(cls) -> Dict:
        """Load all hotels from file."""
        if not os.path.exists(cls.DATA_FILE):
            return {}
        try:
            with open(cls.DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading hotels file: {e}")
            return {}

    @classmethod
    def _save_all_hotels(cls, hotels: Dict) -> None:
        """Save all hotels to file."""
        try:
            with open(cls.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(hotels, f, indent=2)
        except IOError as e:
            print(f"Error saving hotels file: {e}")

