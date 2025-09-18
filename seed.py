from faker import Faker
from app import app
from models import db, Course

fake = Faker()

with app.app_context():
    # Clear existing data
    Course.query.delete()

    # Create sample courses
    for _ in range(10):
        course = Course(
            name=fake.sentence(nb_words=3),
            description=fake.text(max_nb_chars=200),
            credits=fake.random_int(min=1, max=5)
        )
        db.session.add(course)

    # Save to database
    db.session.commit()

    print("✅ 10 fake courses added successfully!")
