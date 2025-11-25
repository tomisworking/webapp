# Forum API Documentation

Base URL: `http://localhost:8000/api`

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

Tokens are obtained through the login endpoint and automatically refreshed by the frontend.

---

## 🔐 Authentication Endpoints

### Register User
**POST** `/auth/register/`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword123",
  "password2": "securepassword123"
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "avatar": null,
    "bio": "",
    "thread_count": 0,
    "post_count": 0,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "User registered successfully"
}
```

**Errors:**
- `400` - Validation errors (passwords don't match, email already exists, etc.)

---

### Login
**POST** `/auth/login/`

Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors:**
- `401` - Invalid credentials

---

### Refresh Token
**POST** `/auth/refresh/`

Refresh the access token using a refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Logout
**POST** `/auth/logout/` 🔒

Blacklist the refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "message": "Logout successful"
}
```

---

### Get Current User
**GET** `/auth/user/` 🔒

Get authenticated user's profile.

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "avatar": null,
  "bio": "My bio text",
  "thread_count": 5,
  "post_count": 23,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:20:00Z"
}
```

---

### Update Profile
**PATCH** `/auth/user/` 🔒

Update current user's profile.

**Request Body:**
```json
{
  "username": "newusername",
  "bio": "Updated bio text"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "newusername",
  "avatar": null,
  "bio": "Updated bio text",
  "thread_count": 5,
  "post_count": 23,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-21T09:15:00Z"
}
```

---

### Get User by ID
**GET** `/auth/users/{id}/`

Get public user profile.

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "avatar": null,
  "bio": "My bio",
  "thread_count": 5,
  "post_count": 23,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Get User's Threads
**GET** `/auth/users/{id}/threads/` 🔒

Get all threads created by a user.

**Response:** `200 OK`
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Thread Title",
    "slug": "thread-title",
    "author": {
      "id": 1,
      "username": "username",
      "avatar": null
    },
    "category_name": "Tech Talk",
    "category_slug": "tech",
    "views_count": 45,
    "post_count": 12,
    "is_pinned": false,
    "is_locked": false,
    "created_at": "2024-01-20T10:00:00Z",
    "last_activity": "2024-01-21T15:30:00Z"
  }
]
```

---

### Get User's Posts
**GET** `/auth/users/{id}/posts/` 🔒

Get all posts created by a user.

**Response:** `200 OK`
```json
[
  {
    "id": "223e4567-e89b-12d3-a456-426614174001",
    "thread_title": "Thread Title",
    "author": {
      "id": 1,
      "username": "username",
      "avatar": null
    },
    "content": "Post content here...",
    "is_edited": false,
    "created_at": "2024-01-20T14:00:00Z",
    "updated_at": "2024-01-20T14:00:00Z"
  }
]
```

---

## 📁 Category Endpoints

### List Categories
**GET** `/categories/`

Get all forum categories.

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "General Discussion",
    "slug": "general",
    "description": "General topics and casual conversations",
    "icon": "💬",
    "order": 1,
    "thread_count": 15,
    "post_count": 87,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Get Category
**GET** `/categories/{slug}/`

Get a specific category by slug.

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Tech Talk",
  "slug": "tech",
  "description": "Discuss programming and technology",
  "icon": "💻",
  "order": 2,
  "thread_count": 25,
  "post_count": 156,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### Get Category Threads
**GET** `/categories/{slug}/threads/`

Get all threads in a category.

**Response:** `200 OK`
```json
{
  "category": {
    "id": 1,
    "name": "Tech Talk",
    "slug": "tech",
    "description": "Discuss programming and technology",
    "icon": "💻",
    "order": 2,
    "thread_count": 25,
    "post_count": 156,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "threads": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Thread Title",
      "slug": "thread-title",
      "author": {
        "id": 1,
        "username": "username",
        "avatar": null
      },
      "category_name": "Tech Talk",
      "category_slug": "tech",
      "views_count": 45,
      "post_count": 12,
      "is_pinned": false,
      "is_locked": false,
      "created_at": "2024-01-20T10:00:00Z",
      "last_activity": "2024-01-21T15:30:00Z"
    }
  ]
}
```

