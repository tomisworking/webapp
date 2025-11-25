# Quick Start Guide

This guide will get you up and running in 5 minutes!

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ Node.js 16 or higher installed
- ✅ Git installed (optional)

## 🚀 Quick Setup

### Step 1: Backend Setup (Terminal 1)

```bash
# Navigate to backend folder
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin user (follow prompts)
python manage.py createsuperuser

# Load sample data (optional but recommended)
python manage.py seed_data

# Start backend server
python manage.py runserver
```

✅ Backend should now be running at **http://localhost:8000**

### Step 2: Frontend Setup (Terminal 2 - New Window)

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start frontend server
npm start
```

✅ Frontend should now be running at **http://localhost:3000**

Browser should automatically open. If not, visit http://localhost:3000

## 🎯 First Steps

1. **Register a new account** or use test accounts:
   - Email: `alice@example.com` / Password: `password123`
   - Email: `bob@example.com` / Password: `password123`

2. **Browse categories** on the home page

3. **Click on a category** to see threads

4. **Click on a thread** to read and reply

5. **Create your own thread** using the "New Thread" button

## 🔧 Troubleshooting

### "Port already in use" error

**Backend (port 8000):**
```bash
python manage.py runserver 8001
```

**Frontend (port 3000):**
```bash
npm start
# When prompted, press 'Y' to run on different port
```

### "Module not found" error

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
npm install
```

### Database errors

```bash
cd backend
python manage.py migrate
```

### Cannot connect to backend

1. Check backend is running (Terminal 1)
2. Visit http://localhost:8000/api/categories/ directly
3. Check for error messages in terminal

## 📱 Demo Flow

Follow this flow for a 5-minute demo:

1. ✅ **Home Page** - View all categories
2. ✅ **Click "Tech Talk"** - See threads in category
3. ✅ **Click "Best Python web framework"** - Read thread and replies
4. ✅ **Register** - Create a new account
5. ✅ **Create Thread** - Post your first thread
6. ✅ **Reply to Thread** - Add a reply to existing thread
7. ✅ **Profile** - View your threads and posts

## 🎓 Next Steps

- Explore the **Admin Panel** at http://localhost:8000/admin
- Read the full **README.md** for detailed documentation
- Check **API Endpoints** in README.md
- Customize categories and test data

## ⚡ Quick Commands Reference

### Backend Commands
```bash
# Start server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load test data
python manage.py seed_data

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

### Frontend Commands
```bash
# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## 🆘 Need Help?

- Check console for error messages
- Review README.md for detailed setup
- Ensure both servers are running
- Verify Python and Node versions

---

**Happy Forum Building! 🎉**
