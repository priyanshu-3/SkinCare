# 🎨 Frontend-Only Deployment to Vercel

## Overview

This guide will help you deploy **only the React frontend** to Vercel while keeping the Flask backend running locally. This is perfect for:
- ✅ Testing and development
- ✅ Showcasing the UI
- ✅ Avoiding ML model deployment issues
- ✅ Quick deployments

## 🚀 Quick Deployment Steps

### Step 1: Go to Vercel

Visit: **https://vercel.com/new**

### Step 2: Import Repository

1. Click **"Import Git Repository"**
2. Select **GitHub**
3. Choose **`priyanshu-3/SkinCare`**
4. Click **"Import"**

### Step 3: Configure Project

**IMPORTANT**: Set the root directory to `frontend`

```
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

### Step 4: Add Environment Variable

Click **"Environment Variables"** and add:

```
Name: VITE_API_URL
Value: http://localhost:5001
```

> **Note**: This will point to your local backend. Later, you can change this to a deployed backend URL.

### Step 5: Deploy!

Click **"Deploy"** and wait 1-2 minutes.

## ✅ Your Frontend is Live!

Your frontend will be available at:
```
https://your-project-name.vercel.app
```

## 🔧 Running Backend Locally

To make the deployed frontend work, you need to run the backend locally:

### Step 1: Start Backend

```bash
cd /Users/priyanshumehra/SkinCancerProject/skin-cancer
source venv/bin/activate  # or: venv\Scripts\activate on Windows
python app.py
```

Backend will run on: `http://localhost:5001`

### Step 2: Update CORS Settings

Make sure your `app.py` has CORS enabled for your Vercel domain:

```python
from flask_cors import CORS

# Update CORS to allow your Vercel domain
CORS(app, origins=[
    'http://localhost:3000',
    'https://your-project-name.vercel.app',  # Add your Vercel URL
    'https://*.vercel.app'  # Allow all Vercel preview deployments
], supports_credentials=True)
```

### Step 3: Test the Application

1. Open your Vercel URL: `https://your-project-name.vercel.app`
2. Make sure backend is running locally
3. Try logging in or registering
4. Upload an image for analysis

## 🌐 Making It Work from Anywhere

### Problem
The deployed frontend on Vercel can't reach `localhost:5001` because localhost only works on your computer.

### Solutions

#### Option A: Use ngrok (Quick Testing)

Expose your local backend to the internet:

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com

# Start ngrok
ngrok http 5001
```

You'll get a public URL like: `https://abc123.ngrok.io`

Update Vercel environment variable:
```
VITE_API_URL=https://abc123.ngrok.io
```

Redeploy frontend on Vercel.

#### Option B: Deploy Backend to Railway (Recommended)

Deploy your backend to Railway for a permanent solution:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize and deploy
cd /Users/priyanshumehra/SkinCancerProject/skin-cancer
railway init
railway up

# Get your Railway URL
railway domain
```

Update Vercel environment variable:
```
VITE_API_URL=https://your-app.railway.app
```

Redeploy frontend on Vercel.

#### Option C: Deploy Backend to Render

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Configure:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```
5. Add environment variables
6. Deploy!

Update Vercel environment variable:
```
VITE_API_URL=https://your-app.onrender.com
```

## 📝 Update CORS in Backend

Whichever option you choose, update your `app.py`:

```python
from flask_cors import CORS

# Get allowed origins from environment or use defaults
allowed_origins = os.getenv('CORS_ORIGINS', '').split(',') or [
    'http://localhost:3000',
    'https://your-vercel-app.vercel.app',
    'https://*.vercel.app'
]

CORS(app, 
     origins=allowed_origins,
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
```

## 🔄 Continuous Deployment

Every time you push to GitHub:
- ✅ Vercel automatically redeploys your frontend
- ✅ Changes go live in 1-2 minutes
- ✅ You get a preview URL for each branch

## 🎯 Testing Checklist

After deployment, test these features:

### Frontend Only (Should Work)
- [ ] Login page loads and looks good
- [ ] Register page loads and looks good
- [ ] Dashboard UI displays correctly
- [ ] History page displays correctly
- [ ] Settings page displays correctly
- [ ] Navigation works
- [ ] Responsive design works on mobile

### With Backend (Requires local backend or deployed backend)
- [ ] User registration works
- [ ] User login works
- [ ] Image upload works
- [ ] Camera capture works
- [ ] Analysis completes
- [ ] PDF download works
- [ ] History displays data
- [ ] Export CSV works

## 🐛 Troubleshooting

### Issue: "Failed to fetch" or CORS errors

**Solution:**
1. Make sure backend is running
2. Check CORS settings in `app.py`
3. Verify `VITE_API_URL` in Vercel
4. Check browser console for exact error

### Issue: API calls go to wrong URL

**Solution:**
1. Check environment variable in Vercel dashboard
2. Make sure it's `VITE_API_URL` (with VITE_ prefix)
3. Redeploy after changing environment variables

### Issue: Backend not accessible

**Solution:**
1. If using localhost: Backend must be running on your computer
2. If using ngrok: Make sure ngrok is running
3. If using Railway/Render: Check if backend is deployed and running

### Issue: Changes not showing

**Solution:**
1. Clear browser cache
2. Hard refresh (Cmd+Shift+R or Ctrl+Shift+R)
3. Check Vercel deployment logs
4. Verify build completed successfully

## 📊 Deployment Status

### What's Deployed
- ✅ React Frontend (Vercel)
- ✅ All UI components
- ✅ Routing
- ✅ Styling (Tailwind CSS)

### What's NOT Deployed
- ❌ Flask Backend (runs locally)
- ❌ ML Models
- ❌ Database
- ❌ File uploads

## 🎉 Next Steps

### For Development
Keep using this setup! It's perfect for:
- Quick UI iterations
- Testing frontend changes
- Showing off the design
- Frontend development

### For Production
When ready, deploy the backend:

1. **Railway** (Recommended)
   - Full ML support
   - $5/month
   - Easy setup
   - See: `DEPLOYMENT_OPTIONS.md`

2. **Render**
   - Free tier available
   - Good for smaller apps
   - See: `DEPLOYMENT_OPTIONS.md`

3. **AWS/DigitalOcean**
   - Full control
   - More complex
   - See: `DEPLOYMENT_OPTIONS.md`

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Vite Docs**: https://vitejs.dev/guide/
- **CORS Issues**: Check Flask-CORS documentation

## 🔗 Useful Links

- **Vercel Dashboard**: https://vercel.com/dashboard
- **GitHub Repo**: https://github.com/priyanshu-3/SkinCare
- **ngrok**: https://ngrok.com
- **Railway**: https://railway.app
- **Render**: https://render.com

---

## 📋 Quick Reference

### Start Local Backend
```bash
cd /Users/priyanshumehra/SkinCancerProject/skin-cancer
source venv/bin/activate
python app.py
```

### Deploy Frontend
```bash
# Just push to GitHub
git add .
git commit -m "Update frontend"
git push origin main

# Vercel auto-deploys!
```

### Update Environment Variable
1. Go to Vercel Dashboard
2. Select your project
3. Settings → Environment Variables
4. Edit `VITE_API_URL`
5. Redeploy

---

**Happy Deploying! 🚀**