---

## 📝 Thread Endpoints

### List Threads
**GET** `/threads/`

Get all threads with optional filtering.

**Query Parameters:**
- `category__slug` - Filter by category slug
- `author__id` - Filter by author ID
- `search` - Search in title and content
- `ordering` - Sort by field (e.g., `-created_at`, `views_count`)
- `page` - Page number (pagination)

**Examples:**
```
/threads/?category__slug=tech
/threads/?search=django
/threads/?ordering=-views_count
```

**Response:** `200 OK` (paginated)
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/threads/?page=2",
  "previous": null,
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Thread Title",
      "slug": "thread-title",
      "author": {
        "id": 1,
        "username": "username",
        "avatar": null
      },
      "category_name": "Tech Talk",
      "category_slug": "tech",
      "views_count": 45,
      "post_count": 12,
      "is_pinned": false,
      "is_locked": false,
      "created_at": "2024-01-20T10:00:00Z",
      "last_activity": "2024-01-21T15:30:00Z"
    }
  ]
}
```

---

### Create Thread
**POST** `/threads/create/` 🔒

Create a new thread.

**Request Body:**
```json
{
  "title": "My Thread Title",
  "content": "Thread content goes here...",
  "category_id": 1
}
```

**Response:** `201 Created`
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "My Thread Title",
  "slug": "my-thread-title",
  "content": "Thread content goes here...",
  "author": {
    "id": 1,
    "username": "username",
    "avatar": null
  },
  "category": {
    "id": 1,
    "name": "Tech Talk",
    "slug": "tech",
    "description": "Discuss programming and technology",
    "icon": "💻",
    "order": 2,
    "thread_count": 26,
    "post_count": 156,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "views_count": 0,
  "post_count": 0,
  "is_pinned": false,
  "is_locked": false,
  "created_at": "2024-01-21T16:00:00Z",
  "updated_at": "2024-01-21T16:00:00Z",
  "last_activity": "2024-01-21T16:00:00Z"
}
```

**Errors:**
- `400` - Validation errors
- `401` - Not authenticated

---

### Get Thread
**GET** `/threads/{id}/`

Get thread details. Increments view counter.

**Response:** `200 OK`
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Thread Title",
  "slug": "thread-title",
  "content": "Full thread content...",
  "author": {
    "id": 1,
    "username": "username",
    "avatar": null
  },
  "category": {
    "id": 1,
    "name": "Tech Talk",
    "slug": "tech",
    "description": "Discuss programming and technology",
    "icon": "💻",
    "order": 2,
    "thread_count": 25,
    "post_count": 156,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "views_count": 46,
  "post_count": 12,
  "is_pinned": false,
  "is_locked": false,
  "created_at": "2024-01-20T10:00:00Z",
  "updated_at": "2024-01-20T10:00:00Z",
  "last_activity": "2024-01-21T15:30:00Z"
}
```

---

### Get Thread with Posts
**GET** `/threads/{id}/posts/`

Get thread details with all posts.

**Response:** `200 OK`
```json
{
  "thread": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Thread Title",
    "slug": "thread-title",
    "content": "Full thread content...",
    "author": {
      "id": 1,
      "username": "username",
      "avatar": null
    },
    "category": { /* category object */ },
    "views_count": 46,
    "post_count": 12,
    "is_pinned": false,
    "is_locked": false,
    "created_at": "2024-01-20T10:00:00Z",
    "updated_at": "2024-01-20T10:00:00Z",
    "last_activity": "2024-01-21T15:30:00Z"
  },
  "posts": [
    {
      "id": "223e4567-e89b-12d3-a456-426614174001",
      "thread_title": "Thread Title",
      "author": {
        "id": 2,
        "username": "otheruser",
        "avatar": null
      },
      "content": "Reply content...",
      "is_edited": false,
      "created_at": "2024-01-20T14:00:00Z",
      "updated_at": "2024-01-20T14:00:00Z"
    }
  ]
}
```

---

### Update Thread
**PATCH** `/threads/{id}/` 🔒

Update thread (author only).

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content..."
}
```

