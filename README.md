# Forum Application - Phase L1

A complete discussion forum web application built with Django REST Framework and React.

## 🎯 Project Overview

This is a full-stack forum application with user authentication, categories, threads, and posts. Users can register, create discussion threads, and reply to existing threads. The application follows RESTful API architecture with JWT token-based authentication.

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: SQLite (development)
- **Authentication**: JWT tokens using djangorestframework-simplejwt
- **Additional**: django-cors-headers, django-filter, bleach

### Frontend
- **Framework**: React 18+ with functional components and hooks
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: Custom CSS with responsive design

## ✨ Features

### Implemented (Phase L1)
✅ User registration with email validation  
✅ Login/logout with JWT authentication  
✅ Protected routes and endpoints  
✅ Forum categories with icons and descriptions  
✅ Create discussion threads in categories  
✅ Reply to threads with posts  
✅ Public access to view threads and posts (no login required)  
✅ User profile page with threads and posts  
✅ Thread view counter  
✅ Responsive UI for desktop and mobile  
✅ Input validation and HTML sanitization  
✅ Soft delete for threads and posts  
✅ Pin and lock threads functionality  
✅ Automatic token refresh  

## 📁 Project Structure

```
forum-project/
├── backend/
│   ├── config/                 # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/                  # User authentication app
│   │   ├── models.py           # Custom User model
│   │   ├── serializers.py      # User serializers
│   │   ├── views.py            # Auth endpoints
│   │   ├── urls.py
│   │   └── admin.py
│   ├── forum/                  # Forum app
│   │   ├── models.py           # Category, Thread, Post models
│   │   ├── serializers.py      # Forum serializers
│   │   ├── views.py            # Forum endpoints
│   │   ├── urls.py
│   │   ├── permissions.py      # Custom permissions
│   │   ├── admin.py
│   │   └── management/
│   │       └── commands/
│   │           └── seed_data.py  # Test data seeder
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/         # Reusable components
    │   │   ├── Navbar.js
    │   │   ├── Loading.js
    │   │   ├── ErrorMessage.js
    │   │   └── ProtectedRoute.js
    │   ├── pages/              # Page components
    │   │   ├── Home.js
    │   │   ├── Login.js
    │   │   ├── Register.js
    │   │   ├── CategoryThreads.js
    │   │   ├── ThreadDetail.js
    │   │   ├── NewThread.js
    │   │   └── Profile.js
    │   ├── services/           # API services
    │   │   ├── api.js
    │   │   ├── auth.js
    │   │   └── forum.js
    │   ├── context/
    │   │   └── AuthContext.js  # Authentication context
    │   ├── App.js
    │   ├── index.js
    │   └── index.css
    ├── package.json
    └── .env.example
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+ and npm
- Git

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file**
   ```bash
   copy .env.example .env
   ```
   (On Mac/Linux use `cp .env.example .env`)

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

8. **Seed test data** (Optional but recommended)
   ```bash
   python manage.py seed_data
   ```
   This creates:
   - 8 test users (password: `password123`)
   - 5 categories
   - 15 threads
   - 50+ posts

9. **Run development server**
   ```bash
   python manage.py runserver
   ```
   Backend will be available at `http://localhost:8000`
   Admin panel at `http://localhost:8000/admin`

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal)
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   ```bash
   copy .env.example .env
   ```
   (On Mac/Linux use `cp .env.example .env`)

4. **Run development server**
   ```bash
   npm start
   ```
   Frontend will be available at `http://localhost:3000`

## 📚 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login user | No |
| POST | `/api/auth/refresh/` | Refresh access token | No |
| POST | `/api/auth/logout/` | Logout user | Yes |
| GET | `/api/auth/user/` | Get current user | Yes |
| PATCH | `/api/auth/user/` | Update user profile | Yes |
| GET | `/api/auth/users/{id}/` | Get user by ID | No |
| GET | `/api/auth/users/{id}/threads/` | Get user's threads | Yes |
| GET | `/api/auth/users/{id}/posts/` | Get user's posts | Yes |

### Category Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | List all categories | No |
| GET | `/api/categories/{slug}/` | Get category by slug | No |
| GET | `/api/categories/{slug}/threads/` | Get category threads | No |

### Thread Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/threads/` | List threads (with filters) | No |
| POST | `/api/threads/create/` | Create new thread | Yes |
| GET | `/api/threads/{id}/` | Get thread details | No |
| PATCH | `/api/threads/{id}/` | Update thread | Yes (author) |
| DELETE | `/api/threads/{id}/` | Delete thread | Yes (author) |
| GET | `/api/threads/{id}/posts/` | Get thread with posts | No |

### Post Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/posts/` | List posts | No |
| POST | `/api/posts/create/` | Create new post | Yes |
| GET | `/api/posts/{id}/` | Get post details | No |
| PATCH | `/api/posts/{id}/` | Update post | Yes (author) |
| DELETE | `/api/posts/{id}/` | Delete post | Yes (author) |

## 🧪 Test Credentials

After running `seed_data` command, you can use these test accounts:

| Email | Username | Password |
|-------|----------|----------|
| alice@example.com | alice | password123 |
| bob@example.com | bob | password123 |
| charlie@example.com | charlie | password123 |
| diana@example.com | diana | password123 |
| eve@example.com | eve | password123 |

## 🎨 Frontend Pages

- **Home** (`/`) - Categories list
- **Login** (`/login`) - User login form
- **Register** (`/register`) - User registration form
- **Category Threads** (`/category/{slug}`) - Threads in a category
- **Thread Detail** (`/threads/{id}`) - Thread with all posts
- **New Thread** (`/threads/new`) - Create thread form (protected)
- **Profile** (`/profile`) - User profile with threads/posts (protected)

## 🔒 Security Features

- Password hashing using Django's default PBKDF2
- JWT token authentication with auto-refresh
- CORS configuration for frontend domain
- Input validation on all forms
- HTML sanitization to prevent XSS attacks
- SQL injection prevention via Django ORM
- Protected routes requiring authentication
- Author-only permissions for edit/delete

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (below 768px)

## 🐛 Debugging

### Backend Issues

1. **Check if server is running**
   ```bash
   python manage.py runserver
   ```

2. **View logs in terminal** - Django shows all requests and errors

3. **Check database**
   ```bash
   python manage.py dbshell
   ```

4. **Run tests** (if implemented)
   ```bash
   python manage.py test
   ```

### Frontend Issues

1. **Clear browser cache** - Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

2. **Check console** - Open browser DevTools (F12) for errors

3. **Verify API connection** - Check Network tab in DevTools

4. **Clear localStorage**
   ```javascript
   localStorage.clear()
   ```

## 📝 Environment Variables

### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

## 🚧 Known Limitations (Phase L1)

- No search functionality yet
- No post upvote/downvote system
- No user avatars (shows initials)
- No rich text editor (plain text only)
- No email notifications
- No user reputation system
- SQLite database (not production-ready)

## 🔄 Future Enhancements (Phase L2+)

- Full-text search across threads and posts
- Rich text editor (Markdown or WYSIWYG)
- User reputation and badges
- Post voting system
- Email notifications
- User avatar uploads
- Thread bookmarking
- Advanced filtering and sorting
- Real-time updates with WebSockets
- PostgreSQL for production
- Docker containerization
- CI/CD pipeline

## 📞 Support

If you encounter issues:
1. Check the console/terminal for error messages
2. Verify all dependencies are installed
3. Ensure both backend and frontend servers are running
4. Check that ports 8000 and 3000 are available

## 📄 License

This is a learning project for educational purposes.

---

**Built with ❤️ using Django and React**
