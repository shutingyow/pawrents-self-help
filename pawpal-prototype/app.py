"""
PawPal - Dog Sitting Community Platform
Flask Application with Database Support
"""
import os
import uuid
from datetime import datetime, date, time, timedelta
import calendar
from pathlib import Path

# Allow OAuth over HTTP for local development (not in production)
if os.environ.get('FLASK_CONFIG') != 'production':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from flask_dance.contrib.google import make_google_blueprint, google

from config import config
from database import (
    db, bcrypt, User, Dog, AvailabilitySlot, Booking, Post, Notification,
    Conversation, Message,
    DogSize, SlotStatus, BookingStatus, PostType,
    get_available_slots_for_browse, get_available_slots_filtered, get_user_bookings,
    get_user_notifications, get_unread_notification_count, get_feed_posts,
    get_or_create_conversation, get_user_conversations, get_total_unread_messages
)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def save_uploaded_file(file, subfolder=''):
    """Save uploaded file and return the URL path"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"

        # Create subfolder if specified
        upload_path = Path(current_app.config['UPLOAD_FOLDER'])
        if subfolder:
            upload_path = upload_path / subfolder
            upload_path.mkdir(parents=True, exist_ok=True)

        # Save file
        file_path = upload_path / filename
        file.save(str(file_path))

        # Return URL path
        if subfolder:
            return f"/static/uploads/{subfolder}/{filename}"
        return f"/static/uploads/{filename}"
    return None


def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Context processor for global template variables
    @app.context_processor
    def inject_globals():
        if current_user.is_authenticated:
            return {
                'current_user': current_user,
                'notification_count': get_unread_notification_count(current_user.id),
                'message_count': get_total_unread_messages(current_user.id),
                'now': datetime.now(),
                'today': date.today()
            }
        return {
            'now': datetime.now(),
            'today': date.today()
        }

    # Setup Google OAuth (only if credentials are configured)
    if app.config.get('GOOGLE_OAUTH_CLIENT_ID') and app.config.get('GOOGLE_OAUTH_CLIENT_SECRET'):
        google_bp = make_google_blueprint(
            client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
            client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
            scope=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
            redirect_url='/google-callback'
        )
        app.register_blueprint(google_bp, url_prefix='/login')

    # ============================================================
    # AUTHENTICATION ROUTES
    # ============================================================

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')

            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                login_user(user)
                flash(f'Welcome back, {user.display_name}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home'))
            else:
                flash('Invalid email or password.', 'error')

        return render_template('login.html')

    @app.route('/google-callback')
    def google_callback():
        """Handle Google OAuth callback"""
        if not google.authorized:
            flash('Failed to log in with Google.', 'error')
            return redirect(url_for('login'))

        try:
            resp = google.get('/oauth2/v2/userinfo')
            if resp.ok:
                google_info = resp.json()
                email = google_info.get('email', '').lower()
                name = google_info.get('name', '')
                picture = google_info.get('picture', '')

                # Check if user exists
                user = User.query.filter_by(email=email).first()

                if user:
                    # Existing user - log them in
                    login_user(user)
                    flash(f'Welcome back, {user.display_name}!', 'success')
                    return redirect(url_for('home'))
                else:
                    # New user - create account
                    user = User(
                        email=email,
                        display_name=name,
                        profile_photo_url=picture,
                        location=''
                    )
                    # Set a random password (user won't need it for OAuth)
                    user.set_password(os.urandom(32).hex())
                    db.session.add(user)
                    db.session.commit()

                    login_user(user)
                    flash('Account created successfully! Please add your dog to get started.', 'success')
                    return redirect(url_for('add_dog'))
            else:
                flash('Failed to get user info from Google.', 'error')
                return redirect(url_for('login'))
        except Exception as e:
            flash('An error occurred during Google sign-in.', 'error')
            return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            display_name = request.form.get('display_name', '').strip()
            location = request.form.get('location', '').strip()

            # Validation
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'error')
                return render_template('register.html')

            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('register.html')

            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'error')
                return render_template('register.html')

            # Create user
            user = User(
                email=email,
                display_name=display_name,
                location=location
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash('Account created successfully! Add your dog to get started.', 'success')
            return redirect(url_for('add_dog'))

        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    # ============================================================
    # MAIN ROUTES
    # ============================================================

    @app.route('/')
    @login_required
    def home():
        user_dog = current_user.get_dog()

        # Redirect to add dog if user hasn't added one yet
        if not user_dog:
            flash('Please add your dog to get started!', 'info')
            return redirect(url_for('add_dog'))

        user_bookings = get_user_bookings(current_user.id)

        pending_requests = sum(1 for b in user_bookings
                               if b['booking'].status == BookingStatus.PENDING and b['is_provider'])
        upcoming_bookings = sum(1 for b in user_bookings
                                if b['booking'].status == BookingStatus.CONFIRMED)
        available_slots = AvailabilitySlot.query.filter(
            AvailabilitySlot.user_id != current_user.id,
            AvailabilitySlot.status == SlotStatus.AVAILABLE,
            AvailabilitySlot.date >= date.today()
        ).count()

        return render_template('home.html',
                               active_page='home',
                               user_dog=user_dog,
                               pending_requests=pending_requests,
                               upcoming_bookings=upcoming_bookings,
                               available_slots=available_slots,
                               community_members=User.query.count(),
                               recent_notifications=get_user_notifications(current_user.id)[:4],
                               nearby_available=get_available_slots_for_browse(current_user.id))

    @app.route('/browse')
    @login_required
    def browse():
        # Get filter parameters
        date_range = request.args.get('date_range', '7')
        time_of_day = request.args.get('time_of_day', '')
        dog_size = request.args.get('dog_size', '')
        block_filter = request.args.get('block', '')

        # Get available slots with filters
        available = get_available_slots_filtered(
            current_user.id,
            date_range=int(date_range) if date_range else 7,
            time_of_day=time_of_day,
            dog_size=dog_size,
            block=block_filter
        )

        return render_template('browse.html',
                               active_page='browse',
                               available_slots=available,
                               date_range=date_range,
                               time_of_day=time_of_day,
                               dog_size=dog_size,
                               block_filter=block_filter)

    @app.route('/book/<int:slot_id>')
    @login_required
    def book(slot_id):
        slot = AvailabilitySlot.query.get_or_404(slot_id)

        if slot.user_id == current_user.id:
            flash("You can't book your own availability slot.", 'error')
            return redirect(url_for('browse'))

        if slot.status != SlotStatus.AVAILABLE:
            flash('This slot is no longer available.', 'error')
            return redirect(url_for('browse'))

        provider = User.query.get(slot.user_id)
        user_dog = current_user.get_dog()

        return render_template('book.html',
                               active_page='browse',
                               slot=slot,
                               provider=provider,
                               user_dog=user_dog)

    @app.route('/book/<int:slot_id>/submit', methods=['POST'])
    @login_required
    def submit_booking(slot_id):
        slot = AvailabilitySlot.query.get_or_404(slot_id)

        if slot.status != SlotStatus.AVAILABLE:
            flash('This slot is no longer available.', 'error')
            return redirect(url_for('browse'))

        message = request.form.get('message', '')
        provider = User.query.get(slot.user_id)

        # Create new booking
        booking = Booking(
            requester_id=current_user.id,
            provider_id=slot.user_id,
            slot_id=slot_id,
            status=BookingStatus.PENDING,
            message=message
        )
        db.session.add(booking)

        # Create notification for provider
        notification = Notification(
            user_id=slot.user_id,
            title="New Booking Request",
            message=f"{current_user.display_name} has requested your help on {slot.date.strftime('%b %d')}",
            link="/bookings"
        )
        db.session.add(notification)

        db.session.commit()

        return render_template('booking_success.html',
                               active_page='browse',
                               provider=provider,
                               slot=slot)

    @app.route('/bookings')
    @login_required
    def my_bookings():
        user_bookings = get_user_bookings(current_user.id)
        return render_template('bookings.html',
                               active_page='bookings',
                               user_bookings=user_bookings)

    @app.route('/bookings/<int:booking_id>/accept')
    @login_required
    def accept_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)

        if booking.provider_id != current_user.id:
            flash('Unauthorized action.', 'error')
            return redirect(url_for('my_bookings'))

        booking.status = BookingStatus.CONFIRMED
        booking.response_message = "Looking forward to it!"

        # Mark slot as booked
        slot = AvailabilitySlot.query.get(booking.slot_id)
        if slot:
            slot.status = SlotStatus.BOOKED

        # Notify requester
        notification = Notification(
            user_id=booking.requester_id,
            title="Booking Confirmed",
            message=f"Great news! {current_user.display_name} accepted your booking.",
            link="/bookings"
        )
        db.session.add(notification)

        db.session.commit()
        flash('Booking accepted!', 'success')
        return redirect(url_for('my_bookings'))

    @app.route('/bookings/<int:booking_id>/decline')
    @login_required
    def decline_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)

        if booking.provider_id != current_user.id:
            flash('Unauthorized action.', 'error')
            return redirect(url_for('my_bookings'))

        booking.status = BookingStatus.DECLINED
        booking.response_message = "Sorry, I'm not able to help this time."

        # Notify requester
        notification = Notification(
            user_id=booking.requester_id,
            title="Booking Declined",
            message=f"{current_user.display_name} couldn't accept your request.",
            link="/bookings"
        )
        db.session.add(notification)

        db.session.commit()
        flash('Booking declined.', 'info')
        return redirect(url_for('my_bookings'))

    @app.route('/bookings/<int:booking_id>/cancel')
    @login_required
    def cancel_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)

        if booking.requester_id != current_user.id:
            flash('Unauthorized action.', 'error')
            return redirect(url_for('my_bookings'))

        booking.status = BookingStatus.CANCELLED

        # Release the slot if it was booked
        slot = AvailabilitySlot.query.get(booking.slot_id)
        if slot and slot.status == SlotStatus.BOOKED:
            slot.status = SlotStatus.AVAILABLE

        db.session.commit()
        flash('Booking cancelled.', 'info')
        return redirect(url_for('my_bookings'))

    @app.route('/calendar')
    @login_required
    def my_calendar():
        # Get month/year from query params or use current
        try:
            month = int(request.args.get('month', date.today().month))
            year = int(request.args.get('year', date.today().year))
        except (ValueError, TypeError):
            month = date.today().month
            year = date.today().year

        # Ensure valid month
        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1

        my_slots = AvailabilitySlot.query.filter_by(user_id=current_user.id).order_by(
            AvailabilitySlot.date, AvailabilitySlot.start_time
        ).all()

        # Calculate prev/next month
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1

        return render_template('calendar.html',
                               active_page='calendar',
                               my_slots=my_slots,
                               calendar_weeks=get_calendar_weeks(current_user.id, month, year),
                               current_month=date(year, month, 1).strftime('%B %Y'),
                               prev_month=prev_month,
                               prev_year=prev_year,
                               next_month=next_month,
                               next_year=next_year)

    @app.route('/calendar/add', methods=['POST'])
    @login_required
    def add_availability():
        slot_date = request.form.get('date')
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
        notes = request.form.get('notes', '')

        if slot_date and start_time_str and end_time_str:
            slot = AvailabilitySlot(
                user_id=current_user.id,
                date=datetime.strptime(slot_date, '%Y-%m-%d').date(),
                start_time=datetime.strptime(start_time_str, '%H:%M').time(),
                end_time=datetime.strptime(end_time_str, '%H:%M').time(),
                status=SlotStatus.AVAILABLE,
                notes=notes
            )
            db.session.add(slot)
            db.session.commit()
            flash('Availability added!', 'success')

        return redirect(url_for('my_calendar'))

    @app.route('/calendar/delete/<int:slot_id>')
    @login_required
    def delete_availability(slot_id):
        slot = AvailabilitySlot.query.get_or_404(slot_id)

        if slot.user_id != current_user.id:
            flash('Unauthorized action.', 'error')
            return redirect(url_for('my_calendar'))

        if slot.status == SlotStatus.BOOKED:
            flash('Cannot delete a booked slot.', 'error')
            return redirect(url_for('my_calendar'))

        db.session.delete(slot)
        db.session.commit()
        flash('Availability slot deleted.', 'info')
        return redirect(url_for('my_calendar'))

    @app.route('/profile')
    @login_required
    def profile():
        user_dog = current_user.get_dog()

        # Redirect to add dog if user hasn't added one yet
        if not user_dog:
            flash('Please add your dog to get started!', 'info')
            return redirect(url_for('add_dog'))

        return render_template('profile.html',
                               active_page='profile',
                               user_dog=user_dog)

    @app.route('/profile/edit', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        if request.method == 'POST':
            current_user.display_name = request.form.get('display_name', current_user.display_name).strip()
            current_user.location = request.form.get('location', current_user.location).strip()
            current_user.bio = request.form.get('bio', current_user.bio).strip()

            # Handle photo upload
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo and photo.filename:
                    photo_url = save_uploaded_file(photo, 'profiles')
                    if photo_url:
                        current_user.profile_photo_url = photo_url

            db.session.commit()
            flash('Profile updated!', 'success')
            return redirect(url_for('profile'))

        return render_template('edit_profile.html', active_page='profile')

    @app.route('/profile/upload-photo', methods=['POST'])
    @login_required
    def upload_profile_photo():
        if 'photo' not in request.files:
            flash('No photo selected.', 'error')
            return redirect(url_for('profile'))

        photo = request.files['photo']
        if photo.filename == '':
            flash('No photo selected.', 'error')
            return redirect(url_for('profile'))

        photo_url = save_uploaded_file(photo, 'profiles')
        if photo_url:
            current_user.profile_photo_url = photo_url
            db.session.commit()
            flash('Profile photo updated!', 'success')
        else:
            flash('Invalid file type. Please upload an image (PNG, JPG, GIF, WebP).', 'error')

        return redirect(url_for('profile'))

    @app.route('/dog/add', methods=['GET', 'POST'])
    @login_required
    def add_dog():
        if request.method == 'POST':
            # Handle photo upload
            photo_url = ''
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo and photo.filename:
                    uploaded_url = save_uploaded_file(photo, 'dogs')
                    if uploaded_url:
                        photo_url = uploaded_url

            dog = Dog(
                owner_id=current_user.id,
                name=request.form.get('name', '').strip(),
                breed=request.form.get('breed', '').strip(),
                age=int(request.form.get('age', 0)),
                size=DogSize(request.form.get('size', 'medium')),
                temperament=request.form.get('temperament', '').strip(),
                care_instructions=request.form.get('care_instructions', '').strip(),
                photo_url=photo_url
            )
            db.session.add(dog)
            db.session.commit()
            flash(f'{dog.name} has been added!', 'success')
            return redirect(url_for('profile'))

        return render_template('add_dog.html', active_page='profile')

    @app.route('/dog/edit/<int:dog_id>', methods=['GET', 'POST'])
    @login_required
    def edit_dog(dog_id):
        dog = Dog.query.get_or_404(dog_id)

        if dog.owner_id != current_user.id:
            flash('Unauthorized action.', 'error')
            return redirect(url_for('profile'))

        if request.method == 'POST':
            dog.name = request.form.get('name', dog.name).strip()
            dog.breed = request.form.get('breed', dog.breed).strip()
            dog.age = int(request.form.get('age', dog.age))
            dog.size = DogSize(request.form.get('size', dog.size.value))
            dog.temperament = request.form.get('temperament', dog.temperament).strip()
            dog.care_instructions = request.form.get('care_instructions', dog.care_instructions).strip()

            # Handle photo upload
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo and photo.filename:
                    photo_url = save_uploaded_file(photo, 'dogs')
                    if photo_url:
                        dog.photo_url = photo_url

            db.session.commit()
            flash(f'{dog.name}\'s profile updated!', 'success')
            return redirect(url_for('profile'))

        return render_template('edit_dog.html', active_page='profile', dog=dog)

    @app.route('/dog/<int:dog_id>/upload-photo', methods=['POST'])
    @login_required
    def upload_dog_photo(dog_id):
        dog = Dog.query.get_or_404(dog_id)

        if dog.owner_id != current_user.id:
            flash('Unauthorized action.', 'error')
            return redirect(url_for('profile'))

        if 'photo' not in request.files:
            flash('No photo selected.', 'error')
            return redirect(url_for('profile'))

        photo = request.files['photo']
        if photo.filename == '':
            flash('No photo selected.', 'error')
            return redirect(url_for('profile'))

        photo_url = save_uploaded_file(photo, 'dogs')
        if photo_url:
            dog.photo_url = photo_url
            db.session.commit()
            flash(f'{dog.name}\'s photo updated!', 'success')
        else:
            flash('Invalid file type. Please upload an image (PNG, JPG, GIF, WebP).', 'error')

        return redirect(url_for('profile'))

    # ============================================================
    # SETTINGS ROUTES
    # ============================================================

    @app.route('/settings/notifications', methods=['GET', 'POST'])
    @login_required
    def settings_notifications():
        if request.method == 'POST':
            # In a real app, save these preferences to the database
            flash('Notification preferences saved!', 'success')
            return redirect(url_for('settings_notifications'))

        return render_template('settings.html',
                               active_page='profile',
                               setting_type='notifications',
                               title='Notification Preferences',
                               subtitle='Manage how you receive notifications')

    @app.route('/settings/privacy', methods=['GET', 'POST'])
    @login_required
    def settings_privacy():
        if request.method == 'POST':
            flash('Privacy settings saved!', 'success')
            return redirect(url_for('settings_privacy'))

        return render_template('settings.html',
                               active_page='profile',
                               setting_type='privacy',
                               title='Privacy & Security',
                               subtitle='Manage your password and privacy settings')

    @app.route('/settings/change-password', methods=['POST'])
    @login_required
    def change_password():
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('settings_privacy'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return redirect(url_for('settings_privacy'))

        if len(new_password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('settings_privacy'))

        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('settings_privacy'))

    @app.route('/settings/location', methods=['GET', 'POST'])
    @login_required
    def settings_location():
        if request.method == 'POST':
            location = request.form.get('location', '').strip()
            current_user.location = location
            db.session.commit()
            flash('Location updated!', 'success')
            return redirect(url_for('settings_location'))

        return render_template('settings.html',
                               active_page='profile',
                               setting_type='location',
                               title='Location Settings',
                               subtitle='Update your neighbourhood')

    @app.route('/settings/help')
    @login_required
    def settings_help():
        return render_template('settings.html',
                               active_page='profile',
                               setting_type='help',
                               title='Help & Support',
                               subtitle='FAQs and contact support')

    @app.route('/settings/delete-account')
    @login_required
    def delete_account():
        user_id = current_user.id
        logout_user()

        # Delete user's data
        user = User.query.get(user_id)
        if user:
            # Delete related data
            Dog.query.filter_by(owner_id=user_id).delete()
            AvailabilitySlot.query.filter_by(user_id=user_id).delete()
            Booking.query.filter((Booking.requester_id == user_id) | (Booking.provider_id == user_id)).delete()
            Notification.query.filter_by(user_id=user_id).delete()
            Post.query.filter_by(author_id=user_id).delete()
            Message.query.filter_by(sender_id=user_id).delete()
            Conversation.query.filter((Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)).delete()
            db.session.delete(user)
            db.session.commit()

        flash('Your account has been deleted.', 'info')
        return redirect(url_for('login'))

    @app.route('/feed')
    @login_required
    def feed():
        return render_template('feed.html',
                               active_page='feed',
                               posts=get_feed_posts())

    @app.route('/feed/post', methods=['POST'])
    @login_required
    def create_post():
        content = request.form.get('content', '').strip()
        post_type = request.form.get('type', 'text')

        if content:
            post = Post(
                author_id=current_user.id,
                type=PostType(post_type),
                content=content
            )
            db.session.add(post)
            db.session.commit()
            flash('Post shared!', 'success')

        return redirect(url_for('feed'))

    @app.route('/notifications')
    @login_required
    def view_notifications():
        notifications = get_user_notifications(current_user.id)
        return render_template('notifications.html',
                               active_page='notifications',
                               notifications=notifications)

    @app.route('/notifications/mark-read')
    @login_required
    def mark_notifications_read():
        Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
        db.session.commit()
        return redirect(url_for('view_notifications'))

    # ============================================================
    # MESSAGING ROUTES
    # ============================================================

    @app.route('/messages')
    @login_required
    def messages_inbox():
        """View all conversations"""
        conversations = get_user_conversations(current_user.id)
        return render_template('messages.html',
                               active_page='messages',
                               conversations=conversations)

    @app.route('/messages/<int:user_id>')
    @login_required
    def conversation_view(user_id):
        """View conversation with a specific user"""
        other_user = User.query.get_or_404(user_id)
        if other_user.id == current_user.id:
            return redirect(url_for('messages_inbox'))

        conversation = get_or_create_conversation(current_user.id, other_user.id)
        messages_list = conversation.messages.order_by(Message.created_at.asc()).all()

        # Mark messages as read
        Message.query.filter_by(
            conversation_id=conversation.id,
            is_read=False
        ).filter(Message.sender_id != current_user.id).update({'is_read': True})
        db.session.commit()

        return render_template('conversation.html',
                               active_page='messages',
                               conversation=conversation,
                               other_user=other_user,
                               messages=messages_list)

    @app.route('/messages/<int:user_id>/send', methods=['POST'])
    @login_required
    def send_message(user_id):
        """Send a message to a user"""
        other_user = User.query.get_or_404(user_id)
        content = request.form.get('content', '').strip()

        if content and other_user.id != current_user.id:
            conversation = get_or_create_conversation(current_user.id, other_user.id)

            message = Message(
                conversation_id=conversation.id,
                sender_id=current_user.id,
                content=content
            )
            db.session.add(message)

            # Update conversation last_message_at
            conversation.last_message_at = datetime.now()

            # Create notification for recipient
            notification = Notification(
                user_id=other_user.id,
                title='New Message',
                message=f'{current_user.display_name} sent you a message',
                link=f'/messages/{current_user.id}'
            )
            db.session.add(notification)
            db.session.commit()

        return redirect(url_for('conversation_view', user_id=user_id))

    @app.route('/messages/start/<int:user_id>')
    @login_required
    def start_conversation(user_id):
        """Start a new conversation with a user (redirect to conversation view)"""
        return redirect(url_for('conversation_view', user_id=user_id))

    # ============================================================
    # CALENDAR EXPORT ROUTES
    # ============================================================

    @app.route('/booking/<int:booking_id>/calendar')
    @login_required
    def export_booking_to_calendar(booking_id):
        """Export booking to calendar (ICS format)"""
        booking = Booking.query.get_or_404(booking_id)

        # Check authorization
        if booking.requester_id != current_user.id and booking.provider_id != current_user.id:
            flash('Unauthorized action.', 'error')
            return redirect(url_for('my_bookings'))

        slot = AvailabilitySlot.query.get(booking.slot_id)
        other_user = User.query.get(
            booking.provider_id if booking.requester_id == current_user.id else booking.requester_id
        )
        requester_dog = User.query.get(booking.requester_id).get_dog()

        # Build ICS content
        start_datetime = datetime.combine(slot.date, slot.start_time)
        end_datetime = datetime.combine(slot.date, slot.end_time)

        # Format for ICS
        dtstart = start_datetime.strftime('%Y%m%dT%H%M%S')
        dtend = end_datetime.strftime('%Y%m%dT%H%M%S')
        dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
        uid = f'pawpal-booking-{booking.id}@pawpal.app'

        if booking.requester_id == current_user.id:
            summary = f'Dog Sitting: {requester_dog.name if requester_dog else "Your dog"} with {other_user.display_name}'
            description = f'Your dog will be cared for by {other_user.display_name}\\nLocation: {other_user.location}\\n\\nContact: Open PawPal to message'
        else:
            summary = f'Dog Sitting: Caring for {requester_dog.name if requester_dog else "dog"}'
            description = f'You are caring for {requester_dog.name if requester_dog else "a dog"} for {other_user.display_name}\\nContact: Open PawPal to message'

        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//PawPal//Dog Sitting//EN
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{summary}
DESCRIPTION:{description}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR"""

        response = app.response_class(
            response=ics_content,
            status=200,
            mimetype='text/calendar'
        )
        response.headers['Content-Disposition'] = f'attachment; filename=pawpal-booking-{booking.id}.ics'
        return response

    @app.route('/booking/<int:booking_id>/google-calendar')
    @login_required
    def add_to_google_calendar(booking_id):
        """Generate Google Calendar link for booking"""
        booking = Booking.query.get_or_404(booking_id)

        # Check authorization
        if booking.requester_id != current_user.id and booking.provider_id != current_user.id:
            flash('Unauthorized action.', 'error')
            return redirect(url_for('my_bookings'))

        slot = AvailabilitySlot.query.get(booking.slot_id)
        other_user = User.query.get(
            booking.provider_id if booking.requester_id == current_user.id else booking.requester_id
        )
        requester_dog = User.query.get(booking.requester_id).get_dog()

        # Build dates for Google Calendar
        start_datetime = datetime.combine(slot.date, slot.start_time)
        end_datetime = datetime.combine(slot.date, slot.end_time)

        dates = f"{start_datetime.strftime('%Y%m%dT%H%M%S')}/{end_datetime.strftime('%Y%m%dT%H%M%S')}"

        if booking.requester_id == current_user.id:
            title = f'Dog Sitting: {requester_dog.name if requester_dog else "Your dog"} with {other_user.display_name}'
            details = f'Your dog will be cared for by {other_user.display_name}'
        else:
            title = f'Dog Sitting: Caring for {requester_dog.name if requester_dog else "dog"}'
            details = f'You are caring for {requester_dog.name if requester_dog else "a dog"} for {other_user.display_name}'

        location = other_user.location

        # Build Google Calendar URL
        from urllib.parse import urlencode, quote
        params = {
            'action': 'TEMPLATE',
            'text': title,
            'dates': dates,
            'details': details,
            'location': location
        }
        google_url = f"https://calendar.google.com/calendar/render?{urlencode(params)}"

        return redirect(google_url)

    # ============================================================
    # CLI COMMANDS
    # ============================================================

    @app.cli.command('init-db')
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Database initialized!')

    @app.cli.command('seed-db')
    def seed_db():
        """Seed the database with sample data."""
        from seed_data import clear_database, seed_database
        clear_database()
        seed_database()

    @app.cli.command('reset-db')
    def reset_db():
        """Reset and seed the database."""
        from seed_data import clear_database, seed_database
        clear_database()
        seed_database()

    return app


def get_calendar_weeks(user_id, month=None, year=None):
    """Generate calendar data for the specified month"""
    today = date.today()
    if month is None:
        month = today.month
    if year is None:
        year = today.year

    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdatescalendar(year, month)

    weeks = []
    for week in month_days:
        week_data = []
        for day in week:
            day_slots = AvailabilitySlot.query.filter_by(user_id=user_id, date=day).all()
            week_data.append({
                'date': day,
                'day': day.day,
                'is_today': day == today,
                'is_current_month': day.month == month,
                'slots': day_slots
            })
        weeks.append(week_data)
    return weeks


# Create app instance
app = create_app()

if __name__ == '__main__':
    print("\n🐾 PawPal - Dog Sitting Community Platform")
    print("=" * 50)
    print("Starting development server...")
    print("Open http://127.0.0.1:8080 in your browser")
    print("=" * 50 + "\n")
    app.run(debug=True, host='127.0.0.1', port=8080)
