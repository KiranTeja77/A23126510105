# Notification System Design

# Stage 1

## Core Actions

- Fetch all notifications for a logged-in student
- Mark notification as read
- Fetch unread notification count
- Fetch notifications by type also like Placement, Event, Result

## Endpoints

### Get All Notifications

GET /api/notifications
Headers: { "Authorization": "Bearer <token>" }

Response:
{
"notifications": [
{
"id": "uuid",
"type": "Placement" | "Event" | "Result",
"message": "string",
"isRead": false,
"timestamp": "timestamp"
}
]
}

### Get Notifications by Type

GET /api/notifications?type=Placement
Headers: { "Authorization": "Bearer <token>" }

Response:
{
"notifications": [
{
"id": "uuid",
"type": "specific type",
"message": "string",
"isRead": false,
"timestamp": "timestamp"
}
]
}

### Get Unread Count

GET /api/notifications/unread/count
Headers: { "Authorization": "Bearer <token>" }

Response:
{
"unreadCount": 5
}

### Mark as Read

PATCH /api/notifications/:id/read
Headers: { "Authorization": "Bearer <token>" }

Response:
{
"message": "Notification is marked as read"
}

### Mark All as Read

PATCH /api/notifications/read/all
Headers: { "Authorization": "Bearer <token>" }

Response:
{
"message": "All notifications are marked as read"
}

## JSON Schemas

### Notification Schema

{
"id": "string (uuid)",
"studentId": "string (uuid)",
"type": "enum: Placement | Event | Result",
"message": "string",
"isRead": "boolean",
"timestamp": "string (timezone)"
}

## Real Time Mechanism

we can twilio, websocket many more

# Stage 2

## DB Choice: PostgreSQL

Went with PostgreSQL because notifications are pretty structured data —
each one has a type, message, student it belongs to, read status and timestamp.
SQL handles this really well and makes querying easy.

## Schema

### Students Table

CREATE TABLE students (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
name VARCHAR(255) NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL,
roll_no VARCHAR(50) UNIQUE NOT NULL,
created_at TIMESTAMP DEFAULT NOW()
);

### Notifications Table

CREATE TABLE notifications (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
student_id UUID REFERENCES students(id) ON DELETE CASCADE,
type VARCHAR(50) CHECK (type IN ('Placement', 'Event', 'Result')),
message TEXT NOT NULL,
is_read BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT NOW()
);

### Indexes

CREATE INDEX idx_notifications_student_id ON notifications(student_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);

## As Data Grows

- **Indexes** — makes filtering much faster an finding data is much easier.
- **Redis** — fetching data from DB for same queries will burden the DB so redis will be the best option in this scenarios.
