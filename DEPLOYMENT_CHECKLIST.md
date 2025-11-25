# Deployment Checklist

Use this checklist to verify the forum application is ready for deployment or demonstration.

## 🔍 Pre-Deployment Verification

### Backend Checklist

#### Environment Setup
- [ ] Python 3.8+ installed and accessible
- [ ] Virtual environment created (`venv/` folder exists)
- [ ] All dependencies installed from `requirements.txt`
- [ ] `.env` file created (copy from `.env.example`)
- [ ] Database migrations completed successfully
- [ ] Superuser account created for admin access

#### Database Verification
- [ ] `db.sqlite3` file exists in backend folder
- [ ] Users table has data (test users exist)
- [ ] Categories table populated (5 categories)
- [ ] Threads table has sample data
- [ ] Posts table has sample replies
- [ ] No migration warnings or errors

#### Admin Panel Test
- [ ] Admin panel accessible at http://localhost:8000/admin
- [ ] Can login with superuser credentials
- [ ] Can view users list
- [ ] Can view categories
- [ ] Can view threads
- [ ] Can view posts
- [ ] Can edit/delete content through admin

#### API Endpoints Test
- [ ] Categories list: GET `/api/categories/` returns 200
- [ ] Category detail: GET `/api/categories/tech/` returns 200
- [ ] Threads list: GET `/api/threads/` returns 200
- [ ] Register works: POST `/api/auth/register/` accepts new user
- [ ] Login works: POST `/api/auth/login/` returns JWT tokens
- [ ] Protected endpoint requires auth (test with `/api/auth/user/`)

### Frontend Checklist

#### Environment Setup
- [ ] Node.js 16+ installed and accessible
- [ ] `node_modules/` folder exists
- [ ] All dependencies installed from `package.json`
- [ ] `.env` file created if needed
- [ ] Build completes without errors (`npm start` works)

#### Page Accessibility
- [ ] Home page loads (/)
- [ ] Login page loads (/login)
- [ ] Register page loads (/register)
- [ ] Category page loads (/category/tech)
- [ ] Thread detail page loads (click any thread)
- [ ] New thread page loads (/threads/new) - requires auth
- [ ] Profile page loads (/profile) - requires auth

#### Navigation Test
- [ ] Navbar visible on all pages
- [ ] Logo links to home page
- [ ] Login/Register buttons visible when logged out
- [ ] User menu visible when logged in
- [ ] All navigation links work
- [ ] Browser back/forward buttons work

#### Responsive Design Test
- [ ] Desktop view (1200px+) looks good
- [ ] Tablet view (768px) looks good
- [ ] Mobile view (375px) looks good
- [ ] Navigation collapses on mobile
- [ ] All buttons are clickable on mobile
- [ ] Text is readable on all screen sizes

## ✅ Functional Testing

### Authentication Flow
- [ ] Can register new account
- [ ] Registration validates email format
- [ ] Registration requires password match
- [ ] Registration shows success message
- [ ] Automatically logs in after registration
- [ ] Can login with registered credentials
- [ ] Login shows error with wrong password
- [ ] Can logout successfully
- [ ] Logout redirects to login page
- [ ] Protected routes redirect to login when logged out
- [ ] Token refresh works automatically

### Category Features
- [ ] Home page shows all categories
- [ ] Each category shows thread count
- [ ] Each category shows post count
- [ ] Clicking category navigates to threads
- [ ] Category icons display correctly
- [ ] Category descriptions visible

### Thread Features
- [ ] Can view list of threads in category
- [ ] Thread list shows author name
- [ ] Thread list shows view count
- [ ] Thread list shows reply count
- [ ] Thread list shows creation date
- [ ] Can create new thread (when logged in)
- [ ] Thread creation requires title
- [ ] Thread creation requires content
- [ ] Thread creation requires category selection
- [ ] New thread appears in list immediately
- [ ] Can view thread details
- [ ] View counter increments when viewing thread
- [ ] Pinned threads appear at top
- [ ] Locked threads show lock icon
- [ ] Can edit own thread
- [ ] Can delete own thread
- [ ] Cannot edit other users' threads

### Post (Reply) Features
- [ ] Can view all posts in a thread
- [ ] Posts show author name
- [ ] Posts show creation date
- [ ] Can reply to thread (when logged in)
- [ ] Reply form validates content required
- [ ] New reply appears immediately
- [ ] Cannot reply to locked thread
- [ ] Reply form not shown when logged out
- [ ] Can edit own posts
- [ ] Edited posts show "edited" indicator
- [ ] Can delete own posts
- [ ] Cannot edit other users' posts

### User Profile
- [ ] Profile page shows username
- [ ] Profile page shows email
- [ ] Profile page shows bio (if set)
- [ ] Profile shows thread count
- [ ] Profile shows post count
- [ ] Profile shows user's threads list
- [ ] Profile shows user's posts list
- [ ] Can switch between threads/posts tabs
- [ ] Clicking thread from profile navigates correctly
- [ ] Clicking post navigates to source thread

