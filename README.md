# 🥭 Mango Leaf Disease Detection API

A FastAPI-based REST API for detecting diseases in mango leaves using YOLO (You Only Look Once) object detection.

## 🚀 Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/mango-disease-detection)

## 📋 Features

- **Disease Detection**: Detects three types of conditions in mango leaves:
  - 🍂 **Die Back** - Fungal disease affecting mango leaves
  - 🌱 **Healthy** - Normal, healthy mango leaves  
  - 🦠 **Powder Mildew** - Fungal disease causing white powdery spots

- **Multiple Input Methods**:
  - Single image upload
  - Batch image processing (up to 10 images)
  - Base64 encoded images

- **Web Interface**: Beautiful drag & drop interface for easy testing

## 🛠️ Setup Instructions

### Option 1: Deploy to Railway (Recommended)

1. **Fork this repository** or **upload this folder** to your GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "Start a New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will automatically detect and deploy using the Dockerfile
7. Your API will be live at `https://your-app-name.railway.app`

### Option 2: Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Add your trained model**:
   - Copy your best trained model file to the root directory
   - Rename it to `best.pt`
   - Or update the model paths in `main.py`

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Access the application**:
   - Web Interface: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

## 📁 File Structure

```
railway_deployment/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── railway.toml        # Railway deployment config
├── static/
│   └── index.html      # Web interface
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## 🔗 API Endpoints

### Health Check
```bash
GET /health
```

### Single Image Prediction
```bash
POST /predict
Content-Type: multipart/form-data

Parameters:
- file: Image file (JPG, PNG, etc.)
- conf_threshold: Confidence threshold (0.0-1.0, default: 0.25)
```

### Batch Image Prediction
```bash
POST /predict_batch
Content-Type: multipart/form-data

Parameters:
- files: Multiple image files (max 10)
- conf_threshold: Confidence threshold (0.0-1.0, default: 0.25)
```

### Base64 Image Prediction
```bash
POST /predict_base64
Content-Type: application/json

Body:
{
  "image": "base64_encoded_image_data",
  "conf_threshold": 0.25
}
```

## 📊 Response Format

```json
{
  "filename": "mango_leaf.jpg",
  "results": {
    "detections": [
      {
        "bbox": {
          "x1": 100.5,
          "y1": 150.2,
          "x2": 300.8,
          "y2": 400.1
        },
        "confidence": 0.85,
        "class_id": 0,
        "class_name": "Die Back"
      }
    ],
    "num_detections": 1,
    "image_shape": {
      "width": 640,
      "height": 480
    }
  },
  "status": "success"
}
```

## 🧪 Testing Your Deployment

### Using the Web Interface
1. Visit your Railway URL
2. Drag & drop a mango leaf image
3. Adjust confidence threshold if needed
4. Click "Analyze Image"

### Using cURL
```bash
# Health check
curl https://your-app-name.railway.app/health

# Single prediction
curl -X POST "https://your-app-name.railway.app/predict" \
  -F "file=@mango_leaf.jpg" \
  -F "conf_threshold=0.25"
```

## 📝 Important Notes

### Model File
- **Before deploying**: Add your trained model file (`best.pt`) to the root directory
- The app will look for models in this order:
  1. `best.pt` (your trained model)
  2. `yolo11n.pt` (fallback)
  3. `yolov8s.pt` (fallback)

### Railway Deployment Tips
- Railway automatically detects the `Dockerfile`
- No environment variables required
- The app runs on the port specified by Railway
- Health check endpoint: `/health`

## 🔧 Customization

### Adding Your Model
1. Copy your trained YOLO model to the root directory
2. Rename it to `best.pt` or update the model paths in `main.py`:

```python
model_paths = [
    "your_model_name.pt",  # Add your model here
    "best.pt",
    "yolo11n.pt",
    "yolov8s.pt"
]
```

### Updating Classes
If your model has different classes, update the `CLASS_NAMES` dictionary in `main.py`:

```python
CLASS_NAMES = {
    0: "Your_Class_1",
    1: "Your_Class_2", 
    2: "Your_Class_3"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Model not loading**:
   - Ensure your model file is in the root directory
   - Check the model file name matches the paths in `main.py`

2. **Build fails on Railway**:
   - Check that all files are uploaded to GitHub
   - Verify `requirements.txt` has correct dependencies

3. **Predictions not working**:
   - Test the `/health` endpoint first
   - Check Railway logs for error messages

### Getting Help
- Check Railway build logs for specific errors
- Test locally first before deploying
- Ensure your model file is compatible with the ultralytics package

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Ready to deploy?** Upload this folder to GitHub and connect it to Railway! 🚀