# 🚀 Full-Stack Setup Guide

## Overview

This guide will help you run both the Flask backend and React frontend together for a complete skin cancer detection system.

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

## 🔧 Backend Setup (Flask)

### 1. Navigate to Project Root
```bash
cd /Users/priyanshumehra/Desktop/finalProject/skin-cancer
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Ensure your `.env` file has these variables:
```env
# Roboflow API Key
ROBOFLOW_API_KEY=your-roboflow-api-key-here

# Model details
WORKSPACE=your-workspace-name
PROJECT=your-project-name
VERSION=your-version-number

# Groq API Key
GROQ_API_KEY=your-groq-api-key-here

# Server configuration
PORT=5001

# Database
DATABASE_URL=sqlite:///skin_cancer.db

# Secret Key
SECRET_KEY=your-secret-key-here
```

### 4. Start Flask Server
```bash
python app.py
```

Backend will be available at: **http://localhost:5001**

You should see:
```
✅ Model loaded from models/xgboost_ensemble.pkl
✅ XGBoost ensemble initialized
✅ XAI explainer initialized
 * Running on http://127.0.0.1:5001
```

## ⚛️ Frontend Setup (React)

### 1. Navigate to Frontend Directory
Open a **new terminal** and run:
```bash
cd /Users/priyanshumehra/Desktop/finalProject/skin-cancer/frontend
```

### 2. Install Node Dependencies
```bash
npm install
```

This will install:
- React & React DOM
- React Router
- Vite
- Tailwind CSS
- PostCSS & Autoprefixer

### 3. Start Development Server
```bash
npm run dev
```

Frontend will be available at: **http://localhost:5173**

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## 🌐 Accessing the Application

1. Open your browser to: **http://localhost:5173**
2. You'll see the **Login** page
3. Click **"Create one now"** to register a new account
4. After registration, login with your credentials
5. You'll be redirected to the **Dashboard** where you can:
   - Enter patient information
   - Upload or capture skin lesion images
   - Get AI-powered analysis
   - View medical insights

## 📡 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Analysis
- `POST /analyze` - Analyze skin lesion image
  - Requires: image file, patient info (name, age, gender, location)
  - Returns: predictions, confidence, visualizations, LLM advice

### Dashboard
- `GET /dashboard` - Main application (requires login)

## 🔄 Development Workflow

### Terminal 1 (Backend)
```bash
cd /Users/priyanshumehra/Desktop/finalProject/skin-cancer
python app.py
```

### Terminal 2 (Frontend)
```bash
cd /Users/priyanshumehra/Desktop/finalProject/skin-cancer/frontend
npm run dev
```

### Making Changes

**Backend Changes:**
- Edit Python files
- Flask auto-reloads (debug mode)
- Check Terminal 1 for errors

**Frontend Changes:**
- Edit React components in `src/`
- Vite hot-reloads automatically
- Changes appear instantly in browser

## 🐛 Troubleshooting

### Backend Issues

#### Issue: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

#### Issue: "Port 5001 already in use"
**Solution:**
- Change PORT in `.env` file
- Or kill the process: `lsof -ti:5001 | xargs kill -9`

#### Issue: "API Key is incorrect"
**Solution:**
- Check `.env` file has correct Roboflow and Groq keys
- Ensure no extra spaces around keys

#### Issue: "Database errors"
**Solution:**
```bash
rm skin_cancer.db
python app.py  # This will recreate the database
```

### Frontend Issues

#### Issue: "Cannot connect to backend"
**Solution:**
- Ensure Flask backend is running on port 5001
- Check browser console for CORS errors
- Verify backend URL in components is `http://localhost:5001`

