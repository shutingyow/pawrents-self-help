"""
Mock database with sample data for PawPal prototype
"""
from datetime import datetime, date, time, timedelta
from models import (
    User, Dog, AvailabilitySlot, Booking, Post, Notification,
    DogSize, SlotStatus, BookingStatus, PostType
)

# ============================================================
# USERS
# ============================================================
users = {
    "user-1": User(
        id="user-1",
        email="rachel@example.com",
        display_name="Rachel Chen",
        profile_photo_url="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
        location="Tanjong Pagar",
        bio="Marketing manager who loves hiking with my corgi on weekends! Always looking for fellow dog lovers to connect with.",
        created_at=datetime(2024, 1, 15)
    ),
    "user-2": User(
        id="user-2",
        email="david@example.com",
        display_name="David Tan",
        profile_photo_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150",
        location="Tiong Bahru",
        bio="Freelance designer working from home. Max and I love meeting new furry friends!",
        created_at=datetime(2024, 2, 1)
    ),
    "user-3": User(
        id="user-3",
        email="sarah@example.com",
        display_name="Sarah Lee",
        profile_photo_url="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150",
        location="Tanjong Pagar",
        bio="Dog trainer and proud poodle mom. Happy to share tips and help with dog sitting!",
        created_at=datetime(2024, 2, 20)
    ),
    "user-4": User(
        id="user-4",
        email="michael@example.com",
        display_name="Michael Wong",
        profile_photo_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150",
        location="Bukit Merah",
        bio="Software engineer with a hyper beagle. Looking for playdate buddies!",
        created_at=datetime(2024, 3, 5)
    ),
}

# ============================================================
# DOGS
# ============================================================
dogs = {
    "dog-1": Dog(
        id="dog-1",
        owner_id="user-1",
        name="Biscuit",
        breed="Corgi",
        age=2,
        size=DogSize.MEDIUM,
        temperament="Friendly, energetic, loves belly rubs",
        care_instructions="Needs walk twice daily. No chicken in diet.",
        photo_url="https://images.unsplash.com/photo-1612536057832-2ff7ead58194?w=300"
    ),
    "dog-2": Dog(
        id="dog-2",
        owner_id="user-2",
        name="Max",
        breed="Golden Retriever",
        age=5,
        size=DogSize.LARGE,
        temperament="Super friendly, gentle giant, great with other dogs",
        care_instructions="Joint supplements with morning meal. Loves fetch!",
        photo_url="https://images.unsplash.com/photo-1552053831-71594a27632d?w=300"
    ),
    "dog-3": Dog(
        id="dog-3",
        owner_id="user-3",
        name="Coco",
        breed="Toy Poodle",
        age=3,
        size=DogSize.SMALL,
        temperament="Smart, playful, can be shy at first",
        care_instructions="Hypoallergenic treats only. Groomed every 6 weeks.",
        photo_url="https://images.unsplash.com/photo-1616149256480-c8d51a2ae3e2?w=300"
    ),
    "dog-4": Dog(
        id="dog-4",
        owner_id="user-4",
        name="Buddy",
        breed="Beagle",
        age=1,
        size=DogSize.MEDIUM,
        temperament="Very energetic, curious, follows his nose everywhere",
        care_instructions="Keep on leash outdoors - tends to chase scents. Loves treats!",
        photo_url="https://images.unsplash.com/photo-1505628346881-b72b27e84530?w=300"
    ),
}

# ============================================================
# AVAILABILITY SLOTS (Next 7 days)
# ============================================================
today = date.today()

