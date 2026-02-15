"""
Hotel Reservation System Module.

This module implements a hotel reservation system with three main classes:
Hotel, Customer, and Reservation. It provides persistent storage using JSON
files and includes error handling for invalid data.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Customer:
    """Represents a customer in the hotel reservation system."""

    DATA_FILE = "customers.json"

    def __init__(self, customer_id: str, name: str, email: str,
                 phone: str):
        """
        Initialize a Customer instance.

        Args:
            customer_id: Unique identifier for the customer
            name: Customer's full name
            email: Customer's email address
            phone: Customer's phone number
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self) -> Dict:
        """Convert customer to dictionary format."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Customer':
        """Create a Customer instance from dictionary data."""
        return cls(
            customer_id=data["customer_id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"]
        )

    @classmethod
    def create_customer(cls, customer_id: str, name: str, email: str,
                        phone: str) -> 'Customer':
        """
        Create a new customer and save to file.

        Args:
            customer_id: Unique identifier for the customer
            name: Customer's full name
            email: Customer's email address
            phone: Customer's phone number

        Returns:
            Customer: The created customer instance
        """
        customer = cls(customer_id, name, email, phone)
        customers = cls._load_all_customers()
        customers[customer_id] = customer.to_dict()
        cls._save_all_customers(customers)
        return customer

    @classmethod
    def delete_customer(cls, customer_id: str) -> bool:
        """
        Delete a customer from the system.

        Args:
            customer_id: ID of the customer to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        customers = cls._load_all_customers()
        if customer_id in customers:
            del customers[customer_id]
            cls._save_all_customers(customers)
            return True
        return False

    @classmethod
    def display_customer_information(cls, customer_id: str) -> Optional[str]:
        """
        Display customer information.

        Args:
            customer_id: ID of the customer to display

        Returns:
            str: Formatted customer information or None if not found
        """
        customers = cls._load_all_customers()
        if customer_id in customers:
            customer_data = customers[customer_id]
            return (
                f"Customer ID: {customer_data['customer_id']}\n"
                f"Name: {customer_data['name']}\n"
                f"Email: {customer_data['email']}\n"
                f"Phone: {customer_data['phone']}"
            )
        return None

    @classmethod
    def modify_customer_information(cls, customer_id: str,
                                     name: Optional[str] = None,
                                     email: Optional[str] = None,
                                     phone: Optional[str] = None) -> bool:
        """
        Modify customer information.

        Args:
            customer_id: ID of the customer to modify
            name: New name (optional)
            email: New email (optional)
            phone: New phone (optional)

        Returns:
            bool: True if modified successfully, False otherwise
        """
        customers = cls._load_all_customers()
        if customer_id in customers:
            if name is not None:
                customers[customer_id]["name"] = name
            if email is not None:
                customers[customer_id]["email"] = email
            if phone is not None:
                customers[customer_id]["phone"] = phone
            cls._save_all_customers(customers)
            return True
        return False

    @classmethod
    def _load_all_customers(cls) -> Dict:
        """Load all customers from file."""
        if not os.path.exists(cls.DATA_FILE):
            return {}
        try:
            with open(cls.DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading customers file: {e}")
            return {}

    @classmethod
    def _save_all_customers(cls, customers: Dict) -> None:
        """Save all customers to file."""
        try:
            with open(cls.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(customers, f, indent=2)
        except IOError as e:
            print(f"Error saving customers file: {e}")

