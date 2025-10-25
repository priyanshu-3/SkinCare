# 🚀 Vercel Deployment Guide

## Overview

This guide will help you deploy the SkinCare AI application to Vercel. The application consists of:
- **Backend**: Flask (Python) API
- **Frontend**: React (Vite)

## ⚠️ Important Note

**Vercel has limitations for Python applications:**
- Serverless functions have a 10-second execution timeout
- File uploads are limited to 4.5MB
- Database writes may not persist (use external database)
- ML models may be too large for serverless

### Recommended Alternative: Split Deployment

For production, consider:
1. **Frontend on Vercel** (React app)
2. **Backend on Railway/Render/Heroku** (Flask API with ML models)

## 📋 Prerequisites

1. GitHub account with repository pushed
2. Vercel account (sign up at https://vercel.com)
3. API keys ready (Roboflow, Groq)

## 🎯 Option 1: Full Deployment (Experimental)

### Step 1: Prepare Repository

Files already created:
- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `frontend/package.json` - Updated with vercel-build script

### Step 2: Deploy to Vercel

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Click "Add New" → "Project"

2. **Import Repository**
   - Select "Import Git Repository"
   - Choose your GitHub account
   - Select `SkinCare` repository
   - Click "Import"

3. **Configure Project**
   ```
   Framework Preset: Other
   Root Directory: ./
   Build Command: cd frontend && npm run build
   Output Directory: frontend/dist
   Install Command: npm install
   ```

4. **Add Environment Variables**
   Click "Environment Variables" and add:
   ```
   ROBOFLOW_API_KEY=your_roboflow_key
   GROQ_API_KEY=your_groq_key
   SECRET_KEY=your_secret_key_here
   WORKSPACE=your_workspace
   PROJECT=your_project
   VERSION=1
   PORT=5001
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at `https://your-project.vercel.app`

### Step 3: Configure API Routes

After deployment, update frontend API calls:

In your frontend code, change:
```javascript
// From
const response = await fetch('http://localhost:5001/api/...')

// To
const response = await fetch('/api/...')
```

## 🎯 Option 2: Frontend Only (Recommended)

Deploy only the React frontend to Vercel and keep backend elsewhere.

### Step 1: Deploy Frontend

1. **Create `vercel.json` in frontend folder**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend-url.com/api/:path*"
    }
  ]
}
```

2. **Deploy**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

### Step 2: Deploy Backend Separately

**Recommended Platforms:**

#### Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

#### Render
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

## 📝 Configuration Files

### vercel.json (Root)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "frontend/dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "app.py"
    },
    {
      "src": "/analyze",
      "dest": "app.py"
    },
    {
      "src": "/static/(.*)",
      "dest": "app.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/dist/$1"
    }
  ]
}
```

### requirements.txt
Already created with all necessary Python packages.

### Frontend Environment Variables

Create `.env.production` in frontend:
```env
VITE_API_URL=https://your-backend-url.com
```

Update API calls:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'
```

## 🔧 Troubleshooting

### Issue: Build Fails

**Solution:**
1. Check build logs in Vercel dashboard
2. Ensure all dependencies are in `package.json`
3. Verify Node version compatibility

### Issue: API Routes Don't Work

**Solution:**
1. Check `vercel.json` routes configuration
2. Ensure backend is deployed and accessible
3. Update CORS settings in Flask:
```python
CORS(app, origins=['https://your-vercel-app.vercel.app'])
```

### Issue: Environment Variables Not Working

**Solution:**
1. Add variables in Vercel dashboard
2. Redeploy after adding variables
3. Check variable names match exactly

### Issue: ML Model Too Large

**Solution:**
1. Deploy backend to Railway/Render (no size limits)
2. Use external model hosting (AWS S3, Roboflow)
3. Optimize model size

### Issue: Database Not Persisting

**Solution:**
1. Use external database (PostgreSQL, MongoDB Atlas)
2. Update connection string in environment variables
3. Change SQLite to PostgreSQL:
```python
# Install psycopg2
# Update DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
```

## 🌐 Custom Domain

### Add Custom Domain

1. Go to Vercel Dashboard → Your Project
2. Click "Settings" → "Domains"
3. Add your domain
4. Update DNS records as instructed
5. Wait for DNS propagation (up to 48 hours)

### Configure DNS

Add these records to your domain:
```
Type: A
Name: @
Value: 76.76.21.21

Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

## 📊 Monitoring

### Vercel Analytics

1. Go to Project Settings
2. Enable "Analytics"
3. View real-time metrics in dashboard

### Error Tracking

Add Sentry or similar:
```bash
npm install @sentry/react
```

```javascript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "your-sentry-dsn",
  environment: "production"
});
```

## 🔒 Security

### Environment Variables

Never commit:
- API keys
- Secret keys
- Database URLs
- Passwords

### CORS Configuration

Update Flask CORS:
```python
CORS(app, origins=[
    'https://your-app.vercel.app',
    'http://localhost:3000'  # For development
])
```

### Rate Limiting

Add rate limiting to API:
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

## 📈 Performance Optimization

### Frontend

1. **Code Splitting**
```javascript
const Dashboard = lazy(() => import('./pages/Dashboard'))
```

2. **Image Optimization**
```javascript
import { Image } from 'next/image'
```

3. **Caching**
```javascript
// Add cache headers
res.setHeader('Cache-Control', 'public, max-age=31536000')
```

### Backend

1. **Use CDN for static files**
2. **Enable gzip compression**
3. **Optimize database queries**
4. **Use caching (Redis)**

## 🚀 Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Vercel account
- [ ] Import repository to Vercel
- [ ] Add environment variables
- [ ] Configure build settings
- [ ] Deploy and test
- [ ] Update API URLs in frontend
- [ ] Test all features
- [ ] Configure custom domain (optional)
- [ ] Enable analytics
- [ ] Set up error tracking
- [ ] Monitor performance

## 📞 Support

### Vercel Support
- Documentation: https://vercel.com/docs
- Community: https://github.com/vercel/vercel/discussions
- Support: support@vercel.com

### Common Commands

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls
```

## 🎉 Success!

Once deployed, your app will be available at:
- **Production**: `https://your-project.vercel.app`
- **Preview**: `https://your-project-git-branch.vercel.app`

## 📝 Post-Deployment

1. **Test all features**
   - User registration/login
   - Image upload
   - Camera capture
   - Analysis functionality
   - PDF generation
   - History viewing

2. **Monitor performance**
   - Check Vercel analytics
   - Monitor error rates
   - Check API response times

3. **Update documentation**
   - Add deployment URL to README
   - Update API endpoints
   - Document any issues

## 🔄 Continuous Deployment

Vercel automatically deploys when you push to GitHub:
- **Main branch** → Production
- **Other branches** → Preview deployments

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Vercel automatically deploys!
```

---

**Note**: For production use with ML models and large file uploads, consider using Railway, Render, or AWS for the backend while keeping the frontend on Vercel.

**Last Updated**: October 2025

