"""
Database configuration and models for PawPal
"""
from datetime import datetime, date, time
from enum import Enum as PyEnum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


# ============================================================
# ENUMS
# ============================================================

class DogSize(PyEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class SlotStatus(PyEnum):
    AVAILABLE = "available"
    BOOKED = "booked"
    BLOCKED = "blocked"


class BookingStatus(PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class PostType(PyEnum):
    PHOTO = "photo"
    TEXT = "text"
    EVENT = "event"


# ============================================================
# MODELS
# ============================================================

class User(db.Model, UserMixin):
    """User model - represents a pawrent"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    profile_photo_url = db.Column(db.String(500), default='')
    location = db.Column(db.String(100), default='')
    bio = db.Column(db.Text, default='')
    phone = db.Column(db.String(20), default='')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    dogs = db.relationship('Dog', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    availability_slots = db.relationship('AvailabilitySlot', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    bookings_as_requester = db.relationship('Booking', foreign_keys='Booking.requester_id', backref='requester', lazy='dynamic')
    bookings_as_provider = db.relationship('Booking', foreign_keys='Booking.provider_id', backref='provider', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_dog(self):
        """Get user's first dog (primary dog)"""
        return self.dogs.first()

    def __repr__(self):
        return f'<User {self.display_name}>'


class Dog(db.Model):
    """Dog model - represents a user's dog"""
    __tablename__ = 'dogs'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100), default='')
    age = db.Column(db.Integer, default=0)
    size = db.Column(db.Enum(DogSize), default=DogSize.MEDIUM)
    temperament = db.Column(db.Text, default='')
    care_instructions = db.Column(db.Text, default='')
    photo_url = db.Column(db.String(500), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Dog {self.name}>'


class AvailabilitySlot(db.Model):
    """Availability slot model - time slots when a user can help"""
    __tablename__ = 'availability_slots'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.Enum(SlotStatus), default=SlotStatus.AVAILABLE)
    notes = db.Column(db.Text, default='')
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_rule = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bookings = db.relationship('Booking', backref='slot', lazy='dynamic')

    def time_range_str(self):
        """Return formatted time range string"""
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

    def __repr__(self):
        return f'<AvailabilitySlot {self.date} {self.start_time}-{self.end_time}>'


class Booking(db.Model):
    """Booking model - dog-sitting request between users"""
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('availability_slots.id'), nullable=False, index=True)
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.PENDING)
    message = db.Column(db.Text, default='')
    response_message = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Booking {self.id} {self.status.value}>'


