
from faker import Faker
import random
import models
from database import SessionLocal, engine


# Database  setup
Session = SessionLocal
session = Session()
engine = engine


# Faker instance
fake = Faker()

# Insert Admins (100 records)
admins = [
    models.Admin(
        username=fake.user_name(),
        email=fake.unique.email(),
        password=fake.password(length=random.randint(4, 8)),
    )
    for _ in range(100)
]
session.bulk_save_objects(admins)
session.commit()
print("Inserted Admins")

# Insert Route_ticket (10,000 records)
route_tickets = [
    models.Route_ticket(
        source_id=random.randint(1, 28),
        destination_id=random.randint(1, 28),
        company_id=random.randint(1, 42),
        unit_price=random.randint(300, 3000),
        number_seats=random.randint(10, 60),
    )
    for _ in range(10000)
]
session.bulk_save_objects(route_tickets)
session.commit()
print("Inserted Route Tickets")

# Insert Clients (500,000 records)
clients = [
    models.Client(
        username=fake.user_name(),
        Gender=random.choice(["male", "female"]),
        age=random.randint(3, 68),
        balance=random.randint(500, 700000),
        email=fake.unique.email(),
        password=fake.password(length=random.randint(4, 8)),
    )
    for _ in range(500000)
]
session.bulk_save_objects(clients)
session.commit()
print("Inserted Clients")

# Insert BookedTickets (500,000 records)
booked_tickets = [
    models.BookedTicket(
        route_id=random.randint(1, 10000),  # Assuming 10,000 Route Tickets exist
        client_id=random.randint(1, 500000),  # Assuming 500,000 Clients exist
        created_at=fake.date_time_this_year(),
        expires_at=fake.date_time_this_year(),
        number_seats=random.randint(1, 10),
        total_price=random.randint(500, 10000),
        active=fake.boolean(),
        feed_back_description=fake.text(max_nb_chars=100),
    )
    for _ in range(500000)
]
session.bulk_save_objects(booked_tickets)
session.commit()
print("Inserted Booked Tickets")
