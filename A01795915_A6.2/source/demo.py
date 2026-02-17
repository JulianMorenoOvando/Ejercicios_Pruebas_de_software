"""
Demo script for the Hotel Reservation System.

This script demonstrates the basic functionality of the system.
"""

import sys
import os

# Source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'A01795915_A6.2/results'))

from reservation import Customer, Hotel, Reservation


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")


def demo():
    """Run a demonstration of the reservation system."""
    print_section("Hotel Reservation System Demo")

    # Clean up any existing test data
    for file in ["customers.json", "hotels.json", "reservations.json"]:
        if os.path.exists(file):
            os.remove(file)

    # Create customers
    print_section("Creating Customers")
    customer1 = Customer.create_customer(
        "C001",
        "Juan Perez",
        "juan.perez@gmail.com",
        "555-0101"
    )
    print(f" Created customer: {customer1.name}")

    customer2 = Customer.create_customer(
        "C002",
        "Maria Lopez",
        "maria.lopez@gmail.com",
        "555-0102"
    )
    print(f" Created customer: {customer2.name}")

    # Display customer information
    print_section("Customer Information")
    print(Customer.display_customer_information("C001"))

    # Create hotels
    print_section("Creating Hotels")
    hotel1 = Hotel.create_hotel(
        "H001",
        "Grand Plaza Hotel",
        "New York, NY",
        150
    )
    print(f" Created hotel: {hotel1.name} ({hotel1.total_rooms} rooms)")

    hotel2 = Hotel.create_hotel(
        "H002",
        "Seaside Resort",
        "Miami, FL",
        200
    )
    print(f" Created hotel: {hotel2.name} ({hotel2.total_rooms} rooms)")

    # Display hotel information
    print_section("Hotel Information")
    print(Hotel.display_hotel_information("H001"))

    # Create reservations
    print_section("Creating Reservations")
    reservation1 = Reservation.create_reservation(
        "R001",
        "C001",
        "H001",
        "2026-03-15",
        "2026-03-20"
    )
    if reservation1:
        print(f" Created reservation {reservation1.reservation_id}")
        print(f"  Customer: {reservation1.customer_id}")
        print(f"  Hotel: {reservation1.hotel_id}")
        print(f"  Check-in: {reservation1.check_in}")
        print(f"  Check-out: {reservation1.check_out}")

    reservation2 = Reservation.create_reservation(
        "R002",
        "C002",
        "H002",
        "2026-04-01",
        "2026-04-07"
    )
    if reservation2:
        print(f" Created reservation {reservation2.reservation_id}")

    # Check hotel availability after reservations
    print_section("Hotel Availability After Reservations")
    print(Hotel.display_hotel_information("H001"))

    # Modify customer information
    print_section("Modifying Customer Information")
    Customer.modify_customer_information(
        "C001",
        email="juan.perez.new@email.com",
        phone="555-9999"
    )
    print(" Updated customer C001")
    print(Customer.display_customer_information("C001"))

    # Modify hotel information
    print_section("Modifying Hotel Information")
    Hotel.modify_hotel_information(
        "H001",
        name="Grand Plaza Hotel & Spa"
    )
    print(" Updated hotel H001")
    print(Hotel.display_hotel_information("H001"))

    # Cancel a reservation
    print_section("Cancelling Reservation")
    if Reservation.cancel_reservation("R001"):
        print(" Cancelled reservation R001")
        print("\nHotel availability after cancellation:")
        print(Hotel.display_hotel_information("H001"))

    # Test error handling
    print_section("Testing Error Handling")

    print("\n1. Attempting to create reservation with non-existent customer:")
    result = Reservation.create_reservation(
        "R999",
        "C999",  # Non-existent customer
        "H001",
        "2026-05-01",
        "2026-05-05"
    )
    if result is None:
        print(" Error handled correctly")

    print("\n2. Attempting to create reservation with no available rooms:")
    # Create a hotel with 0 rooms
    Hotel.create_hotel("H003", "Tiny Hotel", "Boston, MA", 0)
    result = Reservation.create_reservation(
        "R998",
        "C001",
        "H003",
        "2026-05-01",
        "2026-05-05"
    )
    if result is None:
        print(" Error handled correctly")

    print("\n3. Attempting to delete non-existent customer:")
    result = Customer.delete_customer("C999")
    if not result:
        print(" Error handled correctly (returned False)")

    # Clean up
    print_section("Cleanup")
    Customer.delete_customer("C001")
    # Customer.delete_customer("C002")
    print(" Deleted customers")

    Hotel.delete_hotel("H001")
    # Hotel.delete_hotel("H002")
    # Hotel.delete_hotel("H003")
    print(" Deleted hotels")

    print_section("Demo Complete!")
    print("All functionality demonstrated successfully.")
    print("Data files created: customers.json, hotels.json, "
          "reservations.json")


if __name__ == "__main__":
    demo()
