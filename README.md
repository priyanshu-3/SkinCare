# Sk## ✨ Key Features

### Location-Aware Healthcare

- **GPS Location Detection**: Click the map marker button to auto-detect your location
- **Reverse Geocoding**: Automatically converts coordinates to city/state names
- **Personalized Hospital Recommendations**: AI suggests local healthcare facilities based on your location
- **Emergency Resources**: Location-specific emergency contact information

### Medical Insights Sections

The AI provides comprehensive medical guidance in these formatted sections:

- 📋 **Condition Overview**: Clear explanation of the detected condition
- ⚠️ **Important Precautions**: Actionable safety measures and next steps
- 🏥 **Recommended Medical Care**: Appropriate healthcare facilities and specialists
- 🗺️ **Nearest Hospital Recommendations**: Local hospital suggestions with directions
- 🚨 **Emergency Signs**: When to seek immediate medical attention
- 💝 **Supportive Message**: Compassionate guidance and encouragementr Detection Web Application

A comprehensive AI-powered web application for skin cancer detection using Roboflow models and Groq LLM for personalized medical insights.

## Features

- 🏥 **AI-Powered Diagnosis**: Uses Roboflow-trained models to classify 7 types of skin lesions
- 📸 **Multiple Input Methods**: Drag-and-drop file upload or live camera capture
- 🤖 **Personalized Insights**: Groq LLM (OpenAI GPT-OSS-20B) provides tailored medical advice and precautions with beautifully formatted sections
- 📍 **Location-Aware Care**: GPS location detection for personalized hospital recommendations
- 🏥 **Nearest Hospital Finder**: AI-powered suggestions for local healthcare facilities
- 📊 **Visual Analytics**: Interactive charts and confidence visualizations
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔒 **Patient Privacy**: All processing happens locally (except LLM calls)

## Skin Conditions Detected

1. **Actinic keratoses** - Precancerous growths (Medium Risk)
2. **Basal cell carcinoma** - Common skin cancer (High Risk)
3. **Benign keratosis-like lesions** - Non-cancerous growths (Low Risk)
4. **Dermatofibroma** - Benign skin growth (Low Risk)
5. **Melanocytic nevi** - Common moles (Low Risk)
6. **Melanoma** - Serious skin cancer (Very High Risk)
7. **Vascular lesions** - Blood vessel lesions (Low Risk)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit the `.env` file with your API keys:

```env
# Roboflow API Key (from https://roboflow.com)
ROBOFLOW_API_KEY=your-roboflow-api-key

# Model details
WORKSPACE=your-workspace-name
PROJECT=your-project-name
VERSION=your-model-version

# Groq API Key (from https://console.groq.com/)
GROQ_API_KEY=your-groq-api-key
```

### 3. Get API Keys

#### Roboflow API Key:

1. Go to [Roboflow](https://roboflow.com)
2. Sign in to your account
3. Go to Account Settings → API Keys
4. Copy your Private API Key

#### Groq API Key:

1. Go to [Groq Console](https://console.groq.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### Web Interface Features:

1. **Patient Information Form**:

   - Enter patient's full name, age, gender, and location
   - All fields except location are required

2. **Image Upload Options**:

   - **File Upload**: Drag and drop images or click to browse
   - **Camera Capture**: Use device camera for live capture

3. **Analysis Results**:
   - Primary diagnosis with confidence score
   - Risk level assessment
   - All model predictions ranked by confidence
   - Personalized medical insights from AI
   - Visual charts and analysis

### Supported Image Formats:

- JPG, JPEG, PNG
- Maximum file size: 16MB

## API Endpoints

- `GET /` - Main web interface
- `POST /analyze` - Analyze uploaded image
- `POST /capture` - Handle camera capture

## Medical Disclaimer

⚠️ **IMPORTANT**: This application is for educational and informational purposes only. The AI predictions are not a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for proper medical evaluation and care.

## Technical Details

### Backend:

- **Flask** - Web framework
- **Roboflow** - AI model inference
- **Groq** - LLM for medical insights
- **OpenCV & PIL** - Image processing
- **Matplotlib** - Data visualization

### Frontend:

- **Bootstrap 5** - Responsive UI
- **HTML5 Canvas** - Camera capture
- **Drag & Drop API** - File uploads
- **Fetch API** - AJAX requests

### Security:

- Client-side validation
- Secure file uploads
- CORS enabled
- Input sanitization

## Troubleshooting

### Common Issues:

1. **"Module not found" errors**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Camera not working**:

   - Ensure HTTPS connection for camera access
   - Grant camera permissions in browser
   - Try different browser (Chrome recommended)

3. **Model loading errors**:

   - Verify Roboflow API key and model details
   - Check internet connection
   - Ensure model is publicly accessible

4. **LLM response errors**:
   - Verify Groq API key
   - Check API quota/limits
   - Ensure stable internet connection

### Camera Capture Issues

If the camera is not working, try these solutions:

1. **Browser Permissions**: Allow camera access when prompted
2. **HTTPS Requirement**: Modern browsers require HTTPS for camera access. For local development:
   - Use `http://localhost:5000` or `http://127.0.0.1:5000`
   - Avoid IP addresses like `http://192.168.x.x:5000`
3. **Browser Compatibility**: Use Chrome, Firefox, or Edge (latest versions)
4. **Multiple Cameras**: If you have multiple cameras, the app uses the front camera on mobile
5. **Permissions Reset**: Clear browser permissions and try again
6. **Console Debug**: Press F12 to open developer tools and check for errors

**Quick Test**: Run `debug_camera.bat` for troubleshooting information.

## Development

### Project Structure:

```
skin-cancer-detection/
├── app.py                 # Flask application
├── main.py               # Command-line interface
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── README.md            # Documentation
├── templates/
│   └── index.html       # Web interface
└── static/
    └── uploads/         # Uploaded images
```

### Adding New Features:

1. **New skin conditions**: Update `CONDITION_INFO` in `app.py`
2. **Additional input methods**: Extend the upload/capture functionality
3. **Enhanced UI**: Modify `templates/index.html`
4. **New API endpoints**: Add routes in `app.py`

## License

This project is for educational purposes. Please ensure compliance with medical regulations and data privacy laws when deploying.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For technical issues or questions:

- Check the troubleshooting section above
- Review the code comments for implementation details
- Ensure all dependencies are properly installed

---

**Remember**: This tool provides AI-assisted analysis but should never replace professional medical consultation. Always seek advice from qualified healthcare providers for medical concerns.
