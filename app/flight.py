import random


class Flight:
    def __init__(self, flight_number, total_seats):
        self.flight_number = flight_number
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.reservations = {}

    def book_seat(self, passenger_name):
        if self.available_seats == 0:
            raise ValueError("Keine Sitzplätze mehr verfügbar")
        seat_number = self.total_seats - self.available_seats + 1
        self.reservations[seat_number] = passenger_name
        self.available_seats -= 1
        return seat_number

    def get_available_seats(self):
        return self.available_seats


class PaymentGateway:
    def process_payment(self, amount, card_number):
        if not card_number.startswith("4"):
            raise ValueError("Ungültige Kreditkarte")
        return random.choice([True, False])


class BookingSystem:
    def __init__(self, payment_gateway):
        self.flights = {}
        self.payment_gateway = payment_gateway
        self.transactions = []

    def add_flight(self, flight):
        self.flights[flight.flight_number] = flight

    def book_ticket(self, flight_number, passenger_name, card_number, amount):
        if flight_number not in self.flights:
            raise ValueError("Flug nicht gefunden")

        flight = self.flights[flight_number]

        if not self.payment_gateway.process_payment(amount, card_number):
            raise ValueError("Zahlung fehlgeschlagen")

        seat_number = flight.book_seat(passenger_name)
        self.transactions.append(
            f"Flug {flight_number}: {passenger_name} Sitz {seat_number}, bezahlt: {amount} EUR"
        )
        return seat_number
