"""
Unit tests for the Hotel Reservation System.

This module contains comprehensive unit tests for the Customer, Hotel,
and Reservation classes to ensure proper functionality.
"""

import unittest
import os
import json
import sys
from unittest.mock import patch
from reservation import Customer, Hotel, Reservation

# Add source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                 '..', 'source'))


class TestCustomer(unittest.TestCase):
    """Test cases for the Customer class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_file = "test_customers.json"
        Customer.DATA_FILE = self.test_file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_customer_initialization(self):
        """Test customer object initialization."""
        customer = Customer("C001", "Juan Perez", "juan@gmail.com",
                            "123-456-7890")
        self.assertEqual(customer.customer_id, "C001")
        self.assertEqual(customer.name, "Juan Perez")
        self.assertEqual(customer.email, "juan@gmail.com")
        self.assertEqual(customer.phone, "123-456-7890")

    def test_customer_to_dict(self):
        """Test converting customer to dictionary."""
        customer = Customer("C001", "Juan Perez", "juan@gmail.com",
                            "123-456-7890")
        customer_dict = customer.to_dict()
        self.assertEqual(customer_dict["customer_id"], "C001")
        self.assertEqual(customer_dict["name"], "Juan Perez")
        self.assertEqual(customer_dict["email"], "juan@gmail.com")
        self.assertEqual(customer_dict["phone"], "123-456-7890")

    def test_customer_from_dict(self):
        """Test creating customer from dictionary."""
        data = {
            "customer_id": "C001",
            "name": "Juan Perez",
            "email": "juan@gmail.com",
            "phone": "123-456-7890"
        }
        customer = Customer.from_dict(data)
        self.assertEqual(customer.customer_id, "C001")
        self.assertEqual(customer.name, "Juan Perez")

    def test_create_customer(self):
        """Test creating and saving a customer."""
        customer = Customer.create_customer("C001", "Juan Perez",
                                            "juan@gmail.com",
                                            "123-456-7890")
        self.assertIsNotNone(customer)
        self.assertTrue(os.path.exists(self.test_file))

        # Verify data was saved correctly
        with open(self.test_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertIn("C001", data)
            self.assertEqual(data["C001"]["name"], "Juan Perez")

    def test_delete_customer(self):
        """Test deleting a customer."""
        Customer.create_customer("C001", "Juan Perez", "juan@gmail.com",
                                 "123-456-7890")
        result = Customer.delete_customer("C001")
        self.assertTrue(result)

        # Verify customer was deleted
        with open(self.test_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertNotIn("C001", data)

    def test_delete_nonexistent_customer(self):
        """Test deleting a customer that doesn't exist."""
        result = Customer.delete_customer("C999")
        self.assertFalse(result)

    def test_display_customer_information(self):
        """Test displaying customer information."""
        Customer.create_customer("C001", "Juan Perez", "juan@gmail.com",
                                 "123-456-7890")
        info = Customer.display_customer_information("C001")
        self.assertIsNotNone(info)
        self.assertIn("Juan Perez", info)
        self.assertIn("juan@gmail.com", info)

    def test_display_nonexistent_customer(self):
        """Test displaying information for nonexistent customer."""
        info = Customer.display_customer_information("C999")
        self.assertIsNone(info)

    def test_modify_customer_information(self):
        """Test modifying customer information."""
        Customer.create_customer("C001", "Juan Perez", "juan@gmail.com",
                                 "123-456-7890")
        result = Customer.modify_customer_information(
            "C001",
            name="Juana Perez",
            email="juana@gmail.com"
        )
        self.assertTrue(result)

        # Verify modifications
        with open(self.test_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(data["C001"]["name"], "Juana Perez")
            self.assertEqual(data["C001"]["email"], "juana@gmail.com")

    def test_modify_nonexistent_customer(self):
        """Test modifying a customer that doesn't exist."""
        result = Customer.modify_customer_information("C999", name="Test")
        self.assertFalse(result)

    def test_load_customers_file_not_exists(self):
        """Test loading customers when file doesn't exist."""
        customers = Customer._load_all_customers()
        self.assertEqual(customers, {})

    def test_load_customers_invalid_json(self):
        """Test loading customers with invalid JSON."""
        with open(self.test_file, 'w', encoding='utf-8') as file:
            file.write("invalid json content")

        with patch('builtins.print') as mock_print:
            customers = Customer._load_all_customers()
            self.assertEqual(customers, {})
            mock_print.assert_called()

    @staticmethod
    def test_save_customers_io_error():
        """Test handling IO error when saving customers."""
        with patch('builtins.open', side_effect=IOError("Test error")):
            with patch('builtins.print') as mock_print:
                Customer._save_all_customers({"C001": {}})
                mock_print.assert_called()



if __name__ == '__main__':
    unittest.main()
