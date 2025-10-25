# 🚀 Vercel Quick Start Guide

## ⚡ Deploy in 5 Minutes!

### Step 1: Go to Vercel
Visit: **https://vercel.com/new**

### Step 2: Import Repository
1. Click **"Import Git Repository"**
2. Select **GitHub**
3. Choose **`priyanshu-3/SkinCare`**
4. Click **"Import"**

### Step 3: Configure Project

**Framework Preset**: `Other`

**Build Settings**:
```
Root Directory: ./
Build Command: cd frontend && npm run build
Output Directory: frontend/dist
Install Command: npm install
```

### Step 4: Add Environment Variables

Click **"Environment Variables"** and add these:

```
ROBOFLOW_API_KEY = your_roboflow_api_key
GROQ_API_KEY = your_groq_api_key
SECRET_KEY = your_secret_key_here
WORKSPACE = your_workspace
PROJECT = your_project
VERSION = 1
PORT = 5001
```

### Step 5: Deploy!

Click **"Deploy"** button and wait 2-3 minutes.

## ✅ Your App is Live!

Your app will be available at:
```
https://your-project-name.vercel.app
```

## ⚠️ Important Notes

### Limitations on Vercel:
- ❌ ML models may be too large
- ❌ File uploads limited to 4.5MB
- ❌ 10-second timeout for API calls
- ❌ Database won't persist (SQLite)

### Recommended Setup:
✅ **Frontend on Vercel** (React)
✅ **Backend on Railway** (Flask + ML models)

## 🔄 Alternative: Split Deployment

### Option A: Railway for Backend

1. **Go to Railway**
   - Visit: https://railway.app
   - Sign in with GitHub

2. **Deploy Backend**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `SkinCare` repository
   - Add environment variables
   - Deploy!

3. **Get Backend URL**
   - Copy your Railway URL: `https://your-app.railway.app`

4. **Update Frontend**
   - In Vercel, add environment variable:
   ```
   VITE_API_URL = https://your-app.railway.app
   ```

### Option B: Render for Backend

1. **Go to Render**
   - Visit: https://render.com
   - Sign in with GitHub

2. **New Web Service**
   - Click "New" → "Web Service"
   - Connect GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Add Environment Variables**
   - Add all your API keys

4. **Deploy**
   - Click "Create Web Service"

## 🎯 Testing Deployment

After deployment, test these features:

1. **Frontend**
   - [ ] Login page loads
   - [ ] Can register new account
   - [ ] Dashboard displays

2. **Backend** (if deployed)
   - [ ] API endpoints respond
   - [ ] Image upload works
   - [ ] Analysis completes
   - [ ] PDF generation works

## 🐛 Troubleshooting

### Build Fails
```bash
# Check logs in Vercel dashboard
# Ensure all dependencies are listed
# Verify Node version
```

### API Not Working
```bash
# Check CORS settings
# Verify environment variables
# Test API endpoint directly
```

### Database Issues
```bash
# Use external database (PostgreSQL)
# Update DATABASE_URL in env variables
```

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs

## 🎉 Success!

Once deployed, share your app:
```
https://your-app.vercel.app
```

---

**Pro Tip**: For production with ML models, use Railway or Render for backend!

