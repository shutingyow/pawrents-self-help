🐾 PawPal

Product Requirements Document

  ----------------- -----------------------------------------------------
  **Version**       1.0

  **Last Updated**  December 2024

  **Author**        Sheldon

  **Status**        Draft
  ----------------- -----------------------------------------------------

1\. Executive Summary

PawPal is a community-based web platform that connects dog owners
(\"pawrents\") within a neighbourhood to help each other with
dog-sitting. The platform enables pawrents to share their availability,
request dog-sitting help from neighbours, and build a supportive
pet-care community through social features.

1.1 Problem Statement

Busy dog owners often struggle to find reliable, affordable dog-sitting
options for short-notice or irregular schedules. Professional services
are expensive, and finding trustworthy individuals through informal
channels is time-consuming and inconsistent.

1.2 Solution

PawPal creates a mutual-aid network where community members can share
dog-sitting responsibilities based on their availability. The platform
includes granular scheduling (specific time slots), a booking request
system, and a social feed for community engagement.

1.3 Goals

1.  Enable pawrents to easily publish and manage their availability at
    hourly granularity

2.  Provide a seamless booking request and confirmation workflow

3.  Foster community connections through social features and shared
    experiences

4.  Create an intuitive, mobile-friendly user experience

2\. User Personas

2.1 Primary Persona: The Busy Professional

-   **Name:** Rachel, 32

-   **Occupation:** Marketing Manager

-   **Dog:** Biscuit, 2-year-old Corgi

-   **Pain Points:** Irregular work hours, last-minute meetings,
    business travel. Feels guilty leaving Biscuit alone.

-   **Goals:** Find reliable neighbours who can watch Biscuit during
    work emergencies

2.2 Secondary Persona: The Flexible Helper

-   **Name:** David, 45

-   **Occupation:** Freelance Designer (works from home)

-   **Dog:** Max, 5-year-old Golden Retriever

-   **Motivation:** Loves dogs, flexible schedule, wants Max to have
    playmates

-   **Goals:** Help neighbours while giving Max socialization
    opportunities, build community connections

3\. Feature Specifications

The platform consists of four core modules: User Management,
Availability & Calendar, Booking System, and Community Feed.

3.1 Module: User Management

3.1.1 User Registration & Authentication

-   Email/password registration with email verification

-   Social login options (Google, Apple, Facebook)

-   Password reset functionality

-   Session management with secure token handling

3.1.2 User Profile

**Pawrent Information:**

-   Display name

-   Profile photo

-   Location / neighbourhood

-   Contact information (phone - optional)

-   Short bio / introduction

**Dog Information:**

-   Dog name

-   Breed

-   Age

-   Size (small / medium / large)

-   Dog photo(s)

-   Temperament notes (e.g., friendly, shy, energetic)

-   Special care instructions (e.g., dietary needs, medications)

3.2 Module: Availability & Calendar

The calendar module enables pawrents to manage their availability with
granular time slots, allowing other community members to view when help
is available.

3.2.1 Availability Management

**Time Slot Configuration:**

-   Users can set availability at hourly granularity (e.g., 9:00 AM -
    6:00 PM)

-   Minimum slot duration: 1 hour

-   Support for recurring availability patterns (e.g., every weekday 9
    AM - 12 PM)

-   One-time availability slots for specific dates

-   Quick-add templates: Morning (6 AM - 12 PM), Afternoon (12 PM - 6
    PM), Evening (6 PM - 10 PM), Full Day

**Slot Details:**

-   Date

-   Start time

-   End time

-   Status: Available / Booked / Blocked

-   Optional notes (e.g., \"Only small dogs\", \"Can pick up from your
    place\")

3.2.2 Calendar Views

-   **Personal Calendar:** Manage own availability, view
    incoming/outgoing bookings

-   **Browse View:** View other pawrents\' availability (read-only)

-   **Week View:** 7-day grid showing hourly slots

-   **Month View:** Overview with day-level indicators

3.2.3 Search & Discovery

-   Filter by date range

-   Filter by time slot (morning / afternoon / evening)

-   Filter by neighbourhood / location

-   Filter by dog size compatibility

3.3 Module: Booking System

The booking system facilitates requests between pawrents who need help
and those with available time slots.

3.3.1 Booking Request Flow

**Step 1: Browse & Select**

-   Requester browses available pawrents

-   Views pawrent profile and dog info

-   Selects desired time slot(s)

**Step 2: Submit Request**

-   Requester adds a message (pickup/dropoff details, special
    instructions)

-   System validates slot availability

-   Request submitted, status set to \"Pending\"

**Step 3: Provider Response**

-   Provider receives notification

-   Provider reviews request details and requester\'s profile

-   Provider accepts or declines (with optional message)

**Step 4: Confirmation**

-   If accepted: Both parties notified, slot marked as \"Booked\"

-   If declined: Requester notified, slot remains available

3.3.2 Booking Statuses

  ----------------- -----------------------------------------------------
  **Status**        **Description**

  Pending           Request submitted, awaiting provider response

  Confirmed         Provider accepted, booking is scheduled

  Declined          Provider declined the request

  Cancelled         Either party cancelled before the scheduled time

  Completed         Dog-sitting session has concluded
  ----------------- -----------------------------------------------------

3.3.3 Booking Management

-   View all bookings (as requester and as provider)

-   Filter by status, date range

-   Cancel booking (with reason)

-   In-app messaging for booking-related communication

3.4 Module: Community Feed (Chitchat)

A social module that enables community members to share updates, photos,
and engage with each other beyond transactional booking interactions.

3.4.1 Post Types

**Photo Posts:**

-   Share dog-sitting moments

-   Multiple photos per post (up to 10)

-   Caption text

-   Tag other pawrents mentioned in the post

**Text Updates:**

-   General announcements

-   Questions to the community

-   Tips and recommendations

**Event Posts:**

-   Community dog walks

-   Meet-ups at dog parks

-   Include date, time, location

-   RSVP functionality (Interested / Going)

3.4.2 Engagement Features

-   **Reactions:** Like, Love, Cute (paw icon)

-   **Comments:** Threaded comments on posts

-   **Share:** Share post link externally

3.4.3 Feed Features

-   Chronological feed (newest first)

-   Pull-to-refresh

-   Infinite scroll pagination

-   Filter by post type (Photos / Events / All)

-   Notification badge for new posts since last visit

4\. Notifications

The system will send notifications via push (mobile/web) and email based
on user preferences.

4.1 Notification Triggers

  -------------------------- --------------------------------------------
  **Event**                  **Notification**

  New booking request        \"\[Name\] has requested your help on
                             \[Date\]!\"

  Booking accepted           \"Great news! \[Name\] accepted your
                             booking.\"

  Booking declined           \"\[Name\] couldn\'t accept your request for
                             \[Date\].\"

  Booking cancelled          \"Your booking on \[Date\] has been
                             cancelled.\"

  Upcoming booking reminder  \"Reminder: Dog-sitting with \[Name\]
                             tomorrow at \[Time\]\"

  New message                \"\[Name\] sent you a message.\"

  Tagged in post             \"\[Name\] mentioned you in a post!\"

  Comment on your post       \"\[Name\] commented on your post.\"

  New community event        \"New event: \[Event Name\] on \[Date\]!\"
  -------------------------- --------------------------------------------

5\. Data Models

5.1 User

  ------------------- --------------- ------------------------------------
  **Field**           **Type**        **Description**

  id                  UUID            Primary key

  email               String          Unique, required

  display_name        String          User\'s display name

  profile_photo_url   String          URL to profile image

  location            String          Neighbourhood/area

  bio                 Text            Short bio/intro

  created_at          Timestamp       Account creation date
  ------------------- --------------- ------------------------------------

5.2 Dog

  ------------------- --------------- ------------------------------------
  **Field**           **Type**        **Description**

  id                  UUID            Primary key

  owner_id            UUID            FK to User

  name                String          Dog\'s name

  breed               String          Breed

  age                 Integer         Age in years

  size                Enum            small / medium / large

  temperament         Text            Personality notes

  care_instructions   Text            Special needs
  ------------------- --------------- ------------------------------------

5.3 AvailabilitySlot

  ------------------ --------------- ------------------------------------
  **Field**          **Type**        **Description**

  id                 UUID            Primary key

  user_id            UUID            FK to User

  date               Date            The date of availability

  start_time         Time            Start time (e.g., 09:00)

  end_time           Time            End time (e.g., 18:00)

  status             Enum            available / booked / blocked

  notes              Text            Optional notes

  is_recurring       Boolean         Part of recurring pattern

  recurrence_rule    String          iCal RRULE format
  ------------------ --------------- ------------------------------------

5.4 Booking

  ------------------ --------------- ------------------------------------
  **Field**          **Type**        **Description**

  id                 UUID            Primary key

  requester_id       UUID            FK to User (person needing help)

  provider_id        UUID            FK to User (person providing help)

  slot_id            UUID            FK to AvailabilitySlot

  status             Enum            pending / confirmed / declined /
                                     cancelled / completed

  message            Text            Message from requester

  response_message   Text            Response from provider

  created_at         Timestamp       Request timestamp
  ------------------ --------------- ------------------------------------

5.5 Post (Community Feed)

  ------------------ ----------------- ------------------------------------
  **Field**          **Type**          **Description**

  id                 UUID              Primary key

  author_id          UUID              FK to User

  type               Enum              photo / text / event

  content            Text              Caption / text content

  media_urls         Array\<String\>   Photo URLs (up to 10)

  event_date         DateTime          For event posts

  event_location     String            For event posts

  tagged_users       Array\<UUID\>     Tagged pawrent IDs

  created_at         Timestamp         Post timestamp
  ------------------ ----------------- ------------------------------------

6\. Non-Functional Requirements

6.1 Performance

1.  Page load time \< 3 seconds on 4G connection

2.  API response time \< 500ms for standard operations

3.  Support 1,000 concurrent users initially

6.2 Security

4.  HTTPS encryption for all traffic

5.  Password hashing using bcrypt

6.  JWT token-based authentication

7.  Rate limiting on API endpoints

6.3 Accessibility

8.  WCAG 2.1 AA compliance

9.  Keyboard navigation support

10. Screen reader compatible

6.4 Compatibility

11. Responsive design (mobile, tablet, desktop)

12. Browser support: Chrome, Safari, Firefox, Edge (latest 2 versions)

13. Progressive Web App (PWA) support for mobile installation

7\. Tech Stack Recommendations

  ----------------- ----------------------- -----------------------------
  **Layer**         **Technology**          **Rationale**

  Frontend          Next.js + Tailwind CSS  SSR, fast builds, great DX

  Backend           Node.js + Express or    Rapid development, JS
                    Supabase                ecosystem

  Database          PostgreSQL              Relational data, JSON support

  Auth              Supabase Auth /         Social logins, secure by
                    Firebase Auth           default

  File Storage      Supabase Storage / AWS  Photos, media uploads
                    S3                      

  Calendar UI       FullCalendar /          Rich calendar interactions
                    react-big-calendar      

  Notifications     Firebase Cloud          Push notifications
                    Messaging               

  Hosting           Vercel / Railway        Easy deployment, CI/CD
  ----------------- ----------------------- -----------------------------

8\. MVP Scope

For the initial release, the following features are prioritized:

8.1 MVP Features (Phase 1)

-   User registration and basic profile setup

-   Dog profile creation

-   Availability calendar with time slots

-   Browse pawrents and their availability

-   Booking request and accept/decline flow

-   Basic push notifications

8.2 Phase 2 Features

-   Community Feed (Chitchat module)

-   Event posts with RSVP

-   Recurring availability patterns

-   In-app messaging

8.3 Future Considerations

-   Trust/reputation system with reviews

-   Verification badges

-   Location-based matching

-   Payment integration for premium features

9\. Success Metrics

  -------------------------- ---------------------- ---------------------
  **Metric**                 **Target (3 months)**  **Target (6 months)**

  Registered users           100                    500

  Monthly active users       50                     300

  Completed bookings per     30                     200
  month                                             

  Booking acceptance rate    \> 60%                 \> 75%

  Community posts per week   20                     100
  -------------------------- ---------------------- ---------------------

Appendix: Glossary

  ------------------ ----------------------------------------------------
  **Term**           **Definition**

  Pawrent            A dog owner who is a member of the PawPal community

  Requester          A pawrent seeking dog-sitting help from the
                     community

  Provider           A pawrent offering their time to help watch another
                     pawrent\'s dog

  Availability Slot  A specific time window when a pawrent is available
                     to provide dog-sitting

  Booking            A confirmed arrangement between a requester and
                     provider for dog-sitting

  Chitchat           The community social feed module for sharing posts,
                     photos, and events
  ------------------ ----------------------------------------------------
