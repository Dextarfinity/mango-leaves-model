import os
import io
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from ultralytics import YOLO
import cv2
import base64
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mango Leaf Disease Detection API",
    description="API for detecting diseases in mango leaves using YOLO",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variable to store the model
model = None

# Disease class names
CLASS_NAMES = {
    0: "Die Back",
    1: "Healthy", 
    2: "Powder Mildew"
}

def load_model():
    """Load the YOLO model"""
    global model
    try:
        # Try to load the best trained model first
        model_paths = [
            "best.pt",  # Place your trained model here
            "yolo11n.pt",
            "yolov8n.pt"  # Use smaller model for faster loading
        ]
        
        for path in model_paths:
            if os.path.exists(path):
                logger.info(f"Loading model from {path}")
                model = YOLO(path)
                return model
        
        # If no model found, use the smallest default one for Railway
        logger.warning("No trained model found, using YOLOv8n (smallest)")
        model = YOLO("yolov8n.pt")
        return model
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        # Fallback to basic YOLO model
        try:
            logger.info("Attempting fallback to basic YOLO model...")
            model = YOLO("yolov8n.pt")
            return model
        except Exception as fallback_e:
            logger.error(f"Fallback model loading failed: {fallback_e}")
            raise e

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        # Don't crash the app, let it start without model for debugging
        logger.warning("App starting without model - check /health endpoint")

@app.get("/")
async def root():
    """Serve the main web interface"""
    return FileResponse("static/index.html")

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Mango Leaf Disease Detection API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "predict_batch": "/predict_batch",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "model_loaded": model is not None,
            "classes": CLASS_NAMES,
            "message": "Mango Disease Detection API is running"
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "degraded",
            "model_loaded": False,
            "error": str(e),
            "message": "API is running but model may not be loaded"
        }

def process_image(image_bytes: bytes) -> Image.Image:
    """Process uploaded image bytes"""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=400, detail="Invalid image format")

def run_inference(image: Image.Image, conf_threshold: float = 0.25) -> Dict[str, Any]:
    """Run YOLO inference on image"""
    try:
        # Convert PIL to numpy array
        img_array = np.array(image)
        
        # Run inference
        results = model(img_array, conf=conf_threshold)
        
        # Process results
        detections = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Get confidence and class
                    confidence = float(box.conf[0].cpu().numpy())
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = CLASS_NAMES.get(class_id, f"Unknown_{class_id}")
                    
                    detection = {
                        "bbox": {
                            "x1": float(x1),
                            "y1": float(y1),
                            "x2": float(x2),
                            "y2": float(y2)
                        },
                        "confidence": confidence,
                        "class_id": class_id,
                        "class_name": class_name
                    }
                    detections.append(detection)
        
        return {
            "detections": detections,
            "num_detections": len(detections),
            "image_shape": {
                "width": image.width,
                "height": image.height
            }
        }
        
    except Exception as e:
        logger.error(f"Error during inference: {e}")
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

@app.post("/predict")
async def predict_single_image(
    file: UploadFile = File(...),
    conf_threshold: float = 0.25
):
    """
    Predict diseases in a single mango leaf image
    
    - **file**: Image file (JPG, PNG, etc.)
    - **conf_threshold**: Confidence threshold for detections (0.0-1.0)
    """
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        image_bytes = await file.read()
        image = process_image(image_bytes)
        
        # Run inference
        results = run_inference(image, conf_threshold)
        
        return {
            "filename": file.filename,
            "results": results,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in predict endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict_batch")
async def predict_batch_images(
    files: List[UploadFile] = File(...),
    conf_threshold: float = 0.25
):
    """
    Predict diseases in multiple mango leaf images
    
    - **files**: List of image files
    - **conf_threshold**: Confidence threshold for detections (0.0-1.0)
    """
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files per batch")
    
    results = []
    
    for file in files:
        if not file.content_type.startswith('image/'):
            results.append({
                "filename": file.filename,
                "error": "File must be an image",
                "status": "failed"
            })
            continue
        
        try:
            # Read and process image
            image_bytes = await file.read()
            image = process_image(image_bytes)
            
            # Run inference
            prediction_results = run_inference(image, conf_threshold)
            
            results.append({
                "filename": file.filename,
                "results": prediction_results,
                "status": "success"
            })
            
        except Exception as e:
            logger.error(f"Error processing {file.filename}: {e}")
            results.append({
                "filename": file.filename,
                "error": str(e),
                "status": "failed"
            })
    
    return {
        "batch_results": results,
        "total_files": len(files),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] == "failed"])
    }

@app.post("/predict_base64")
async def predict_base64_image(
    image_data: dict,
    conf_threshold: float = 0.25
):
    """
    Predict diseases from base64 encoded image
    
    - **image_data**: Dict with 'image' key containing base64 encoded image
    - **conf_threshold**: Confidence threshold for detections (0.0-1.0)
    """
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Decode base64 image
        image_base64 = image_data.get('image', '')
        if not image_base64:
            raise HTTPException(status_code=400, detail="No image data provided")
        
        # Remove data URL prefix if present
        if image_base64.startswith('data:image'):
            image_base64 = image_base64.split(',')[1]
        
        image_bytes = base64.b64decode(image_base64)
        image = process_image(image_bytes)
        
        # Run inference
        results = run_inference(image, conf_threshold)
        
        return {
            "results": results,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error in base64 predict endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")