import os
import django
import random
from datetime import time
from faker import Faker

# -----------------------------------
# Django setup
# -----------------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event, Participant

fake = Faker()

def run():
    # -----------------------------------
    # Clear old data (optional but useful)
    # -----------------------------------
    Participant.objects.all().delete()
    Event.objects.all().delete()
    Category.objects.all().delete()

    # -----------------------------------
    # Create Categories
    # -----------------------------------
    categories = []
    category_names = [
        ("Technology", "Tech related events"),
        ("Business", "Business and startup events"),
        ("Education", "Academic and learning events"),
        ("Entertainment", "Fun and entertainment events"),
    ]

    for name, desc in category_names:
        category = Category.objects.create(
            name=name,
            description=desc
        )
        categories.append(category)

    # -----------------------------------
    # Create Events
    # -----------------------------------
    events = []
    for _ in range(10):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(nb_sentences=4),
            date=fake.date_between(start_date="-10d", end_date="+30d"),
            time=time(
                hour=random.randint(9, 20),
                minute=random.choice([0, 15, 30, 45])
            ),
            location=fake.city(),
            category=random.choice(categories)
        )
        events.append(event)

    # -----------------------------------
    # Create Participants
    # -----------------------------------
    for _ in range(30):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )

        # Assign participant to 1–3 random events
        participant.event.add(*random.sample(events, random.randint(1, 3)))

    print("✅ Database populated successfully using Faker!")


if __name__ == "__main__":
    run()
