# Railway Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Prepare Your Model
**IMPORTANT**: Before deploying, you need to add your trained model file.

1. Copy your best trained model from `runs/detect/mango_augmented/weights/best.pt` or `runs/detect/mango_augmented2/weights/best.pt`
2. Place it in the `railway_deployment` folder
3. Rename it to `best.pt`

### 2. Upload to GitHub
1. Create a new repository on GitHub
2. Upload the entire `railway_deployment` folder contents
3. Make sure `best.pt` is included (check file size limits)

### 3. Deploy to Railway

1. **Go to Railway**:
   - Visit [Railway.app](https://railway.app)
   - Sign up/Login with GitHub

2. **Create New Project**:
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Automatic Deployment**:
   - Railway detects the `Dockerfile` automatically
   - Build process starts immediately
   - Wait for deployment to complete (5-10 minutes)

4. **Get Your URL**:
   - Railway provides a URL like `https://your-app-name.railway.app`
   - Click on the URL to access your API

### 4. Test Your Deployment

1. **Health Check**:
   ```
   https://your-app-name.railway.app/health
   ```

2. **Web Interface**:
   ```
   https://your-app-name.railway.app
   ```

3. **API Documentation**:
   ```
   https://your-app-name.railway.app/docs
   ```

## 📁 File Checklist

Before uploading to GitHub, ensure you have:
- ✅ `main.py` - FastAPI application
- ✅ `requirements.txt` - Dependencies
- ✅ `Dockerfile` - Container config
- ✅ `railway.toml` - Railway config
- ✅ `static/index.html` - Web interface
- ✅ `README.md` - Documentation
- ✅ `.gitignore` - Git ignore rules
- ✅ **`best.pt`** - Your trained model (REQUIRED!)

## ⚠️ Important Notes

### Model File Size
- GitHub has a 100MB file limit
- If your model is larger, use Git LFS:
  ```bash
  git lfs track "*.pt"
  git add .gitattributes
  git add best.pt
  git commit -m "Add model with LFS"
  ```

### Railway Limits
- Free tier: 512MB RAM, 1GB storage
- If you need more resources, upgrade your Railway plan

### Build Time
- First deployment: 5-10 minutes
- Subsequent deployments: 2-5 minutes

## 🔧 Troubleshooting

### Build Fails
1. **Check GitHub upload**: Ensure all files are uploaded
2. **Check model file**: Make sure `best.pt` exists
3. **Check Railway logs**: Look for specific error messages
4. **Verify dependencies**: Ensure `requirements.txt` is correct

### Model Loading Issues
1. **File path**: Model should be in root directory as `best.pt`
2. **File format**: Must be a valid YOLO `.pt` file
3. **Compatibility**: Ensure model is compatible with ultralytics version

### Memory Issues
1. **Upgrade Railway plan** for more RAM
2. **Optimize model**: Use smaller YOLO variant if needed
3. **Reduce batch size**: Lower the batch processing limit

## 📞 Getting Help

### Railway Support
- Railway Dashboard > Project > Logs
- Railway Discord community
- Railway documentation: https://docs.railway.app

### Common Error Solutions

**"Model not found"**:
- Check that `best.pt` is in the root directory
- Verify file was uploaded to GitHub

**"Out of memory"**:
- Upgrade Railway plan
- Use a smaller model file

**"Build timeout"**:
- Check for large files
- Optimize Docker layers

## 🎉 Success!

Once deployed successfully, you'll have:
- 🌐 **Web Interface**: Upload images via browser
- 📱 **REST API**: Integrate with mobile/web apps  
- 📊 **Interactive Docs**: Test API endpoints
- 🔍 **Health Monitoring**: Check system status

Your mango disease detection API is now live and ready to use! 🥭