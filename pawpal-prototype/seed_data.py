"""
Seed database with sample data for PawPal
"""
from datetime import datetime, date, time, timedelta
from database import (
    db, User, Dog, AvailabilitySlot, Booking, Post, Notification,
    DogSize, SlotStatus, BookingStatus, PostType
)


def seed_database():
    """Populate database with sample data"""
    print("🌱 Seeding database...")

    # ============================================================
    # USERS
    # ============================================================
    print("  Creating users...")

    users_data = [
        {
            "email": "rachel@example.com",
            "password": "password123",
            "display_name": "Rachel Chen",
            "profile_photo_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
            "location": "Block 81",
            "bio": "Marketing manager who loves hiking with my corgi on weekends! Always looking for fellow dog lovers to connect with."
        },
        {
            "email": "david@example.com",
            "password": "password123",
            "display_name": "David Tan",
            "profile_photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150",
            "location": "Block 83",
            "bio": "Freelance designer working from home. Max and I love meeting new furry friends!"
        },
        {
            "email": "sarah@example.com",
            "password": "password123",
            "display_name": "Sarah Lee",
            "profile_photo_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150",
            "location": "Block 85",
            "bio": "Dog trainer and proud poodle mom. Happy to share tips and help with dog sitting!"
        },
        {
            "email": "michael@example.com",
            "password": "password123",
            "display_name": "Michael Wong",
            "profile_photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150",
            "location": "Block 87",
            "bio": "Software engineer with a hyper beagle. Looking for playdate buddies!"
        },
    ]

    users = []
    for user_data in users_data:
        user = User(
            email=user_data["email"],
            display_name=user_data["display_name"],
            profile_photo_url=user_data["profile_photo_url"],
            location=user_data["location"],
            bio=user_data["bio"]
        )
        user.set_password(user_data["password"])
        db.session.add(user)
        users.append(user)

    db.session.flush()  # Get IDs assigned

    # ============================================================
    # DOGS
    # ============================================================
    print("  Creating dogs...")

    dogs_data = [
        {
            "owner": users[0],
            "name": "Biscuit",
            "breed": "Corgi",
            "age": 2,
            "size": DogSize.MEDIUM,
            "temperament": "Friendly, energetic, loves belly rubs",
            "care_instructions": "Needs walk twice daily. No chicken in diet.",
            "photo_url": "https://images.unsplash.com/photo-1612536057832-2ff7ead58194?w=300"
        },
        {
            "owner": users[1],
            "name": "Max",
            "breed": "Golden Retriever",
            "age": 5,
            "size": DogSize.LARGE,
            "temperament": "Super friendly, gentle giant, great with other dogs",
            "care_instructions": "Joint supplements with morning meal. Loves fetch!",
            "photo_url": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=300"
        },
        {
            "owner": users[2],
            "name": "Coco",
            "breed": "Toy Poodle",
            "age": 3,
            "size": DogSize.SMALL,
            "temperament": "Smart, playful, can be shy at first",
            "care_instructions": "Hypoallergenic treats only. Groomed every 6 weeks.",
            "photo_url": "https://images.unsplash.com/photo-1616149256480-c8d51a2ae3e2?w=300"
        },
        {
            "owner": users[3],
            "name": "Buddy",
            "breed": "Beagle",
            "age": 1,
            "size": DogSize.MEDIUM,
            "temperament": "Very energetic, curious, follows his nose everywhere",
            "care_instructions": "Keep on leash outdoors - tends to chase scents. Loves treats!",
            "photo_url": "https://images.unsplash.com/photo-1505628346881-b72b27e84530?w=300"
        },
    ]

    dogs = []
    for dog_data in dogs_data:
        dog = Dog(
            owner_id=dog_data["owner"].id,
            name=dog_data["name"],
            breed=dog_data["breed"],
            age=dog_data["age"],
            size=dog_data["size"],
            temperament=dog_data["temperament"],
            care_instructions=dog_data["care_instructions"],
            photo_url=dog_data["photo_url"]
        )
        db.session.add(dog)
        dogs.append(dog)

    db.session.flush()

    # ============================================================
    # AVAILABILITY SLOTS
    # ============================================================
    print("  Creating availability slots...")

    today = date.today()

    slots_data = [
        # David's availability (user[1]) - works from home
        {"user": users[1], "days_ahead": 1, "start": time(9, 0), "end": time(12, 0), "notes": "Morning slots available. Can pick up from your place!"},
        {"user": users[1], "days_ahead": 1, "start": time(14, 0), "end": time(18, 0), "notes": "Afternoon availability"},
        {"user": users[1], "days_ahead": 2, "start": time(9, 0), "end": time(17, 0), "notes": "Full day available"},
        {"user": users[1], "days_ahead": 3, "start": time(10, 0), "end": time(15, 0), "notes": "", "status": SlotStatus.BOOKED},

        # Sarah's availability (user[2]) - dog trainer
        {"user": users[2], "days_ahead": 1, "start": time(8, 0), "end": time(11, 0), "notes": "Morning slot - great for high energy dogs!"},
        {"user": users[2], "days_ahead": 2, "start": time(15, 0), "end": time(19, 0), "notes": "Afternoon/evening. Small dogs preferred."},
        {"user": users[2], "days_ahead": 4, "start": time(9, 0), "end": time(18, 0), "notes": "Full day - can do training activities too!"},

        # Michael's availability (user[3])
        {"user": users[3], "days_ahead": 2, "start": time(18, 0), "end": time(21, 0), "notes": "Evening after work. Buddy needs a playmate!"},
        {"user": users[3], "days_ahead": 5, "start": time(10, 0), "end": time(16, 0), "notes": "Weekend availability. Planning to go to the dog park!"},

        # Rachel's availability (user[0]) - the default logged-in user
        {"user": users[0], "days_ahead": 3, "start": time(9, 0), "end": time(13, 0), "notes": "Work from home morning"},
        {"user": users[0], "days_ahead": 6, "start": time(14, 0), "end": time(20, 0), "notes": "Weekend afternoon - let's have a playdate!"},
    ]

    slots = []
    for slot_data in slots_data:
        slot = AvailabilitySlot(
            user_id=slot_data["user"].id,
            date=today + timedelta(days=slot_data["days_ahead"]),
            start_time=slot_data["start"],
            end_time=slot_data["end"],
            notes=slot_data.get("notes", ""),
            status=slot_data.get("status", SlotStatus.AVAILABLE)
        )
        db.session.add(slot)
        slots.append(slot)

    db.session.flush()

    # ============================================================
    # BOOKINGS
    # ============================================================
    print("  Creating bookings...")

    # Booking 1: Rachel requested David's booked slot (confirmed)
    booking1 = Booking(
        requester_id=users[0].id,
        provider_id=users[1].id,
        slot_id=slots[3].id,  # David's booked slot
        status=BookingStatus.CONFIRMED,
        message="Hi David! Could you watch Biscuit while I'm at a work meeting? He's super friendly and loves Golden Retrievers!",
        response_message="Of course! Max would love a playmate. See you then!",
        created_at=datetime.now() - timedelta(days=2)
    )
    db.session.add(booking1)

    # Booking 2: Michael requested Rachel's slot (pending)
    booking2 = Booking(
        requester_id=users[3].id,
        provider_id=users[0].id,
        slot_id=slots[9].id,  # Rachel's slot
        status=BookingStatus.PENDING,
        message="Hey Rachel! I have a vet appointment and can't bring Buddy. Could you watch him for a few hours? He's energetic but well-behaved!",
        created_at=datetime.now() - timedelta(hours=5)
    )
    db.session.add(booking2)

    # Booking 3: Rachel requested Sarah's slot (pending)
    booking3 = Booking(
        requester_id=users[0].id,
        provider_id=users[2].id,
        slot_id=slots[6].id,  # Sarah's full day slot
        status=BookingStatus.PENDING,
        message="Hi Sarah! I have a business trip coming up. Would love if Biscuit could spend the day with you and get some training!",
        created_at=datetime.now() - timedelta(hours=2)
    )
    db.session.add(booking3)

    db.session.flush()

    # ============================================================
    # POSTS
    # ============================================================
    print("  Creating community posts...")

    posts_data = [
        {
            "author": users[1],
            "type": PostType.PHOTO,
            "content": "Max and Biscuit had the best playdate today! These two are becoming best friends 🐕",
            "media_urls": ["https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600"],
            "likes_count": 12,
            "days_ago": 1
        },
        {
            "author": users[2],
            "type": PostType.EVENT,
            "content": "Community Dog Walk at East Coast Park! Let's meet up and let our pups socialize. All dogs welcome!",
            "event_date": datetime.now() + timedelta(days=7),
            "event_location": "East Coast Park, Car Park F1",
            "likes_count": 8,
            "days_ago": 2
        },
        {
            "author": users[3],
            "type": PostType.TEXT,
            "content": "Quick tip for fellow pawrents: The pet store at Tiong Bahru has a 20% off sale on treats this weekend! Buddy approved 👍",
            "likes_count": 5,
            "days_ago": 0.5
        },
        {
            "author": users[0],
            "type": PostType.PHOTO,
            "content": "Biscuit's first time at the beach! He was scared of the waves at first but now he can't stop running around 😂",
            "media_urls": ["https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?w=600"],
            "likes_count": 15,
            "days_ago": 3
        },
    ]

    for post_data in posts_data:
        post = Post(
            author_id=post_data["author"].id,
            type=post_data["type"],
            content=post_data["content"],
            media_urls=post_data.get("media_urls", []),
            event_date=post_data.get("event_date"),
            event_location=post_data.get("event_location", ""),
            likes_count=post_data.get("likes_count", 0),
            created_at=datetime.now() - timedelta(days=post_data["days_ago"])
        )
        db.session.add(post)

    db.session.flush()

    # ============================================================
    # NOTIFICATIONS for Rachel (user[0])
    # ============================================================
    print("  Creating notifications...")

    notifications_data = [
        {
            "title": "New Booking Request",
            "message": f"Michael Wong has requested your help on {(today + timedelta(days=3)).strftime('%b %d')}",
            "link": "/bookings",
            "is_read": False,
            "hours_ago": 5
        },
        {
            "title": "Booking Confirmed",
            "message": "Great news! David Tan accepted your booking.",
            "link": "/bookings",
            "is_read": True,
            "hours_ago": 48
        },
        {
            "title": "New Community Post",
            "message": "David Tan shared a photo of Max and Biscuit!",
            "link": "/feed",
            "is_read": True,
            "hours_ago": 24
        },
        {
            "title": "Upcoming Event",
            "message": "Community Dog Walk at East Coast Park is coming up!",
            "link": "/feed",
            "is_read": False,
            "hours_ago": 1
        },
    ]

    for notif_data in notifications_data:
        notif = Notification(
            user_id=users[0].id,
            title=notif_data["title"],
            message=notif_data["message"],
            link=notif_data.get("link", ""),
            is_read=notif_data.get("is_read", False),
            created_at=datetime.now() - timedelta(hours=notif_data["hours_ago"])
        )
        db.session.add(notif)

    # Commit all changes
    db.session.commit()

    print("✅ Database seeded successfully!")
    print(f"   - {len(users)} users created")
    print(f"   - {len(dogs)} dogs created")
    print(f"   - {len(slots)} availability slots created")
    print(f"   - 3 bookings created")
    print(f"   - {len(posts_data)} posts created")
    print(f"   - {len(notifications_data)} notifications created")
    print(f"\n📧 Demo login: rachel@example.com / password123")


def clear_database():
    """Clear all data from database"""
    print("🗑️  Clearing database...")
    db.drop_all()
    db.create_all()
    print("✅ Database cleared!")


if __name__ == '__main__':
    # This can be run directly for testing
    from app import create_app
    app = create_app()
    with app.app_context():
        clear_database()
        seed_database()
