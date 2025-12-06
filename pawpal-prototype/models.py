"""
Data models for PawPal - Dog Sitting Community Platform
"""
from dataclasses import dataclass, field
from datetime import datetime, date, time
from enum import Enum
from typing import Optional
import uuid


class DogSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class SlotStatus(Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    BLOCKED = "blocked"


class BookingStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class PostType(Enum):
    PHOTO = "photo"
    TEXT = "text"
    EVENT = "event"


@dataclass
class User:
    id: str
    email: str
    display_name: str
    profile_photo_url: str
    location: str
    bio: str
    created_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())


@dataclass
class Dog:
    id: str
    owner_id: str
    name: str
    breed: str
    age: int
    size: DogSize
    temperament: str
    care_instructions: str
    photo_url: str = ""

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())


@dataclass
class AvailabilitySlot:
    id: str
    user_id: str
    date: date
    start_time: time
    end_time: time
    status: SlotStatus = SlotStatus.AVAILABLE
    notes: str = ""
    is_recurring: bool = False
    recurrence_rule: str = ""

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())

    def time_range_str(self) -> str:
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


@dataclass
class Booking:
    id: str
    requester_id: str
    provider_id: str
    slot_id: str
    status: BookingStatus
    message: str
    response_message: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())


@dataclass
class Post:
    id: str
    author_id: str
    type: PostType
    content: str
    media_urls: list = field(default_factory=list)
    event_date: Optional[datetime] = None
    event_location: str = ""
    tagged_users: list = field(default_factory=list)
    likes: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())


@dataclass
class Notification:
    id: str
    user_id: str
    title: str
    message: str
    link: str = ""
    is_read: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())