#### Issue: "npm install fails"
**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
```

#### Issue: "Icons not showing"
**Solution:**
- Font Awesome CDN is in `index.html`
- Check browser console for network errors
- Clear browser cache

#### Issue: "Camera not working"
**Solution:**
- Use HTTPS or localhost (HTTP allowed)
- Grant camera permissions in browser
- Check browser console for errors
- Ensure camera is not in use by another app

### CORS Issues

#### Issue: "CORS policy error"
**Solution:**
Backend is configured with:
```python
CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://127.0.0.1:5173'])
```

If still having issues:
1. Clear browser cache
2. Try incognito/private browsing
3. Check Flask terminal for request logs

## 📦 Building for Production

### Frontend Build
```bash
cd frontend
npm run build
```

This creates optimized files in `frontend/dist/`

### Serving Production Build
You can serve the built files with Flask:
```python
# Add to app.py
from flask import send_from_directory

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join('frontend/dist', path)):
        return send_from_directory('frontend/dist', path)
    else:
        return send_from_directory('frontend/dist', 'index.html')
```

## 🧪 Testing the Application

### Test Login
1. Go to http://localhost:5173
2. Click "Create one now"
3. Register with:
   - Name: Test User
   - Email: test@example.com
   - Password: TestPass123!
4. Login with same credentials

### Test Image Analysis
1. After login, you're on Dashboard
2. Fill patient info:
   - Name: John Doe
   - Age: 45
   - Gender: Male
   - Location: New York
3. **Option A: Upload File**
   - Click "File Upload" tab
   - Drag-drop or click to select a skin lesion image
   - Click "Analyze Image"
4. **Option B: Camera Capture**
   - Click "Camera Capture" tab
   - Click "Start Camera"
   - Position camera over skin lesion
   - Click "Capture"
   - Click "Analyze Captured Image"
5. Wait for analysis (3-10 seconds)
6. View results:
   - Primary diagnosis
   - Confidence score
   - All predictions
   - Medical insights
   - Visualizations

## 📊 Performance Optimization

### Backend
- XGBoost ensemble model is cached
- Roboflow model is loaded once at startup
- Image processing is optimized with PIL
- SQLAlchemy uses connection pooling

### Frontend
- Vite provides fast HMR (Hot Module Replacement)
- Images are lazy-loaded
- Components use React.memo where appropriate
- Tailwind CSS is purged in production

## 🔐 Security Notes

### Current Setup (Development)
- Basic authentication with Flask-Login
- Passwords hashed with Werkzeug
- Session-based authentication
- CORS restricted to localhost origins
- File upload size limited to 16MB

### Production Recommendations
- Use HTTPS (SSL/TLS)
- Set strong SECRET_KEY
- Use environment variables (never commit)
- Implement rate limiting
- Add CSRF protection
- Use production-grade database (PostgreSQL)
- Implement input sanitization
- Add file type validation
- Set up monitoring and logging

## 📝 File Structure

```
skin-cancer/
├── app.py                    # Flask backend
├── ensemble_model.py         # XGBoost ensemble
├── explainability.py         # XAI features
├── temporal_augmentation.py  # Data augmentation
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── skin_cancer.db           # SQLite database
├── static/uploads/          # Uploaded images
├── templates/               # Flask templates (legacy)
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   └── Dashboard.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

## 🎯 Quick Start Commands

### One-Time Setup
```bash
# Backend
cd /Users/priyanshumehra/Desktop/finalProject/skin-cancer
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Daily Development
```bash
# Terminal 1: Backend
python app.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Access Application
Open: **http://localhost:5173**

## 🎉 Success Checklist

- [ ] Backend running on port 5001
- [ ] Frontend running on port 5173
- [ ] No errors in either terminal
- [ ] Can access login page at http://localhost:5173
- [ ] Can register new account
- [ ] Can login successfully
- [ ] Dashboard loads after login
- [ ] Can upload/capture images
- [ ] Analysis returns results
- [ ] Medical insights display
- [ ] Visualizations show properly

## 📚 Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **React Documentation**: https://react.dev/
- **Vite Documentation**: https://vitejs.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **Roboflow API**: https://docs.roboflow.com/
- **Groq API**: https://console.groq.com/docs

## 🆘 Getting Help

If you encounter issues:
1. Check terminal outputs for error messages
2. Check browser console (F12) for frontend errors
3. Review this troubleshooting guide
4. Check CORS configuration
5. Verify all dependencies are installed

---

**Ready to go! 🚀**

Your full-stack skin cancer detection system is now set up and ready for development and testing.

