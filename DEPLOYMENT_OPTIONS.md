# 🚀 Deployment Options for SkinCare AI

## Overview

This document outlines all deployment options for the SkinCare AI application, with pros, cons, and step-by-step guides.

## 📊 Comparison Table

| Platform | Best For | Cost | ML Support | File Upload | Database | Difficulty |
|----------|----------|------|------------|-------------|----------|------------|
| **Vercel** | Frontend | Free tier | ❌ Limited | 4.5MB | ❌ No persist | ⭐ Easy |
| **Railway** | Full-stack | $5/month | ✅ Yes | ✅ Unlimited | ✅ PostgreSQL | ⭐⭐ Medium |
| **Render** | Backend | Free tier | ✅ Yes | ✅ Unlimited | ✅ PostgreSQL | ⭐⭐ Medium |
| **Heroku** | Full-stack | $7/month | ✅ Yes | ✅ Unlimited | ✅ PostgreSQL | ⭐⭐⭐ Hard |
| **AWS** | Enterprise | Pay-as-go | ✅ Yes | ✅ Unlimited | ✅ RDS | ⭐⭐⭐⭐ Expert |
| **DigitalOcean** | Full control | $5/month | ✅ Yes | ✅ Unlimited | ✅ Any | ⭐⭐⭐ Hard |

## 🎯 Recommended Setup

### **Best Option: Split Deployment**

**Frontend**: Vercel (Free)
**Backend**: Railway ($5/month)
**Database**: Railway PostgreSQL (Included)
**Storage**: AWS S3 or Cloudinary (Free tier)

**Why?**
- ✅ Best performance
- ✅ Scalable
- ✅ Reliable
- ✅ Easy to maintain
- ✅ Cost-effective

---

## 1️⃣ Vercel (Frontend Only)

### Pros
- ✅ Free tier generous
- ✅ Automatic deployments
- ✅ Global CDN
- ✅ Easy setup
- ✅ Great for React

### Cons
- ❌ 10-second timeout
- ❌ Limited ML support
- ❌ Small file uploads
- ❌ No persistent storage

### Setup

**Step 1**: Deploy Frontend
```bash
# Already configured!
# Just push to GitHub and import to Vercel
```

**Step 2**: Configure
```
Root: ./
Build: cd frontend && npm run build
Output: frontend/dist
```

**Step 3**: Add Environment Variables
```
VITE_API_URL=https://your-backend.railway.app
```

### Cost
- **Free**: 100GB bandwidth, unlimited projects
- **Pro**: $20/month for more features

---

## 2️⃣ Railway (Recommended for Backend)

### Pros
- ✅ Supports Python/Flask
- ✅ Built-in PostgreSQL
- ✅ No timeout limits
- ✅ Easy deployment
- ✅ Great for ML models

### Cons
- ❌ Not free (but affordable)
- ❌ Less documentation

### Setup

**Step 1**: Install Railway CLI
```bash
npm install -g @railway/cli
```

**Step 2**: Login
```bash
railway login
```

**Step 3**: Initialize Project
```bash
cd /Users/priyanshumehra/SkinCancerProject/skin-cancer
railway init
```

**Step 4**: Add PostgreSQL
```bash
railway add postgresql
```

**Step 5**: Deploy
```bash
railway up
```

**Step 6**: Add Environment Variables
```bash
railway variables set ROBOFLOW_API_KEY=your_key
railway variables set GROQ_API_KEY=your_key
railway variables set SECRET_KEY=your_secret
```

**Step 7**: Get URL
```bash
railway domain
# Copy the URL: https://your-app.railway.app
```

### Cost
- **Free Trial**: $5 credit
- **Hobby**: $5/month
- **Pro**: $20/month

---

## 3️⃣ Render (Alternative Backend)

### Pros
- ✅ Free tier available
- ✅ Supports Python/Flask
- ✅ Built-in PostgreSQL
- ✅ Auto-scaling
- ✅ Good documentation

### Cons
- ❌ Free tier spins down after inactivity
- ❌ Slower cold starts

### Setup

**Step 1**: Create `render.yaml`
```yaml
services:
  - type: web
    name: skincare-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: ROBOFLOW_API_KEY
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: skincare-db
          property: connectionString

databases:
  - name: skincare-db
    databaseName: skincare
    user: skincare
```

**Step 2**: Deploy
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Configure settings
5. Deploy!

### Cost
- **Free**: 750 hours/month, spins down
- **Starter**: $7/month, always on
- **Standard**: $25/month, more resources

---

## 4️⃣ Heroku

### Pros
- ✅ Mature platform
- ✅ Many add-ons
- ✅ Good documentation
- ✅ Supports Python/Flask

### Cons
- ❌ No free tier anymore
- ❌ More expensive
- ❌ Complex setup

### Setup

**Step 1**: Install Heroku CLI
```bash
brew tap heroku/brew && brew install heroku
```

**Step 2**: Login
```bash
heroku login
```

**Step 3**: Create App
```bash
cd /Users/priyanshumehra/SkinCancerProject/skin-cancer
heroku create skincare-ai
```

**Step 4**: Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

**Step 5**: Create Procfile
```bash
echo "web: gunicorn app:app" > Procfile
```

**Step 6**: Deploy
```bash
git push heroku main
```

