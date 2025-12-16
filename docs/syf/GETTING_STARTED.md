# Getting Started - Forum Application

Welcome! This guide will help you get the forum application running on your machine.

## 📋 What You'll Need

Before you begin, make sure you have these installed:
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **A code editor** - VS Code, PyCharm, etc. (optional)
- **A terminal/command prompt**

## 🎯 Choose Your Path

### Option A: Automated Setup (Recommended for Beginners)

**Windows Users:**
1. Double-click `setup-backend.bat`
2. Double-click `setup-frontend.bat`
3. Double-click `start-backend.bat`
4. Double-click `start-frontend.bat` (in a new window)
5. Visit http://localhost:3000

**Mac/Linux Users:**
```bash
# Make scripts executable
chmod +x *.sh

# Run setup
./setup-backend.sh
./setup-frontend.sh

# Start servers
./start-backend.sh
./start-frontend.sh  # In a new terminal
```

### Option B: Manual Setup (For Developers)

Follow the detailed instructions in [QUICKSTART.md](QUICKSTART.md)

## 🎮 Try It Out

Once both servers are running:

1. **Open your browser** to http://localhost:3000
2. **Register** a new account (or use test accounts below)
3. **Browse categories** on the home page
4. **Click a thread** to read discussions
5. **Create your first thread** using the "New Thread" button
6. **Reply to threads** to join conversations

### Test Accounts (if you ran seed_data)

All passwords: `password123`
- alice@example.com
- bob@example.com
- charlie@example.com

## 📚 What's Inside

### Backend (Django REST API)
- **Location:** `backend/` folder
- **Runs on:** http://localhost:8000
- **Admin panel:** http://localhost:8000/admin
- **Database:** SQLite (automatically created)

### Frontend (React App)
- **Location:** `frontend/` folder  
- **Runs on:** http://localhost:3000
- **Connects to:** Backend API

## 🗺️ Site Map

```
Home (/)
├── Categories Grid
│   └── Category Page (/category/tech)
│       └── Thread List
│           └── Thread Detail (/threads/{id})
│               ├── Original Post
│               ├── Replies
│               └── Reply Form
│
├── Login (/login)
├── Register (/register)
├── New Thread (/threads/new) - Protected
└── Profile (/profile) - Protected
    ├── My Threads
    └── My Posts
```

## 🎯 Quick Demo Script

Follow this 5-minute demo:

1. ✅ **Visit home page** - See all categories
2. ✅ **Click "Tech Talk"** - Browse tech threads
3. ✅ **Open a thread** - Read the discussion
4. ✅ **Register an account** - Quick signup
5. ✅ **Create a thread** - Post your first topic
6. ✅ **Reply to a thread** - Join the conversation
7. ✅ **Check your profile** - See your activity

## 🔧 Common Issues

### "Port already in use"

**Backend:**
```bash
# Use a different port
python manage.py runserver 8001
```

**Frontend:**
```bash
# npm will prompt you to use a different port
# Just press 'Y' when asked
```

### "Module not found" (Backend)

```bash
cd backend
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### "Cannot connect to backend" (Frontend)

1. Make sure backend is running on port 8000
2. Check http://localhost:8000/api/categories/ directly
3. Look for error messages in the backend terminal

### Database errors

```bash
cd backend
python manage.py migrate
```

## 📖 Documentation

- **README.md** - Complete project documentation
- **QUICKSTART.md** - Detailed setup guide
- **API_DOCUMENTATION.md** - API reference
- **PROJECT_SUMMARY.md** - Project overview

## 🆘 Need Help?

1. Check the error message in your terminal
2. Read the QUICKSTART.md for detailed troubleshooting
3. Make sure both Python and Node.js are installed correctly
4. Verify both backend and frontend servers are running

## 🎓 Next Steps

Once you're comfortable with the basics:

1. **Explore the admin panel** at http://localhost:8000/admin
2. **Read the API documentation** to understand endpoints
3. **Customize categories** through the admin panel
4. **Add more test data** using the seed_data command
5. **Experiment with the code** to add new features

## 💡 Tips

- Keep both terminals open (backend and frontend)
- Register your own account for testing
- Use the admin panel to manage content
- Check browser console (F12) if frontend has issues
- Check terminal output if backend has issues

## 🚀 Ready to Go!

You're all set! Start with the automated setup scripts, and you'll be up and running in minutes.

**Happy forum building! 🎉**

---

**Quick Commands:**

```bash
# Start backend
cd backend && python manage.py runserver

# Start frontend  
cd frontend && npm start

# Create admin user
cd backend && python manage.py createsuperuser

# Load sample data
cd backend && python manage.py seed_data
```