availability_slots = {
    # David's availability (user-2) - works from home, very flexible
    "slot-1": AvailabilitySlot(
        id="slot-1",
        user_id="user-2",
        date=today + timedelta(days=1),
        start_time=time(9, 0),
        end_time=time(12, 0),
        status=SlotStatus.AVAILABLE,
        notes="Morning slots available. Can pick up from your place!"
    ),
    "slot-2": AvailabilitySlot(
        id="slot-2",
        user_id="user-2",
        date=today + timedelta(days=1),
        start_time=time(14, 0),
        end_time=time(18, 0),
        status=SlotStatus.AVAILABLE,
        notes="Afternoon availability"
    ),
    "slot-3": AvailabilitySlot(
        id="slot-3",
        user_id="user-2",
        date=today + timedelta(days=2),
        start_time=time(9, 0),
        end_time=time(17, 0),
        status=SlotStatus.AVAILABLE,
        notes="Full day available"
    ),
    "slot-4": AvailabilitySlot(
        id="slot-4",
        user_id="user-2",
        date=today + timedelta(days=3),
        start_time=time(10, 0),
        end_time=time(15, 0),
        status=SlotStatus.BOOKED,
        notes=""
    ),

    # Sarah's availability (user-3) - dog trainer
    "slot-5": AvailabilitySlot(
        id="slot-5",
        user_id="user-3",
        date=today + timedelta(days=1),
        start_time=time(8, 0),
        end_time=time(11, 0),
        status=SlotStatus.AVAILABLE,
        notes="Morning slot - great for high energy dogs!"
    ),
    "slot-6": AvailabilitySlot(
        id="slot-6",
        user_id="user-3",
        date=today + timedelta(days=2),
        start_time=time(15, 0),
        end_time=time(19, 0),
        status=SlotStatus.AVAILABLE,
        notes="Afternoon/evening. Small dogs preferred."
    ),
    "slot-7": AvailabilitySlot(
        id="slot-7",
        user_id="user-3",
        date=today + timedelta(days=4),
        start_time=time(9, 0),
        end_time=time(18, 0),
        status=SlotStatus.AVAILABLE,
        notes="Full day - can do training activities too!"
    ),

    # Michael's availability (user-4)
    "slot-8": AvailabilitySlot(
        id="slot-8",
        user_id="user-4",
        date=today + timedelta(days=2),
        start_time=time(18, 0),
        end_time=time(21, 0),
        status=SlotStatus.AVAILABLE,
        notes="Evening after work. Buddy needs a playmate!"
    ),
    "slot-9": AvailabilitySlot(
        id="slot-9",
        user_id="user-4",
        date=today + timedelta(days=5),
        start_time=time(10, 0),
        end_time=time(16, 0),
        status=SlotStatus.AVAILABLE,
        notes="Weekend availability. Planning to go to the dog park!"
    ),

    # Rachel's availability (user-1) - the current logged-in user
    "slot-10": AvailabilitySlot(
        id="slot-10",
        user_id="user-1",
        date=today + timedelta(days=3),
        start_time=time(9, 0),
        end_time=time(13, 0),
        status=SlotStatus.AVAILABLE,
        notes="Work from home morning"
    ),
    "slot-11": AvailabilitySlot(
        id="slot-11",
        user_id="user-1",
        date=today + timedelta(days=6),
        start_time=time(14, 0),
        end_time=time(20, 0),
        status=SlotStatus.AVAILABLE,
        notes="Weekend afternoon - let's have a playdate!"
    ),
}

# ============================================================
# BOOKINGS
# ============================================================
bookings = {
    "booking-1": Booking(
        id="booking-1",
        requester_id="user-1",
        provider_id="user-2",
        slot_id="slot-4",
        status=BookingStatus.CONFIRMED,
        message="Hi David! Could you watch Biscuit while I'm at a work meeting? He's super friendly and loves Golden Retrievers!",
        response_message="Of course! Max would love a playmate. See you then!",
        created_at=datetime.now() - timedelta(days=2)
    ),
    "booking-2": Booking(
        id="booking-2",
        requester_id="user-4",
        provider_id="user-1",
        slot_id="slot-10",
        status=BookingStatus.PENDING,
        message="Hey Rachel! I have a vet appointment and can't bring Buddy. Could you watch him for a few hours? He's energetic but well-behaved!",
        created_at=datetime.now() - timedelta(hours=5)
    ),
    "booking-3": Booking(
        id="booking-3",
        requester_id="user-1",
        provider_id="user-3",
        slot_id="slot-7",
        status=BookingStatus.PENDING,
        message="Hi Sarah! I have a business trip coming up. Would love if Biscuit could spend the day with you and get some training!",
        created_at=datetime.now() - timedelta(hours=2)
    ),
}

