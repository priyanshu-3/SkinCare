"""
Skin Cancer Detection Web Application
Flask app with Roboflow model integration and Groq LLM for medical advice
"""

import os
import json
import base64
from io import BytesIO
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename
from roboflow import Roboflow
from dotenv import load_dotenv
from groq import Groq
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import datetime, timedelta
import re
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


def convert_to_serializable(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj


def parse_markdown_for_pdf(text):
    """Parse Markdown text and return structured content for PDF rendering"""
    if not text:
        return []
    
    # Clean up text - remove problematic Unicode characters
    # Replace common Unicode characters that don't render well in PDF
    text = text.replace('—', '-')  # Em dash
    text = text.replace('–', '-')  # En dash
    text = text.replace(''', "'")  # Smart single quote
    text = text.replace(''', "'")  # Smart single quote
    text = text.replace('"', '"')  # Smart double quote
    text = text.replace('"', '"')  # Smart double quote
    text = text.replace('…', '...')  # Ellipsis
    text = text.replace('•', '*')  # Bullet point (we'll add our own)
    text = text.replace('→', '->')  # Arrow
    text = text.replace('←', '<-')  # Arrow
    text = text.replace('★', '*')  # Star
    text = text.replace('✓', 'v')  # Check mark
    text = text.replace('✗', 'x')  # X mark
    text = text.replace('®', '(R)')  # Registered trademark
    text = text.replace('©', '(c)')  # Copyright
    text = text.replace('™', '(TM)')  # Trademark
    
    # Remove any remaining non-ASCII characters that might cause issues
    # Keep only printable ASCII characters
    text = ''.join(char if ord(char) < 128 or char in '\n\r\t' else ' ' for char in text)
    
    lines = text.split('\n')
    parsed_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            parsed_content.append({'type': 'blank', 'content': ''})
            continue
        
        # Check for headers with special Unicode block characters (█ ▀ ▄ etc)
        # These often appear as black boxes - convert to text markers
        if any(char in line for char in ['█', '▀', '▄', '▌', '▐', '░', '▒', '▓', '■', '□', '▪', '▫']):
            # Remove these characters
            line = re.sub(r'[█▀▄▌▐░▒▓■□▪▫]', '', line)
        
        # Check for headers (## or ###)
        if line.startswith('### '):
            content = line[4:].strip()
            # Remove bold markers
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
            parsed_content.append({'type': 'header3', 'content': content})
        elif line.startswith('## '):
            content = line[3:].strip()
            # Remove bold markers
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
            parsed_content.append({'type': 'header2', 'content': content})
        # Check for bullet points
        elif line.startswith('- ') or line.startswith('* '):
            content = line[2:].strip()
            # Remove bold markers
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
            parsed_content.append({'type': 'bullet', 'content': content})
        # Check for disclaimer
        elif line.startswith('**Disclaimer:**') or 'Disclaimer' in line:
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
            parsed_content.append({'type': 'disclaimer', 'content': content})
        # Regular text
        else:
            # Remove bold markers from regular text
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
            parsed_content.append({'type': 'text', 'content': content})
    
    return parsed_content


def draw_markdown_content(canvas_obj, content_list, start_y, margin, max_width, page_height):
    """Draw parsed Markdown content on PDF canvas with proper formatting"""
    y = start_y
    line_height = 4 * mm
    
    for item in content_list:
        content_type = item['type']
        content = item['content']
        
        # Check if we need a new page
        if y < 40 * mm:
            canvas_obj.showPage()
            y = page_height - 30 * mm
        
        if content_type == 'blank':
            y -= line_height
            
        elif content_type == 'header2':
            canvas_obj.setFont('Helvetica-Bold', 11)
            canvas_obj.setFillColor(colors.HexColor('#1e40af'))  # Blue color
            canvas_obj.drawString(margin, y, content)
            canvas_obj.setFillColor(colors.black)
            y -= 6 * mm
            
        elif content_type == 'header3':
            canvas_obj.setFont('Helvetica-Bold', 10)
            canvas_obj.drawString(margin, y, content)
            y -= 5 * mm
            
        elif content_type == 'bullet':
            # Draw bullet point
            canvas_obj.setFont('Helvetica', 9)
            canvas_obj.circle(margin + 2 * mm, y + 1.5 * mm, 0.8 * mm, fill=1)
            
            # Wrap text for bullet points
            wrapped_lines = wrap_text(content, max_width - 8 * mm, canvas_obj, 'Helvetica', 9)
            for i, wrapped_line in enumerate(wrapped_lines):
                if i == 0:
                    canvas_obj.drawString(margin + 5 * mm, y, wrapped_line)
                else:
                    y -= line_height
                    if y < 40 * mm:
                        canvas_obj.showPage()
                        y = page_height - 30 * mm
                    canvas_obj.drawString(margin + 5 * mm, y, wrapped_line)
            y -= 5 * mm
            
        elif content_type == 'disclaimer':
            canvas_obj.setFont('Helvetica-Bold', 9)
            canvas_obj.setFillColor(colors.HexColor('#dc2626'))  # Red color
            wrapped_lines = wrap_text(content, max_width, canvas_obj, 'Helvetica-Bold', 9)
            for wrapped_line in wrapped_lines:
                if y < 40 * mm:
                    canvas_obj.showPage()
                    y = page_height - 30 * mm
                canvas_obj.drawString(margin, y, wrapped_line)
                y -= line_height
            canvas_obj.setFillColor(colors.black)
            y -= 2 * mm
            
        elif content_type == 'text':
            canvas_obj.setFont('Helvetica', 9)
            wrapped_lines = wrap_text(content, max_width, canvas_obj, 'Helvetica', 9)
            for wrapped_line in wrapped_lines:
                if y < 40 * mm:
                    canvas_obj.showPage()
                    y = page_height - 30 * mm
                canvas_obj.drawString(margin, y, wrapped_line)
                y -= line_height
            y -= 2 * mm
    
    return y


def wrap_text(text, max_width, canvas_obj, font_name, font_size):
    """Wrap text to fit within max_width"""
    # Clean any remaining special characters before wrapping
    text = ''.join(char if ord(char) < 128 else ' ' for char in text)
    
    canvas_obj.setFont(font_name, font_size)
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        # Skip empty words
        if not word.strip():
            continue
            
        test_line = ' '.join(current_line + [word])
        try:
            width = canvas_obj.stringWidth(test_line, font_name, font_size)
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        except Exception:
            # If we can't calculate width, just add the word
            current_line.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines if lines else ['']

# Import XGBoost ensemble and XAI modules
try:
    from ensemble_model import SkinCancerEnsemble, simulate_cnn_predictions
    ENSEMBLE_AVAILABLE = True
except ImportError:
    ENSEMBLE_AVAILABLE = False
    print("⚠️ Ensemble model not available")

try:
    from explainability import SkinCancerExplainer
    XAI_AVAILABLE = True
except ImportError:
    XAI_AVAILABLE = False
    print("⚠️ XAI module not available")

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for React frontend with credentials support
CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://localhost:5173', 'http://127.0.0.1:3000', 'http://127.0.0.1:5173'])

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database and Login setup
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='patient', nullable=False)  # patient | doctor | admin
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationship to analyses
    analyses = db.relationship('Analysis', backref='user', lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Analysis(db.Model):
    """Model for storing patient analysis records"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(255))  # City/location
    diagnosis = db.Column(db.String(255), nullable=False)  # Result/prediction
    confidence = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(500))
    viz_path = db.Column(db.String(500))
    report_path = db.Column(db.String(500))
    all_predictions = db.Column(db.Text)  # JSON string of all predictions
    llm_advice = db.Column(db.Text)  # LLM generated advice
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        """Convert analysis record to dictionary"""
        # Convert UTC to IST (UTC + 5:30) for display
        ist_time = self.created_at + timedelta(hours=5, minutes=30)
        return {
            'id': self.id,
            'patient_name': self.patient_name,
            'age': self.age,
            'gender': self.gender,
            'location': self.location,
            'diagnosis': self.diagnosis,
            'confidence': round(self.confidence, 2),
            'image_path': self.image_path,
            'viz_path': self.viz_path,
            'report_path': self.report_path,
            'all_predictions': json.loads(self.all_predictions) if self.all_predictions else [],
            'llm_advice': self.llm_advice,
            'created_at': ist_time.strftime('%Y-%m-%d %H:%M:%S')
        }


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_db():
    """Initialize database tables."""
    with app.app_context():
        db.create_all()


init_db()

# Initialize Roboflow
API_KEY = os.getenv("ROBOFLOW_API_KEY")
WORKSPACE = os.getenv("WORKSPACE")
PROJECT = os.getenv("PROJECT")
VERSION = os.getenv("VERSION")

rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT)
model = project.version(VERSION).model

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
groq_client = Groq(api_key=GROQ_API_KEY)

# Initialize XGBoost Ensemble
ensemble_model = None
if ENSEMBLE_AVAILABLE:
    try:
        ensemble_model = SkinCancerEnsemble(model_path='models/xgboost_ensemble.pkl')
        print("✅ XGBoost ensemble initialized")
    except Exception as e:
        print(f"⚠️ Could not initialize ensemble: {e}")

# Initialize XAI Explainer
explainer = None
if XAI_AVAILABLE:
    try:
        explainer = SkinCancerExplainer()
        print("✅ XAI explainer initialized")
    except Exception as e:
        print(f"⚠️ Could not initialize explainer: {e}")

# Skin condition information
CONDITION_INFO = {
    'Actinic keratoses': {
        'severity': 'Medium Risk',
        'color': '#FFA500',
        'description': 'Precancerous growths - Monitor closely'
    },
    'Basal cell carcinoma': {
        'severity': 'High Risk',
        'color': '#FF4500',
        'description': 'Common skin cancer - Treatable if caught early'
    },
    'Benign keratosis-like lesions': {
        'severity': 'Low Risk',
        'color': '#90EE90',
        'description': 'Non-cancerous growths - Generally harmless'
    },
    'Dermatofibroma': {
        'severity': 'Low Risk',
        'color': '#87CEEB',
        'description': 'Benign skin growth - Usually no treatment needed'
    },
    'Melanocytic nevi': {
        'severity': 'Low Risk',
        'color': '#98FB98',
        'description': 'Common moles - Monitor for changes'
    },
    'Melanoma': {
        'severity': 'VERY HIGH RISK',
        'color': '#DC143C',
        'description': 'Serious skin cancer - IMMEDIATE medical attention required'
    },
    'Vascular lesions': {
        'severity': 'Low Risk',
        'color': '#DDA0DD',
        'description': 'Blood vessel lesions - Usually harmless'
    }
}

def analyze_with_llm(name, age, gender, prediction, confidence, location="Unknown", latitude=None, longitude=None):
    """
    Get medical advice and insights from Groq LLM
    """
    try:
        condition_info = CONDITION_INFO.get(prediction, {})
        severity = condition_info.get('severity', 'Unknown')
        description = condition_info.get('description', 'Consult a healthcare professional')

        # Prepare location context
        location_context = f"Location: {location}"
        if latitude and longitude:
            location_context += f" (Coordinates: {latitude:.4f}, {longitude:.4f})"

        prompt = f"""
        As a medical AI assistant, provide helpful information about skin cancer detection results.
        Please be cautious and emphasize that this is NOT a medical diagnosis.

        Patient Information:
        - Name: {name}
        - Age: {age}
        - Gender: {gender}
        - {location_context}

        AI Model Prediction:
        - Condition: {prediction}
        - Confidence: {confidence:.2f}%
        - Risk Level: {severity}
        - Description: {description}

        Please provide a well-formatted response using markdown with these sections:

        ## 📋 Condition Overview
        Brief explanation of what this condition means and its characteristics

        ## ⚠️ Important Precautions
        - Bullet points of general precautions and next steps
        - Emphasize seeing a healthcare professional for proper diagnosis

        Format the response with clear headings, bullet points, and professional medical language.
        Always stress that this is not a substitute for professional medical advice.
        """

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful medical information assistant using advanced GPT technology. Always emphasize that AI predictions are not medical diagnoses and patients should consult healthcare professionals."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Unable to generate medical advice at this time. Error: {str(e)}. Please consult a healthcare professional."

def process_image_prediction(image_path):
    """
    Process image through Roboflow model
    """
    try:
        result = model.predict(image_path)
        predictions = result.json()

        pred_list = predictions.get('predictions')
        if not pred_list or not isinstance(pred_list, list) or len(pred_list) == 0:
            return None

        pred_data = predictions['predictions'][0]
        all_preds = pred_data['predictions']

        # Get top class
        predicted_classes = pred_data.get('predicted_classes', [])
        if predicted_classes:
            top_class = predicted_classes[0]
        else:
            top_class = max(all_preds, key=lambda x: all_preds[x]['confidence'])

        top_confidence = all_preds[top_class]['confidence'] * 100

        return {
            'top_class': top_class,
            'confidence': top_confidence,
            'all_predictions': all_preds,
            'image_info': pred_data['image']
        }

    except Exception as e:
        print(f"Error in prediction: {e}")
        return None

def create_visualization(image_path, predictions, save_path):
    """
    Create visualization chart
    """
    try:
        pred_data = predictions
        all_preds = pred_data['all_predictions']

        # Sort predictions
        sorted_preds = sorted(all_preds.items(),
                             key=lambda x: x[1]['confidence'],
                             reverse=True)

        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Left: Original Image
        img = Image.open(image_path)
        ax1.imshow(img)
        ax1.axis('off')
        ax1.set_title('Input Image', fontsize=16, fontweight='bold', pad=15)

        # Right: Confidence Chart
        classes = [item[0] for item in sorted_preds]
        confidences = [item[1]['confidence'] * 100 for item in sorted_preds]
        colors = [CONDITION_INFO.get(cls, {}).get('color', '#808080') for cls in classes]

        # Shorten labels
        short_labels = []
        for cls in classes:
            if len(cls) > 30:
                short_labels.append(cls[:27] + '...')
            else:
                short_labels.append(cls)

        bars = ax2.barh(range(len(classes)), confidences, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        bars[0].set_linewidth(3)
        bars[0].set_edgecolor('darkred')

        ax2.set_yticks(range(len(classes)))
        ax2.set_yticklabels(short_labels, fontsize=11)
        ax2.set_xlabel('Confidence (%)', fontsize=13, fontweight='bold')
        ax2.set_title('Classification Results', fontsize=16, fontweight='bold', pad=15)
        ax2.set_xlim(0, 100)
        ax2.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.7)

        for i, (bar, conf) in enumerate(zip(bars, confidences)):
            ax2.text(conf + 2, i, f'{conf:.1f}%',
                    va='center', ha='left', fontsize=10, fontweight='bold')

        top_class = classes[0]
        top_conf = confidences[0]
        ax2.text(0.5, 1.05, f'Top Prediction: {top_class} ({top_conf:.1f}%)',
                transform=ax2.transAxes, ha='center', fontsize=12,
                fontweight='bold', color='darkred',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()

        return True

    except Exception as e:
        print(f"Error creating visualization: {e}")
        return False

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    # Avoid 404s for favicon requests when no icon is provided
    return "", 204

@app.route('/analyze', methods=['POST'])
# @login_required  # Temporarily disabled for development
def analyze():
    """Analyze uploaded image"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        location = request.form.get('location', 'Unknown').strip()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        # Convert coordinates to float if provided
        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                latitude = None
                longitude = None

        # Validate required fields
        if not all([name, age, gender]):
            return jsonify({'error': 'Name, age, and gender are required'}), 400

        # Handle image upload
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400

        # Validate file type
        filename = secure_filename(file.filename)
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if file_ext not in allowed_extensions:
            return jsonify({
                'error': 'Invalid file format',
                'message': 'Please upload a valid image file (JPG, PNG, JPEG, GIF, BMP, or WEBP)'
            }), 400

        # Save uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Validate if it's actually an image
        try:
            img = Image.open(filepath)
            img.verify()  # Verify it's a valid image
            img = Image.open(filepath)  # Reopen after verify
            
            # Check image dimensions
            width, height = img.size
            if width < 50 or height < 50:
                os.remove(filepath)
                return jsonify({
                    'error': 'Image too small',
                    'message': 'Please upload an image with at least 50x50 pixels for accurate analysis'
                }), 400
                
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                'error': 'Invalid image file',
                'message': 'The uploaded file is not a valid image. Please try again with a different photo.'
            }), 400

        # Process image
        prediction_result = process_image_prediction(filepath)

        if not prediction_result:
            # Clean up the uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                'error': 'No skin lesion detected',
                'message': 'Unable to detect a skin lesion in this image. Please ensure:\n• The image shows a clear view of the skin lesion\n• The lesion is in focus and well-lit\n• The photo is taken from a close distance\n• Try uploading a different image'
            }), 400
        
        # Check if confidence is too low (threshold: 60%)
        if prediction_result['confidence'] < 60:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                'error': 'Invalid or unclear image detected',
                'message': f'The AI model has very low confidence ({prediction_result["confidence"]:.1f}%) in analyzing this image.\n\n⚠️ This usually means:\n• This is NOT a skin lesion image\n• The image shows something else entirely\n• The photo quality is extremely poor\n• The lesion is not visible or in focus\n\n✅ Please upload a clear, close-up photo of an actual skin lesion.\n\n📸 Tips for better results:\n• Use good lighting\n• Focus clearly on the lesion\n• Take photo from 6-12 inches away\n• Ensure the lesion fills most of the frame'
            }), 400
        
        # Additional validation: Check prediction distribution
        # If all predictions are similar (low variance), likely not a skin lesion
        all_preds = prediction_result.get('all_predictions', {})
        if all_preds:
            confidences = [pred.get('confidence', 0) for pred in all_preds.values()]
            if len(confidences) > 1:
                max_conf = max(confidences)
                min_conf = min(confidences)
                variance = max_conf - min_conf
                
                # If variance is too low, predictions are scattered (not confident about anything)
                if variance < 0.20 and max_conf < 0.65:  # Less than 20% difference and top is under 65%
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    return jsonify({
                        'error': 'Unable to identify skin lesion',
                        'message': 'The AI cannot confidently identify a skin lesion in this image.\n\n❌ This image may not contain a skin lesion at all.\n\n✅ Please ensure you upload:\n• A real photograph of a skin lesion/mole/spot\n• NOT drawings, cartoons, or unrelated images\n• Clear, focused photo of actual skin\n\n📸 The image should show human skin with a visible lesion.'
                    }), 400

        # Create visualization
        viz_path = os.path.join(app.config['UPLOAD_FOLDER'], f'viz_{filename}')
        create_visualization(filepath, prediction_result, viz_path)

        # XGBoost Ensemble Prediction (if available)
        ensemble_result = None
        if ensemble_model and ensemble_model.is_trained:
            try:
                # Simulate multiple CNN predictions for ensemble
                # In production, replace with actual multi-model predictions
                cnn_predictions = simulate_cnn_predictions(
                    prediction_result['top_class'], 
                    noise_level=0.05
                )
                
                # Prepare metadata
                metadata = {
                    'age': int(age),
                    'gender': gender,
                    'location': location
                }
                
                # Get ensemble features
                features = ensemble_model.prepare_features(cnn_predictions, metadata)
                
                # Predict with uncertainty
                uncertainty = ensemble_model.predict_with_uncertainty(features, n_iterations=10)
                
                ensemble_result = {
                    'prediction': uncertainty['prediction'],
                    'confidence': round(uncertainty['confidence'], 2),
                    'confidence_std': round(uncertainty['confidence_std'], 2),
                    'uncertainty_score': round(uncertainty['uncertainty_score'], 3),
                    'agreement_rate': round(uncertainty['agreement_rate'], 1),
                    'recommendation': uncertainty['recommendation']
                }
                
                print(f"✅ Ensemble prediction: {ensemble_result['prediction']} "
                      f"({ensemble_result['confidence']:.1f}% ± {ensemble_result['confidence_std']:.1f}%)")
            
            except Exception as e:
                print(f"⚠️ Ensemble prediction failed: {e}")
        
        # Generate Explainability (if available)
        explainability_paths = {}
        if explainer:
            try:
                # Generate saliency map (always works)
                saliency_path = os.path.join(app.config['UPLOAD_FOLDER'], f'saliency_{filename}')
                explainer.generate_saliency_map(filepath, save_path=saliency_path)
                explainability_paths['saliency'] = f'/static/uploads/saliency_{filename}'
                
                print("✅ Saliency map generated")
            
            except Exception as e:
                print(f"⚠️ Explainability generation failed: {e}")
        
        # Get LLM advice
        llm_advice = analyze_with_llm(
            name=name,
            age=age,
            gender=gender,
            prediction=prediction_result['top_class'],
            confidence=prediction_result['confidence'],
            location=location,
            latitude=latitude,
            longitude=longitude
        )

        # Prepare response
        response = {
            'success': True,
            'prediction': prediction_result['top_class'],
            'confidence': round(prediction_result['confidence'], 2),
            'all_predictions': convert_to_serializable(prediction_result['all_predictions']),
            'condition_info': CONDITION_INFO.get(prediction_result['top_class'], {}),
            'ensemble_result': convert_to_serializable(ensemble_result),
            'explainability': explainability_paths,
            'llm_advice': llm_advice,
            'image_path': f'/static/uploads/{filename}',
            'viz_path': f'/static/uploads/viz_{filename}',
            'patient_info': {
                'name': name,
                'age': age,
                'gender': gender,
                'location': location
            }
        }

        # Generate a professional PDF report and save it to uploads
        try:
            report_filename = f'report_{os.path.splitext(filename)[0]}.pdf'
            report_filepath = os.path.join(app.config['UPLOAD_FOLDER'], report_filename)

            def generate_report(pdf_path):
                c = canvas.Canvas(pdf_path, pagesize=A4)
                width, height = A4

                margin = 20 * mm
                usable_width = width - 2 * margin
                y = height - margin

                # Header
                c.setFont('Helvetica-Bold', 18)
                c.drawString(margin, y, 'Skin Cancer Analysis Report')
                c.setFont('Helvetica', 10)
                c.setFillColor(colors.gray)
                # Convert UTC to IST (UTC + 5:30)
                ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
                c.drawRightString(width - margin, y, f'Generated: {ist_time.strftime("%Y-%m-%d %H:%M IST")}')
                c.setFillColor(colors.black)
                y -= 12 * mm

                # Patient details box
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.5)
                c.rect(margin, y - 40 * mm, usable_width, 40 * mm, stroke=1, fill=0)
                pd_x = margin + 6 * mm
                pd_y = y - 8 * mm
                c.setFont('Helvetica-Bold', 12)
                c.drawString(pd_x, pd_y, 'Patient Information')
                c.setFont('Helvetica', 10)
                pd_y -= 6 * mm
                c.drawString(pd_x, pd_y, f'Name: {name}')
                pd_y -= 5 * mm
                c.drawString(pd_x, pd_y, f'Age: {age}    Gender: {gender}')
                pd_y -= 5 * mm
                c.drawString(pd_x, pd_y, f'Location: {location}')
                pd_y -= 5 * mm
                postal = request.form.get('postal_code') or request.form.get('pin') or ''
                if postal:
                    c.drawString(pd_x, pd_y, f'PIN/Postal Code: {postal}')

                # Images: input image on left, visualization on right
                img_y_top = y - 40 * mm - 6 * mm
                img_height = 80 * mm
                img_width = (usable_width - 6 * mm) / 2

                try:
                    input_img = ImageReader(filepath)
                    c.drawImage(input_img, margin, img_y_top - img_height, width=img_width, height=img_height, preserveAspectRatio=True, anchor='sw')
                except Exception:
                    # draw placeholder box
                    c.setStrokeColor(colors.gray)
                    c.rect(margin, img_y_top - img_height, img_width, img_height, stroke=1, fill=0)
                    c.drawString(margin + 6 * mm, img_y_top - 6 * mm, 'Input image could not be embedded')

                try:
                    viz_img = ImageReader(viz_path)
                    c.drawImage(viz_img, margin + img_width + 6 * mm, img_y_top - img_height, width=img_width, height=img_height, preserveAspectRatio=True, anchor='sw')
                except Exception:
                    c.setStrokeColor(colors.gray)
                    c.rect(margin + img_width + 6 * mm, img_y_top - img_height, img_width, img_height, stroke=1, fill=0)
                    c.drawString(margin + img_width + 12 * mm, img_y_top - 6 * mm, 'Visualization could not be embedded')

                # Move cursor below images
                y = img_y_top - img_height - 8 * mm

                # Diagnosis summary
                c.setFont('Helvetica-Bold', 12)
                c.drawString(margin, y, 'Diagnosis Summary')
                y -= 6 * mm
                c.setFont('Helvetica', 11)
                cond = prediction_result.get('top_class', 'Unknown')
                conf = prediction_result.get('confidence', 0)
                severity = CONDITION_INFO.get(cond, {}).get('severity', 'Unknown')
                description = CONDITION_INFO.get(cond, {}).get('description', '')
                c.drawString(margin, y, f'Condition: {cond}    Confidence: {conf:.1f}%    Risk: {severity}')
                y -= 6 * mm
                # Brief description (wrap)
                text = c.beginText(margin, y)
                text.setFont('Helvetica', 10)
                wrap = 95
                for line in description.split('\n'):
                    text.textLine(line)
                c.drawText(text)
                y -= 18 * mm

                # LLM Advice with proper Markdown parsing
                c.setFont('Helvetica-Bold', 12)
                c.drawString(margin, y, 'Medical Insights (AI)')
                y -= 6 * mm
                
                # Parse and render Markdown content
                advice = llm_advice or ''
                parsed_advice = parse_markdown_for_pdf(advice)
                y = draw_markdown_content(c, parsed_advice, y, margin, usable_width, height)

                # Footer: date/time and doctor signature
                footer_y = 25 * mm
                c.setFont('Helvetica', 9)
                # Use IST time for footer as well
                c.drawString(margin, footer_y + 10 * mm, f'Report generated: {ist_time.strftime("%Y-%m-%d %H:%M IST")}')

                # Doctor signature block
                sig_path = os.path.join(app.config['UPLOAD_FOLDER'], 'doctor_signature.png')
                if os.path.exists(sig_path):
                    try:
                        sig = ImageReader(sig_path)
                        sig_w = 40 * mm
                        sig_h = 20 * mm
                        c.drawImage(sig, width - margin - sig_w, footer_y + 2 * mm, width=sig_w, height=sig_h, preserveAspectRatio=True)
                        c.setFont('Helvetica', 9)
                        c.drawString(width - margin - sig_w, footer_y, 'Doctor Signature')
                    except Exception:
                        c.setFont('Helvetica', 9)
                        c.drawString(width - margin - 60 * mm, footer_y, 'Doctor Signature: ____________________')
                else:
                    c.setFont('Helvetica', 9)
                    c.drawString(width - margin - 60 * mm, footer_y, 'Doctor Signature: ____________________')

                c.showPage()
                c.save()

            generate_report(report_filepath)
            response['report_path'] = f'/static/uploads/{report_filename}'
        except Exception as e:
            print(f"⚠️ PDF report generation failed: {e}")
            response['report_path'] = None

        # Save analysis to database
        try:
            analysis_record = Analysis(
                user_id=current_user.id,
                patient_name=name,
                age=int(age),
                gender=gender,
                location=location,
                diagnosis=prediction_result['top_class'],
                confidence=prediction_result['confidence'],
                image_path=f'/static/uploads/{filename}',
                viz_path=f'/static/uploads/viz_{filename}',
                report_path=response.get('report_path'),
                all_predictions=json.dumps(prediction_result['all_predictions']),
                llm_advice=llm_advice
            )
            db.session.add(analysis_record)
            db.session.commit()
            print(f"✅ Analysis record saved (ID: {analysis_record.id})")
        except Exception as e:
            print(f"⚠️ Failed to save analysis record: {e}")
            db.session.rollback()

        return jsonify(response)

    except Exception as e:
        print(f"Error in analyze: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/capture', methods=['POST'])
@login_required
def capture():
    """Handle camera capture"""
    try:
        data = request.get_json()
        image_data = data.get('image')

        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400

        # Decode base64 image
        image_data = image_data.split(',')[1]  # Remove data:image/jpeg;base64, prefix
        image_bytes = base64.b64decode(image_data)

        # Save image
        image = Image.open(BytesIO(image_bytes))
        filename = f'capture_{int(np.random.rand() * 1000000)}.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        return jsonify({'filename': filename, 'path': f'/static/uploads/{filename}'})

    except Exception as e:
        return jsonify({'error': f'Capture failed: {str(e)}'}), 500

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html')


# API endpoints for React frontend
@app.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint for React frontend registration"""
    try:
        data = request.get_json() if request.is_json else request.form
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not all([name, email, password]):
            return jsonify({'error': 'Please fill all required fields'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        user = User(name=name, email=email, role='patient')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for React frontend login"""
    try:
        data = request.get_json() if request.is_json else request.form
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not all([email, password]):
            return jsonify({'error': 'Please fill all required fields'}), 400

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'success': True, 'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        return jsonify({'error': 'Login failed. Please try again.'}), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not all([name, email, password]):
            flash('Please fill all required fields', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return render_template('register.html')

        user = User(name=name, email=email, role='patient')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ===== Patient History API Endpoints =====

@app.route('/api/history', methods=['GET'])
@login_required
def get_patient_history():
    """Get patient analysis history with optional filtering"""
    try:
        # Get query parameters for filtering
        search = request.args.get('search', '').strip()
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        diagnosis = request.args.get('diagnosis')
        
        # Base query - get all analyses for current user
        query = Analysis.query.filter_by(user_id=current_user.id)
        
        # Apply search filter (searches name, location, diagnosis)
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    Analysis.patient_name.ilike(search_pattern),
                    Analysis.location.ilike(search_pattern),
                    Analysis.diagnosis.ilike(search_pattern)
                )
            )
        
        # Apply date range filter
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(Analysis.created_at >= start_dt)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                # Add one day to include the entire end date
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(Analysis.created_at <= end_dt)
            except ValueError:
                pass
        
        # Apply diagnosis filter
        if diagnosis:
            query = query.filter(Analysis.diagnosis == diagnosis)
        
        # Order by most recent first
        query = query.order_by(Analysis.created_at.desc())
        
        # Execute query
        analyses = query.all()
        
        # Convert to dictionaries
        history = [analysis.to_dict() for analysis in analyses]
        
        return jsonify({
            'success': True,
            'count': len(history),
            'history': history
        })
    
    except Exception as e:
        print(f"Error fetching history: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/<int:analysis_id>', methods=['GET'])
@login_required
def get_analysis_detail(analysis_id):
    """Get detailed information for a specific analysis"""
    try:
        analysis = Analysis.query.filter_by(
            id=analysis_id,
            user_id=current_user.id
        ).first()
        
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        return jsonify({
            'success': True,
            'analysis': analysis.to_dict()
        })
    
    except Exception as e:
        print(f"Error fetching analysis detail: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/export', methods=['GET'])
@login_required
def export_history_csv():
    """Export patient history as CSV"""
    try:
        import csv
        from io import StringIO
        from flask import make_response
        
        # Get all analyses for current user
        analyses = Analysis.query.filter_by(
            user_id=current_user.id
        ).order_by(Analysis.created_at.desc()).all()
        
        # Create CSV in memory
        si = StringIO()
        writer = csv.writer(si)
        
        # Write header
        writer.writerow([
            'ID',
            'Patient Name',
            'Age',
            'Gender',
            'Location',
            'Diagnosis',
            'Confidence (%)',
            'Date & Time'
        ])
        
        # Write data rows
        for analysis in analyses:
            # Convert UTC to IST (UTC + 5:30) for CSV export
            ist_time = analysis.created_at + timedelta(hours=5, minutes=30)
            writer.writerow([
                analysis.id,
                analysis.patient_name,
                analysis.age,
                analysis.gender,
                analysis.location or 'N/A',
                analysis.diagnosis,
                f"{analysis.confidence * 100:.2f}",
                ist_time.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Create response
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = f"attachment; filename=patient_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output.headers["Content-type"] = "text/csv"
        
        return output
    
    except Exception as e:
        print(f"Error exporting CSV: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/stats', methods=['GET'])
@login_required
def get_history_stats():
    """Get statistics about patient history"""
    try:
        analyses = Analysis.query.filter_by(user_id=current_user.id).all()
        
        if not analyses:
            return jsonify({
                'success': True,
                'stats': {
                    'total_analyses': 0,
                    'diagnosis_breakdown': {},
                    'avg_confidence': 0,
                    'latest_date': None
                }
            })
        
        # Calculate statistics
        total = len(analyses)
        diagnosis_breakdown = {}
        confidence_sum = 0
        
        for analysis in analyses:
            # Count diagnoses
            diagnosis_breakdown[analysis.diagnosis] = diagnosis_breakdown.get(analysis.diagnosis, 0) + 1
            confidence_sum += analysis.confidence
        
        # Convert latest date to IST
        latest_utc = max(a.created_at for a in analyses)
        latest_ist = latest_utc + timedelta(hours=5, minutes=30)
        latest_date = latest_ist.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'stats': {
                'total_analyses': total,
                'diagnosis_breakdown': diagnosis_breakdown,
                'avg_confidence': round(confidence_sum / total, 2),
                'latest_date': latest_date
            }
        })
    
    except Exception as e:
        print(f"Error calculating stats: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    app.run(debug=debug, host=host, port=port)