**Response:** `200 OK`
```json
{
  /* Updated thread object */
}
```

**Errors:**
- `403` - Not the author
- `404` - Thread not found

---

### Delete Thread
**DELETE** `/threads/{id}/` 🔒

Soft delete thread (author only).

**Response:** `204 No Content`

**Errors:**
- `403` - Not the author
- `404` - Thread not found

---

## 💬 Post Endpoints

### List Posts
**GET** `/posts/`

Get posts with filtering.

**Query Parameters:**
- `thread` - Filter by thread ID

**Response:** `200 OK` (paginated)
```json
{
  "count": 12,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "223e4567-e89b-12d3-a456-426614174001",
      "thread_title": "Thread Title",
      "author": {
        "id": 2,
        "username": "username",
        "avatar": null
      },
      "content": "Post content...",
      "is_edited": false,
      "created_at": "2024-01-20T14:00:00Z",
      "updated_at": "2024-01-20T14:00:00Z"
    }
  ]
}
```

---

### Create Post
**POST** `/posts/create/` 🔒

Create a new post (reply).

**Request Body:**
```json
{
  "thread_id": "123e4567-e89b-12d3-a456-426614174000",
  "content": "My reply content..."
}
```

**Response:** `201 Created`
```json
{
  "id": "323e4567-e89b-12d3-a456-426614174002",
  "thread_title": "Thread Title",
  "author": {
    "id": 1,
    "username": "username",
    "avatar": null
  },
  "content": "My reply content...",
  "is_edited": false,
  "created_at": "2024-01-21T16:30:00Z",
  "updated_at": "2024-01-21T16:30:00Z"
}
```

**Errors:**
- `400` - Validation errors
- `401` - Not authenticated
- `403` - Thread is locked

---

### Get Post
**GET** `/posts/{id}/`

Get post details.

**Response:** `200 OK`
```json
{
  "id": "223e4567-e89b-12d3-a456-426614174001",
  "thread_title": "Thread Title",
  "author": {
    "id": 2,
    "username": "username",
    "avatar": null
  },
  "content": "Post content...",
  "is_edited": false,
  "created_at": "2024-01-20T14:00:00Z",
  "updated_at": "2024-01-20T14:00:00Z"
}
```

---

### Update Post
**PATCH** `/posts/{id}/` 🔒

Update post (author only).

**Request Body:**
```json
{
  "content": "Updated post content..."
}
```

**Response:** `200 OK`
```json
{
  "id": "223e4567-e89b-12d3-a456-426614174001",
  "thread_title": "Thread Title",
  "author": {
    "id": 2,
    "username": "username",
    "avatar": null
  },
  "content": "Updated post content...",
  "is_edited": true,
  "created_at": "2024-01-20T14:00:00Z",
  "updated_at": "2024-01-21T17:00:00Z"
}
```

**Errors:**
- `403` - Not the author
- `404` - Post not found

---

### Delete Post
**DELETE** `/posts/{id}/` 🔒

Soft delete post (author only).

**Response:** `204 No Content`

**Errors:**
- `403` - Not the author
- `404` - Post not found

---

## 🔑 Legend

- 🔒 - Requires authentication
- All dates are in ISO 8601 format
- UUIDs are used for thread and post IDs
- Integers are used for user and category IDs

## 📊 HTTP Status Codes

- `200 OK` - Request succeeded
- `201 Created` - Resource created
- `204 No Content` - Request succeeded, no content to return
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Not authorized
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
