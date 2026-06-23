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
