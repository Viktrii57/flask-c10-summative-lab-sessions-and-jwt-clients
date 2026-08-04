import random
from faker import Faker
from app import create_app
from models import db, User, JournalEntry

fake = Faker()
app = create_app()

with app.app_context():
    print("Clearing existing database tables...")
    JournalEntry.query.delete()
    User.query.delete()

    print("Creating primary test users...")
    demo_user = User(username="demouser", email="demo@example.com")
    demo_user.password = "password123"
    
    other_user = User(username="otheruser", email="other@example.com")
    other_user.password = "password123"

    db.session.add_all([demo_user, other_user])
    db.session.commit()

    print("Seeding journal entries for demo user...")
    categories = ['Work', 'Personal', 'Fitness', 'Ideas']
    for _ in range(25):
        entry = JournalEntry(
            title=fake.sentence(nb_words=4),
            content=fake.paragraph(nb_sentences=4),
            category=random.choice(categories),
            mood_score=random.randint(1, 10),
            user_id=demo_user.id
        )
        db.session.add(entry)

    print("Seeding journal entries for secondary user...")
    for _ in range(5):
        entry = JournalEntry(
            title=fake.sentence(nb_words=4),
            content=fake.paragraph(nb_sentences=3),
            category=random.choice(categories),
            mood_score=random.randint(1, 10),
            user_id=other_user.id
        )
        db.session.add(entry)

    db.session.commit()
    print("Database seeding completed successfully!")