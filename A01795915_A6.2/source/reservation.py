"""
Hotel Reservation System Module.

This module implements a hotel reservation system with three main classes:
Hotel, Customer, and Reservation. It provides persistent storage using JSON
files and includes error handling for invalid data.
"""

import json
import os
from typing import Dict, Optional
from hotel import Hotel
from customer import Customer


class Reservation:
    """Represents a reservation action in the hotel system."""

    DATA_FILE = os.path.join(os.path.dirname(__file__),
                             "../tests/reservations.json")

    def __init__(self, reservation_id: str, customer_id: str,
                 hotel_id: str, check_in: str, check_out: str):
        """
        Initialize a Reservation instance.

        Args:
            reservation_id: Unique identifier for the reservation
            customer_id: ID of the customer making the reservation
            hotel_id: ID of the hotel being reserved
            check_in: Check-in date (YYYY-MM-DD format)
            check_out: Check-out date (YYYY-MM-DD format)
        """
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.check_in = check_in
        self.check_out = check_out
        self.status = "active"

    def to_dict(self) -> Dict:
        """Convert reservation to dictionary format."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Reservation':
        """Create a Reservation instance from dictionary data."""
        reservation = cls(
            reservation_id=data["reservation_id"],
            customer_id=data["customer_id"],
            hotel_id=data["hotel_id"],
            check_in=data["check_in"],
            check_out=data["check_out"]
        )
        reservation.status = data.get("status", "active")
        return reservation

    @classmethod
    
    def create_reservation(cls, reservation_id: str, customer_id: str,
                           hotel_id: str, check_in: str,
                           check_out: str) -> Optional['Reservation']:
        """
        Create a new reservation.

        Args:
            reservation_id: Unique identifier for the reservation
            customer_id: ID of the customer
            hotel_id: ID of the hotel
            check_in: Check-in date (YYYY-MM-DD format)
            check_out: Check-out date (YYYY-MM-DD format)

        Returns:
            Reservation: The created reservation or None if failed
        """
        # Verify customer exists
        if not Customer.customer_exists(customer_id):
            print(f"Error: Customer {customer_id} does not exist")
            return None

        # Verify hotel exists and has available rooms
        if not Hotel.reserve_room(hotel_id):
            print(f"Error: No rooms available at hotel {hotel_id}")
            return None

        reservation = cls(reservation_id, customer_id, hotel_id,
                          check_in, check_out)
        reservations = cls.load_all_reservations()
        reservations[reservation_id] = reservation.to_dict()
        cls.save_all_reservations(reservations)
        return reservation

    @classmethod
    def cancel_reservation(cls, reservation_id: str) -> bool:
        """
        Cancel a reservation.

        Args:
            reservation_id: ID of the reservation to cancel

        Returns:
            bool: True if cancelled successfully, False otherwise
        """
        reservations = cls.load_all_reservations()
        if reservation_id in reservations:
            reservation_data = reservations[reservation_id]
            if reservation_data["status"] == "active":
                # Free up the hotel room
                Hotel.cancel_reservation(reservation_data["hotel_id"])
                reservation_data["status"] = "cancelled"
                reservations[reservation_id] = reservation_data
                cls.save_all_reservations(reservations)
                return True
        return False

    @classmethod
    def load_all_reservations(cls) -> Dict:
        """Load all reservations from file."""
        if not os.path.exists(cls.DATA_FILE):
            return {}
        try:
            with open(cls.DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            print(f"Error loading reservations file: {error}")
            return {}

    @classmethod
    def save_all_reservations(cls, reservations: Dict) -> None:
        """Save all reservations to file."""
        try:
            with open(cls.DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump(reservations, file, indent=2)
        except IOError as error:
            print(f"Error saving reservations file: {error}")
