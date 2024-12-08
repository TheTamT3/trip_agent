import pytest

from src.services.flight.models import Flight
from src.services.flight.sv import book_flight


def test_get_flight():
    departure_city = 'Ho Chi Minh City'
    arrival_city = 'Hanoi'
    flight_date = '2024-12-12'
    flight = Flight.get_flight(departure_city, arrival_city, flight_date)
    print("Result: {}".format(flight))


def test_booking():
    departure_city = 'Hanoi'
    arrival_city = 'Ho Chi Minh City'
    flight_date = '2024-12-20'
    return_date = '2024-12-20'
    seat_class = "economy"
    seat_count = "10"
    user_id = '123456'
    user_phone_number = '123456789'

    result = book_flight(departure_city, arrival_city, flight_date, return_date, seat_class, seat_count, user_id,
                         user_phone_number)
    print(result)
