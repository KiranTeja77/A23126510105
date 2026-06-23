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

# Stage 3

## Original Query

SELECT \* FROM notification
WHERE studentID = 1042 AND isRead = False
ORDER BY createdAt DESC;

## Is it Accurate?

i wont say its accurate but its okay but it has some issues like :

- `SELECT *` fetches all columns but we only need what the frontend actually displays
- No LIMIT — if the data reaches a million rows then the DB will have a burden
- No indexes — full table scan every time which is time taking

## Why is it Slow?

At 50,000 students and 5,000,000 notifications:

- Full table scan on 5M rows to find studentID = 1042
- Then filter isRead = False on top of that
- Then sort everything by createdAt
- No limit it fetches a large amount of data at once

## Fixed Query

SELECT id, type, message, created_at FROM notifications
WHERE student_id = 1042 AND is_read = FALSE
ORDER BY created_at DESC
LIMIT 20;

## What Changed and Why

- `SELECT *` → only fetch columns we need
- Added `LIMIT 20` so it never fetch all at once

## Indexes to Add

CREATE INDEX student_unread_index
ON notifications(student_id, is_read, created_at DESC);

this make the query to fetch the row index rather than the whole data itself

## Result

With indexing and limitization the query will be more accurate even if its a large data

# Stage 4:

## The Problem

Every time a student opens the app, it hits the DB to fetch notifications.
With 50,000 students doing this at the same time — especially during
placement season — the DB gets hammered and slows down for everyone.

## Solution: Caching with Redis

Instead of hitting the DB every single time, we cache the notifications
in Redis after the first fetch. Next time the same student opens the app,
we serve from cache — DB doesn't get touched at all.

### How it works:

1. Student opens app → check Redis first
2. If cache hit → return cached notifications instantly
3. If cache miss → fetch from DB → store in Redis → return to student

## Implementation Idea

1. Student requests their notifications
2. Check Redis for key `notifications:student:{student_id}`
3. If found in cache → return immediately, skip DB
4. If not found:
   - Query DB with LIMIT 20
   - "SELECT id, type, message, is_read, created_at
     FROM notifications
     WHERE student_id = %s AND is_read = FALSE
     ORDER BY created_at DESC LIMIT 20"
   - Return result to student
5. When new notification arrives for a student:
   - Invalidate their cache key in Redis
   - Next request will fetch fresh from DB and re-cache

## Tradeoffs

### Pros:

- DB load drops massively — most requests served from cache
- Response time goes from ~200ms to ~5ms
- Scales easily during peak times like placement season

### Cons:

- Slight staleness — student might not see a notification for up to 5 mins
- Extra infrastructure — need to run and maintain Redis
- Cache invalidation logic adds complexity

## Is it worth it?

Yes. The staleness tradeoff is acceptable for notifications —
a student not seeing a notification for 5 minutes is fine.
The DB relief is massive especially during peak load.
