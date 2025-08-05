# Deploy PDF Tools Suite on Render

## Quick Deployment Steps

### 1. Prepare Your Files
Make sure you have these files in your project root:
- `render_requirements.txt` - Python dependencies for Render
- `render.yaml` - Render service configuration  
- `Procfile` - Process file for web service
- `runtime.txt` - Python version specification
- All your application files (app.py, main.py, templates/, static/, utils/)

### 2. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub, GitLab, or email
3. Verify your account

### 3. Deploy Options

#### Option A: Deploy from Git Repository (Recommended)
1. Push your code to GitHub/GitLab
2. In Render dashboard, click "New +"
3. Select "Web Service"
4. Connect your repository
5. Configure settings:
   - **Name**: `pdf-tools-suite`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r render_requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
   - **Plan**: Free (or paid for better performance)

#### Option B: Manual Upload
1. Create a new Web Service in Render
2. Choose "Deploy without Git"
3. Upload your project files
4. Use the same configuration as Option A

### 4. Environment Variables
Set these in Render dashboard under "Environment":
- `SESSION_SECRET`: Generate a random secret key
- `PYTHON_VERSION`: `3.11.13`

### 5. Configuration Files Explained

**render_requirements.txt**
```
Flask==3.1.1
PyPDF2==3.0.1
pdf2docx==0.5.8
python-pptx==1.0.2
reportlab==4.4.3
Werkzeug==3.1.3
gunicorn==21.2.0
```

**render.yaml** (Alternative configuration)
```yaml
services:
  - type: web
    name: pdf-tools-suite
    env: python
    buildCommand: "pip install -r render_requirements.txt"
    startCommand: "gunicorn --bind 0.0.0.0:$PORT main:app"
    plan: free
    envVars:
      - key: SESSION_SECRET
        generateValue: true
```

**Procfile**
```
web: gunicorn --bind 0.0.0.0:$PORT main:app
```

## Deployment Settings

### Basic Configuration
- **Runtime**: Python 3.11.13
- **Build Command**: `pip install -r render_requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
- **Port**: Render automatically sets $PORT environment variable

### Advanced Settings
- **Health Check Path**: `/` (homepage)
- **Auto-Deploy**: Enable for automatic deployments on git push
- **Instance Type**: Free tier (512MB RAM, 0.1 CPU)

## File Upload Considerations

### Render Free Tier Limitations
- **Memory**: 512MB RAM
- **CPU**: 0.1 CPU units
- **Disk**: 1GB storage
- **Bandwidth**: 100GB/month
- **Build time**: 15 minutes max

### Recommendations for PDF Processing
1. **File size limits**: Keep under 50MB for free tier
2. **Processing timeout**: Large files may timeout (consider upgrading)
3. **Memory usage**: PDF processing is memory-intensive
4. **Concurrent users**: Free tier handles ~10-20 concurrent users

## Post-Deployment

### 1. Test Your Application
- Visit your Render URL (e.g., `https://pdf-tools-suite.onrender.com`)
- Test file upload and processing
- Check all features work correctly

### 2. Monitor Performance
- Check Render dashboard for metrics
- Monitor build and deployment logs
- Watch for memory/CPU usage spikes

### 3. Custom Domain (Optional)
- Add custom domain in Render dashboard
- Configure DNS settings
- SSL certificate is automatic

## Troubleshooting

### Common Issues

**Build Failures**
- Check `render_requirements.txt` for correct package versions
- Verify Python version in `runtime.txt`
- Check build logs for specific errors

**Memory Issues**
- Large PDF files may cause memory errors
- Consider upgrading to paid plan for more RAM
- Implement file size restrictions

**Timeout Errors**
- PDF processing may take too long
- Upgrade to faster instance
- Optimize processing algorithms

### Environment Variables
Make sure to set:
```
SESSION_SECRET=your-random-secret-key-here
PYTHON_VERSION=3.11.13
```

## Upgrading for Production

### Recommended Paid Plan Features
- **Starter Plan ($7/month)**:
  - 512MB RAM → 1GB RAM
  - Better CPU performance
  - Custom domains
  - Priority support

- **Standard Plan ($25/month)**:
  - 2GB RAM
  - Faster builds
  - Advanced metrics

### Performance Optimizations
1. **Enable HTTP/2** - Automatic on Render
2. **Gzip compression** - Built into Gunicorn
3. **Static file caching** - Configure browser caching
4. **CDN integration** - For static assets

## Security Considerations

### Production Security
- Set strong `SESSION_SECRET`
- Enable HTTPS (automatic on Render)
- Implement rate limiting for file uploads
- Add input validation
- Monitor for suspicious activity

### File Security
- Temporary file cleanup is automatic
- Files are processed in isolated containers
- No persistent file storage on free tier

Your PDF Tools Suite will be accessible at:
`https://your-service-name.onrender.com`

The deployment should take 3-5 minutes and handle all the PDF processing features you built!