**Step 7**: Set Environment Variables
```bash
heroku config:set ROBOFLOW_API_KEY=your_key
heroku config:set GROQ_API_KEY=your_key
heroku config:set SECRET_KEY=your_secret
```

### Cost
- **Eco**: $5/month (sleeps after 30 min)
- **Basic**: $7/month (always on)
- **Standard**: $25/month (more resources)

---

## 5️⃣ AWS (Enterprise)

### Pros
- ✅ Most powerful
- ✅ Highly scalable
- ✅ Many services
- ✅ Global infrastructure

### Cons
- ❌ Complex setup
- ❌ Steep learning curve
- ❌ Can be expensive

### Setup

**Services Needed**:
- **EC2**: Server
- **RDS**: Database
- **S3**: File storage
- **CloudFront**: CDN
- **Route 53**: DNS

**Step 1**: Create EC2 Instance
```bash
# Use AWS Console or CLI
aws ec2 run-instances --image-id ami-xxx --instance-type t2.micro
```

**Step 2**: Install Dependencies
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
sudo apt update
sudo apt install python3-pip nginx
```

**Step 3**: Deploy Application
```bash
git clone https://github.com/priyanshu-3/SkinCare.git
cd SkinCare
pip3 install -r requirements.txt
```

**Step 4**: Configure Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5001;
    }
}
```

**Step 5**: Use PM2 or Supervisor
```bash
sudo apt install supervisor
```

### Cost
- **Free Tier**: 750 hours/month for 12 months
- **Typical**: $20-50/month
- **Production**: $100+/month

---

## 6️⃣ DigitalOcean

### Pros
- ✅ Simple pricing
- ✅ Good documentation
- ✅ Full control
- ✅ One-click apps

### Cons
- ❌ Manual setup required
- ❌ Need to manage server

### Setup

**Step 1**: Create Droplet
```bash
# Use DigitalOcean Console
# Choose Ubuntu 22.04
# Select $5/month plan
```

**Step 2**: SSH to Server
```bash
ssh root@your-droplet-ip
```

**Step 3**: Install Dependencies
```bash
apt update
apt install python3-pip nginx postgresql
```

**Step 4**: Deploy Application
```bash
git clone https://github.com/priyanshu-3/SkinCare.git
cd SkinCare
pip3 install -r requirements.txt
```

**Step 5**: Configure Nginx
```bash
nano /etc/nginx/sites-available/skincare
```

**Step 6**: Start Application
```bash
gunicorn --bind 0.0.0.0:5001 app:app
```

### Cost
- **Basic**: $5/month (1GB RAM)
- **Standard**: $12/month (2GB RAM)
- **Performance**: $24/month (4GB RAM)

---

## 🎯 My Recommendation

### For You: **Vercel + Railway**

**Why?**
1. **Easy Setup**: Both platforms are beginner-friendly
2. **Cost-Effective**: ~$5/month total
3. **Scalable**: Can handle growth
4. **Reliable**: 99.9% uptime
5. **No Server Management**: Focus on code, not infrastructure

### Setup Steps

**1. Deploy Backend to Railway**
```bash
npm install -g @railway/cli
railway login
cd /Users/priyanshumehra/SkinCancerProject/skin-cancer
railway init
railway up
```

**2. Get Railway URL**
```bash
railway domain
# Copy: https://skincare-production.up.railway.app
```

**3. Deploy Frontend to Vercel**
```bash
# Go to https://vercel.com/new
# Import GitHub repo
# Add environment variable:
VITE_API_URL=https://skincare-production.up.railway.app
# Deploy!
```

**4. Update Frontend API Calls**

Create `frontend/src/config.js`:
```javascript
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'
```

Update API calls:
```javascript
import { API_URL } from './config'

const response = await fetch(`${API_URL}/api/analyze`, {
  method: 'POST',
  body: formData
})
```

**5. Test Everything**
- ✅ Frontend loads
- ✅ Can login/register
- ✅ Image upload works
- ✅ Analysis completes
- ✅ PDF downloads

---

## 📊 Cost Breakdown

### Recommended Setup (Vercel + Railway)
```
Frontend (Vercel):     $0/month (free tier)
Backend (Railway):     $5/month
Database (Railway):    $0 (included)
Total:                 $5/month
```

### Alternative Setup (Render)
```
Frontend (Vercel):     $0/month
Backend (Render):      $7/month
Database (Render):     $0 (included)
Total:                 $7/month
```

### Enterprise Setup (AWS)
```
EC2 (t2.small):       $17/month
RDS (db.t3.micro):    $15/month
S3 Storage:           $5/month
CloudFront:           $10/month
Total:                $47/month
```

---

## 🔧 Next Steps

1. **Choose Your Platform**
   - Recommended: Railway for backend
   - Already set up: Vercel for frontend

2. **Deploy Backend**
   - Follow Railway setup above
   - Add environment variables
   - Test API endpoints

3. **Update Frontend**
   - Add backend URL to Vercel
   - Update API calls
   - Redeploy

4. **Test Everything**
   - User authentication
   - Image upload
   - Analysis
   - PDF generation
   - History

5. **Monitor**
   - Check logs
   - Monitor errors
   - Track performance

---

## 📞 Support

- **Railway**: https://railway.app/help
- **Vercel**: https://vercel.com/docs
- **Render**: https://render.com/docs

---

## 🎉 You're Ready!

Choose your deployment platform and follow the guide above. Good luck! 🚀

