tools = [
    {
        "type": "function",
        "function": {
            "name": "book_flight",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_city": {"type": "string"},
                    "arrival_city": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "arrival_date": {"type": "string"},
                    "seat_class": {"type": "string", "enum": ["economy", "business"]},
                    "seat_economy_count": {"type": "integer"},
                    "seat_business_count": {"type": "integer"},
                    "user_id": {"type": "string", "description": "customer's identification number"},
                    "user_phone_number": {"type": "string", "description": "customer's phone number"},
                },
                "required": ["departure_city", "arrival_city", "departure_date", "seat_class", "seat_count", "user_id", "user_phone_number"],
                "additionalProperties": False,
            },
        },
    }
]