## 🔒 Security Verification

### Authentication Security
- [ ] Passwords are hashed (not stored plain text)
- [ ] JWT tokens expire after 1 hour
- [ ] Refresh tokens work correctly
- [ ] Tokens are invalidated on logout
- [ ] Cannot access protected endpoints without token
- [ ] Cannot perform actions as another user

### Input Validation
- [ ] Email validation on registration
- [ ] Password length requirements enforced
- [ ] HTML in posts is sanitized
- [ ] XSS attempts are blocked
- [ ] Empty form submissions are rejected
- [ ] SQL injection attempts fail safely

### Authorization
- [ ] Only authors can edit their threads
- [ ] Only authors can delete their threads
- [ ] Only authors can edit their posts
- [ ] Only authors can delete their posts
- [ ] Admin can edit/delete all content (via admin panel)

## 🐛 Error Handling

### Frontend Errors
- [ ] Shows loading spinner during API calls
- [ ] Shows error message on failed API call
- [ ] Shows error on network failure
- [ ] Shows error on 404 (not found)
- [ ] Shows error on 403 (forbidden)
- [ ] Shows error on 500 (server error)
- [ ] Form validation errors display clearly
- [ ] Error messages are user-friendly

### Backend Errors
- [ ] Returns proper HTTP status codes
- [ ] Returns JSON error messages
- [ ] Logs errors to console
- [ ] Handles missing required fields
- [ ] Handles invalid data types
- [ ] Handles database errors gracefully

## 📱 Cross-Browser Testing

### Desktop Browsers
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest) - Mac only
- [ ] Edge (latest)

### Mobile Browsers
- [ ] Mobile Chrome
- [ ] Mobile Safari (iOS)
- [ ] Mobile Firefox

## ⚡ Performance Checks

### Load Times
- [ ] Home page loads under 2 seconds
- [ ] Thread list loads under 2 seconds
- [ ] Thread detail loads under 2 seconds
- [ ] No visible lag when navigating
- [ ] Images/icons load quickly

### Database
- [ ] Queries are optimized (no N+1 queries)
- [ ] Pagination works on long lists
- [ ] Large threads load efficiently

## 📊 Data Integrity

### Sample Data Verification
- [ ] All 5 categories exist
- [ ] At least 10 threads exist
- [ ] At least 30 posts exist
- [ ] All threads have a category
- [ ] All posts belong to a thread
- [ ] All content has an author
- [ ] Relationships are correct (no orphaned data)

## 🚀 Deployment Readiness

### Documentation
- [ ] README.md is complete and accurate
- [ ] QUICKSTART.md has correct setup steps
- [ ] API_DOCUMENTATION.md lists all endpoints
- [ ] All documentation files present
- [ ] Setup scripts work correctly

### Configuration
- [ ] `.env.example` files provided
- [ ] `.gitignore` excludes sensitive files
- [ ] Requirements files are up to date
- [ ] CORS settings configured correctly
- [ ] Secret keys are not hardcoded

### Code Quality
- [ ] No console.log() statements in production code
- [ ] No commented-out code blocks
- [ ] Consistent code formatting
- [ ] Meaningful variable names
- [ ] Functions have clear purposes
- [ ] No unused imports

## 📝 Final Checks

### Pre-Demo
- [ ] Fresh database with seed data
- [ ] Backend server running without errors
- [ ] Frontend server running without errors
- [ ] Test accounts available (alice, bob, charlie)
- [ ] Admin account accessible
- [ ] Browser cache cleared
- [ ] Both servers accessible on network (if demoing remotely)

### Demo Preparation
- [ ] Prepared talking points
- [ ] Test account credentials written down
- [ ] Know which features to showcase
- [ ] Have backup plan if demo fails
- [ ] Screenshots ready (optional)

## ✅ Sign-Off

Once all items are checked:

**Tested by:** _________________

**Date:** _________________

**Backend Status:** ☐ Ready ☐ Issues Found

**Frontend Status:** ☐ Ready ☐ Issues Found

**Overall Status:** ☐ READY FOR DEPLOYMENT ☐ NEEDS FIXES

**Notes:**
```
[Write any issues, concerns, or special notes here]
```

---

## 🔧 Common Issues & Solutions

### Issue: Port already in use
**Solution:** Change port or kill existing process

### Issue: Database locked
**Solution:** Close all connections, restart servers

### Issue: CORS errors
**Solution:** Verify CORS_ALLOWED_ORIGINS in settings.py

### Issue: 404 on API calls
**Solution:** Check backend is running, verify API_URL in frontend

### Issue: Token expired
**Solution:** Clear localStorage, login again

### Issue: Can't create thread/post
**Solution:** Verify user is logged in, check for error messages

---

**Remember:** All checkboxes should be ✅ before considering the application deployment-ready!
