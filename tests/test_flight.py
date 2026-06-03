import unittest
from unittest.mock import MagicMock
from app.flight import Flight, BookingSystem


class TestFlight(unittest.TestCase):
    def setUp(self):
        self.flight = Flight("OS101", 3)

    def test_initial_available_seats(self):
        self.assertEqual(self.flight.get_available_seats(), 3)

    def test_book_seat_returns_seat_number(self):
        seat = self.flight.book_seat("Anna")
        self.assertEqual(seat, 1)

    def test_book_seat_reduces_available_seats(self):
        self.flight.book_seat("Anna")
        self.assertEqual(self.flight.get_available_seats(), 2)

    def test_book_seats_sequential_numbers(self):
        seat1 = self.flight.book_seat("Anna")
        seat2 = self.flight.book_seat("Bob")
        self.assertEqual(seat1, 1)
        self.assertEqual(seat2, 2)

    def test_book_seat_stores_reservation(self):
        self.flight.book_seat("Anna")
        self.assertEqual(self.flight.reservations[1], "Anna")

    def test_overbooking_raises(self):
        self.flight.book_seat("Anna")
        self.flight.book_seat("Bob")
        self.flight.book_seat("Carl")
        with self.assertRaises(ValueError):
            self.flight.book_seat("Dave")


class TestBookingSystem(unittest.TestCase):
    def setUp(self):
        self.mock_gateway = MagicMock()
        self.system = BookingSystem(self.mock_gateway)
        self.flight = Flight("OS101", 5)
        self.system.add_flight(self.flight)

    def test_successful_booking(self):
        self.mock_gateway.process_payment.return_value = True
        seat = self.system.book_ticket("OS101", "Anna", "4111111111111111", 250.0)
        self.assertEqual(seat, 1)

    def test_successful_booking_records_transaction(self):
        self.mock_gateway.process_payment.return_value = True
        self.system.book_ticket("OS101", "Anna", "4111111111111111", 250.0)
        self.assertEqual(len(self.system.transactions), 1)

    def test_payment_failure_raises(self):
        self.mock_gateway.process_payment.return_value = False
        with self.assertRaises(ValueError):
            self.system.book_ticket("OS101", "Anna", "4111111111111111", 250.0)

    def test_payment_failure_no_seat_booked(self):
        self.mock_gateway.process_payment.return_value = False
        try:
            self.system.book_ticket("OS101", "Anna", "4111111111111111", 250.0)
        except ValueError:
            pass
        self.assertEqual(self.flight.get_available_seats(), 5)

    def test_unknown_flight_raises(self):
        self.mock_gateway.process_payment.return_value = True
        with self.assertRaises(ValueError):
            self.system.book_ticket("XX999", "Anna", "4111111111111111", 250.0)

    def test_payment_called_with_correct_args(self):
        self.mock_gateway.process_payment.return_value = True
        self.system.book_ticket("OS101", "Anna", "4111111111111111", 250.0)
        self.mock_gateway.process_payment.assert_called_once_with(250.0, "4111111111111111")


if __name__ == "__main__":
    unittest.main()