# ============================================================
# COMMUNITY POSTS
# ============================================================
posts = {
    "post-1": Post(
        id="post-1",
        author_id="user-2",
        type=PostType.PHOTO,
        content="Max and Biscuit had the best playdate today! These two are becoming best friends 🐕",
        media_urls=["https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600"],
        likes=12,
        created_at=datetime.now() - timedelta(days=1)
    ),
    "post-2": Post(
        id="post-2",
        author_id="user-3",
        type=PostType.EVENT,
        content="Community Dog Walk at East Coast Park! Let's meet up and let our pups socialize. All dogs welcome!",
        event_date=datetime.now() + timedelta(days=7),
        event_location="East Coast Park, Car Park F1",
        likes=8,
        created_at=datetime.now() - timedelta(days=2)
    ),
    "post-3": Post(
        id="post-3",
        author_id="user-4",
        type=PostType.TEXT,
        content="Quick tip for fellow pawrents: The pet store at Tiong Bahru has a 20% off sale on treats this weekend! Buddy approved 👍",
        likes=5,
        created_at=datetime.now() - timedelta(hours=12)
    ),
    "post-4": Post(
        id="post-4",
        author_id="user-1",
        type=PostType.PHOTO,
        content="Biscuit's first time at the beach! He was scared of the waves at first but now he can't stop running around 😂",
        media_urls=["https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?w=600"],
        likes=15,
        created_at=datetime.now() - timedelta(days=3)
    ),
}

# ============================================================
# NOTIFICATIONS for user-1 (Rachel - current user)
# ============================================================
notifications = {
    "notif-1": Notification(
        id="notif-1",
        user_id="user-1",
        title="New Booking Request",
        message="Michael Wong has requested your help on " + (today + timedelta(days=3)).strftime("%b %d"),
        link="/bookings",
        is_read=False,
        created_at=datetime.now() - timedelta(hours=5)
    ),
    "notif-2": Notification(
        id="notif-2",
        user_id="user-1",
        title="Booking Confirmed",
        message="Great news! David Tan accepted your booking.",
        link="/bookings",
        is_read=True,
        created_at=datetime.now() - timedelta(days=2)
    ),
    "notif-3": Notification(
        id="notif-3",
        user_id="user-1",
        title="New Community Post",
        message="David Tan shared a photo of Max and Biscuit!",
        link="/feed",
        is_read=True,
        created_at=datetime.now() - timedelta(days=1)
    ),
    "notif-4": Notification(
        id="notif-4",
        user_id="user-1",
        title="Upcoming Event",
        message="Community Dog Walk at East Coast Park is coming up!",
        link="/feed",
        is_read=False,
        created_at=datetime.now() - timedelta(hours=1)
    ),
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

# Current logged-in user (for prototype)
CURRENT_USER_ID = "user-1"


def get_current_user():
    return users.get(CURRENT_USER_ID)


def get_user_dog(user_id):
    for dog in dogs.values():
        if dog.owner_id == user_id:
            return dog
    return None


def get_user_by_id(user_id):
    return users.get(user_id)


def get_available_slots_for_browse():
    """Get all available slots from other users"""
    result = []
    for slot in availability_slots.values():
        if slot.user_id != CURRENT_USER_ID and slot.status == SlotStatus.AVAILABLE:
            user = users.get(slot.user_id)
            dog = get_user_dog(slot.user_id)
            result.append({
                "slot": slot,
                "user": user,
                "dog": dog
            })
    return sorted(result, key=lambda x: (x["slot"].date, x["slot"].start_time))


def get_user_slots(user_id):
    """Get all slots for a specific user"""
    return [slot for slot in availability_slots.values() if slot.user_id == user_id]


def get_user_bookings(user_id):
    """Get all bookings where user is requester or provider"""
    result = []
    for booking in bookings.values():
        if booking.requester_id == user_id or booking.provider_id == user_id:
            slot = availability_slots.get(booking.slot_id)
            requester = users.get(booking.requester_id)
            provider = users.get(booking.provider_id)
            requester_dog = get_user_dog(booking.requester_id)
            result.append({
                "booking": booking,
                "slot": slot,
                "requester": requester,
                "provider": provider,
                "requester_dog": requester_dog,
                "is_provider": booking.provider_id == user_id
            })
    return sorted(result, key=lambda x: x["booking"].created_at, reverse=True)


def get_user_notifications(user_id):
    """Get notifications for a user"""
    result = [n for n in notifications.values() if n.user_id == user_id]
    return sorted(result, key=lambda x: x.created_at, reverse=True)


def get_unread_notification_count(user_id):
    return sum(1 for n in notifications.values() if n.user_id == user_id and not n.is_read)


def get_feed_posts():
    """Get all posts for the community feed"""
    result = []
    for post in posts.values():
        author = users.get(post.author_id)
        result.append({
            "post": post,
            "author": author
        })
    return sorted(result, key=lambda x: x["post"].created_at, reverse=True)