class Post(db.Model):
    """Post model - community feed posts"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    type = db.Column(db.Enum(PostType), default=PostType.TEXT)
    content = db.Column(db.Text, nullable=False)
    media_urls = db.Column(db.JSON, default=list)  # List of photo URLs
    event_date = db.Column(db.DateTime, nullable=True)
    event_location = db.Column(db.String(255), default='')
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('PostLike', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Post {self.id} by {self.author_id}>'


class Comment(db.Model):
    """Comment model - comments on posts"""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    author = db.relationship('User', backref='comments')

    def __repr__(self):
        return f'<Comment {self.id}>'


class PostLike(db.Model):
    """Like model - likes on posts"""
    __tablename__ = 'post_likes'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint - user can only like a post once
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_like'),)


class Notification(db.Model):
    """Notification model - user notifications"""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), default='')
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification {self.id} for {self.user_id}>'


class Conversation(db.Model):
    """Conversation model - chat thread between two users"""
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=True, index=True)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user1 = db.relationship('User', foreign_keys=[user1_id], backref='conversations_as_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='conversations_as_user2')
    booking = db.relationship('Booking', backref='conversation')
    messages = db.relationship('Message', backref='conversation', lazy='dynamic', cascade='all, delete-orphan')

    def get_other_user(self, current_user_id):
        """Get the other participant in the conversation"""
        if self.user1_id == current_user_id:
            return User.query.get(self.user2_id)
        return User.query.get(self.user1_id)

    def get_unread_count(self, user_id):
        """Get count of unread messages for a user"""
        return Message.query.filter_by(
            conversation_id=self.id,
            is_read=False
        ).filter(Message.sender_id != user_id).count()

    def __repr__(self):
        return f'<Conversation {self.id} between {self.user1_id} and {self.user2_id}>'


class Message(db.Model):
    """Message model - individual chat messages"""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    sender = db.relationship('User', backref='sent_messages')

    def __repr__(self):
        return f'<Message {self.id} from {self.sender_id}>'


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_available_slots_for_browse(current_user_id):
    """Get all available slots from other users"""
    from datetime import date as date_module
    today = date_module.today()

    slots = AvailabilitySlot.query.filter(
        AvailabilitySlot.user_id != current_user_id,
        AvailabilitySlot.status == SlotStatus.AVAILABLE,
        AvailabilitySlot.date >= today
    ).order_by(AvailabilitySlot.date, AvailabilitySlot.start_time).all()

    result = []
    for slot in slots:
        user = User.query.get(slot.user_id)
        dog = user.get_dog() if user else None
        result.append({
            "slot": slot,
            "user": user,
            "dog": dog
        })
    return result


def get_available_slots_filtered(current_user_id, date_range=7, time_of_day='', dog_size='', block=''):
    """Get available slots with filters applied"""
    from datetime import date as date_module, timedelta, time as time_type
    today = date_module.today()
    end_date = today + timedelta(days=date_range)

    # Base query
    query = AvailabilitySlot.query.filter(
        AvailabilitySlot.user_id != current_user_id,
        AvailabilitySlot.status == SlotStatus.AVAILABLE,
        AvailabilitySlot.date >= today,
        AvailabilitySlot.date <= end_date
    )

    # Time of day filter
    if time_of_day == 'morning':
        query = query.filter(AvailabilitySlot.start_time >= time_type(6, 0),
                            AvailabilitySlot.start_time < time_type(12, 0))
    elif time_of_day == 'afternoon':
        query = query.filter(AvailabilitySlot.start_time >= time_type(12, 0),
                            AvailabilitySlot.start_time < time_type(18, 0))
    elif time_of_day == 'evening':
        query = query.filter(AvailabilitySlot.start_time >= time_type(18, 0),
                            AvailabilitySlot.start_time < time_type(22, 0))

    slots = query.order_by(AvailabilitySlot.date, AvailabilitySlot.start_time).all()

    result = []
    for slot in slots:
        user = User.query.get(slot.user_id)
        if not user:
            continue

        # Block filter
        if block and user.location != block:
            continue

        dog = user.get_dog()

        # Dog size filter
        if dog_size and dog:
            if dog.size.value != dog_size:
                continue

        result.append({
            "slot": slot,
            "user": user,
            "dog": dog
        })

    return result


def get_user_bookings(user_id):
    """Get all bookings where user is requester or provider"""
    bookings_list = Booking.query.filter(
        db.or_(Booking.requester_id == user_id, Booking.provider_id == user_id)
    ).order_by(Booking.created_at.desc()).all()

    result = []
    for booking in bookings_list:
        slot = AvailabilitySlot.query.get(booking.slot_id)
        requester = User.query.get(booking.requester_id)
        provider = User.query.get(booking.provider_id)
        requester_dog = requester.get_dog() if requester else None
        result.append({
            "booking": booking,
            "slot": slot,
            "requester": requester,
            "provider": provider,
            "requester_dog": requester_dog,
            "is_provider": booking.provider_id == user_id
        })
    return result


def get_user_notifications(user_id):
    """Get notifications for a user"""
    return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()


def get_unread_notification_count(user_id):
    """Get count of unread notifications"""
    return Notification.query.filter_by(user_id=user_id, is_read=False).count()


def get_feed_posts():
    """Get all posts for the community feed"""
    posts_list = Post.query.order_by(Post.created_at.desc()).all()
    result = []
    for post in posts_list:
        author = User.query.get(post.author_id)
        result.append({
            "post": post,
            "author": author
        })
    return result


def get_or_create_conversation(user1_id, user2_id, booking_id=None):
    """Get existing conversation or create a new one"""
    # Always store the lower ID as user1_id for consistency
    if user1_id > user2_id:
        user1_id, user2_id = user2_id, user1_id

    conversation = Conversation.query.filter_by(
        user1_id=user1_id,
        user2_id=user2_id
    ).first()

    if not conversation:
        conversation = Conversation(
            user1_id=user1_id,
            user2_id=user2_id,
            booking_id=booking_id
        )
        db.session.add(conversation)
        db.session.commit()

    return conversation


def get_user_conversations(user_id):
    """Get all conversations for a user"""
    conversations = Conversation.query.filter(
        db.or_(Conversation.user1_id == user_id, Conversation.user2_id == user_id)
    ).order_by(Conversation.last_message_at.desc()).all()

    result = []
    for conv in conversations:
        other_user = conv.get_other_user(user_id)
        last_message = conv.messages.order_by(Message.created_at.desc()).first()
        unread_count = conv.get_unread_count(user_id)

        result.append({
            "conversation": conv,
            "other_user": other_user,
            "last_message": last_message,
            "unread_count": unread_count
        })

    return result


def get_total_unread_messages(user_id):
    """Get total count of unread messages for a user"""
    conversations = Conversation.query.filter(
        db.or_(Conversation.user1_id == user_id, Conversation.user2_id == user_id)
    ).all()

    total = 0
    for conv in conversations:
        total += conv.get_unread_count(user_id)
    return total
