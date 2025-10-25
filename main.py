"""
Enhanced Skin Cancer Classification with Visualization
"""

import os
from roboflow import Roboflow
from PIL import Image
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key and model details
API_KEY = os.getenv("ROBOFLOW_API_KEY")
WORKSPACE = os.getenv("WORKSPACE")
PROJECT = os.getenv("PROJECT")
VERSION = os.getenv("VERSION")

# Check if all required environment variables are set
if not all([API_KEY, WORKSPACE, PROJECT, VERSION]):
    print("❌ Error: Please set all required environment variables in .env file")
    print("Required: ROBOFLOW_API_KEY, WORKSPACE, PROJECT, VERSION")
    exit(1)

# Initialize Roboflow
print("🔄 Loading Roboflow workspace...")
rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT)
model = project.version(VERSION).model
print("✅ Model loaded successfully!\n")

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

def print_results(predictions):
    """Print detailed classification results"""
    pred_list = predictions.get('predictions')
    if not pred_list or not isinstance(pred_list, list) or len(pred_list) == 0:
        print("❌ No prediction data available.")
        return None, None
    
    pred_data = predictions['predictions'][0]
    all_preds = pred_data['predictions']
    
    # Get top class from predictions if predicted_classes is empty
    predicted_classes = pred_data.get('predicted_classes', [])
    if predicted_classes:
        top_class = predicted_classes[0]
    else:
        # Find top class by confidence
        top_class = max(all_preds, key=lambda x: all_preds[x]['confidence'])
    
    # Sort by confidence
    sorted_preds = sorted(all_preds.items(), 
                         key=lambda x: x[1]['confidence'], 
                         reverse=True)
    
    print("="*70)
    print("🔬 SKIN LESION CLASSIFICATION RESULTS")
    print("="*70)
    
    # Image info
    img_info = pred_data['image']
    print(f"\n📸 Image: {pred_data.get('image_path', 'N/A')}")
    print(f"   Size: {img_info['width']} x {img_info['height']} pixels")
    
    # Top prediction
    top_conf = all_preds[top_class]['confidence'] * 100
    top_info = CONDITION_INFO.get(top_class, {})
    
    print(f"\n🎯 PRIMARY DIAGNOSIS:")
    print(f"   ╔════════════════════════════════════════════════════════════╗")
    print(f"   ║  Condition: {top_class:<45} ║")
    print(f"   ║  Confidence: {top_conf:>6.2f}%                                    ║")
    print(f"   ║  Risk Level: {top_info.get('severity', 'Unknown'):<44} ║")
    print(f"   ╚════════════════════════════════════════════════════════════╝")
    print(f"   ℹ️  {top_info.get('description', 'Consult a healthcare professional')}")
    
    # All predictions
    print(f"\n📊 ALL PREDICTIONS (Ranked by Confidence):")
    print(f"   {'#':<4} {'Condition':<35} {'Confidence':<12} {'Risk Level'}")
    print(f"   {'-'*75}")
    
    for rank, (condition, data) in enumerate(sorted_preds, 1):
        conf = data['confidence'] * 100
        risk = CONDITION_INFO.get(condition, {}).get('severity', 'Unknown')
        marker = "👉" if rank == 1 else "  "
        print(f"   {marker} {rank:<2} {condition:<35} {conf:>6.2f}%       {risk}")
    
    print("\n" + "="*70)
    print("⚠️  IMPORTANT DISCLAIMER:")
    print("   This is an AI-based prediction for REFERENCE PURPOSES ONLY.")
    print("   Always consult a qualified healthcare professional for")
    print("   proper medical diagnosis and treatment advice.")
    print("="*70 + "\n")
    
    return sorted_preds, top_class

def visualize_results(image_path, predictions, save_path="result_visualization.png"):
    """Create visual chart of predictions"""
    pred_list = predictions.get('predictions')
    if not pred_list or not isinstance(pred_list, list) or len(pred_list) == 0:
        print("❌ No prediction data available for visualization.")
        return
    
    pred_data = predictions['predictions'][0]
    all_preds = pred_data['predictions']
    
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
    
    # Shorten labels for display
    short_labels = []
    for cls in classes:
        if len(cls) > 30:
            short_labels.append(cls[:27] + '...')
        else:
            short_labels.append(cls)
    
    # Create horizontal bar chart
    bars = ax2.barh(range(len(classes)), confidences, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Highlight top prediction
    bars[0].set_linewidth(3)
    bars[0].set_edgecolor('darkred')
    
    ax2.set_yticks(range(len(classes)))
    ax2.set_yticklabels(short_labels, fontsize=11)
    ax2.set_xlabel('Confidence (%)', fontsize=13, fontweight='bold')
    ax2.set_title('Classification Results', fontsize=16, fontweight='bold', pad=15)
    ax2.set_xlim(0, 100)
    ax2.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.7)
    
    # Add percentage labels on bars
    for i, (bar, conf) in enumerate(zip(bars, confidences)):
        ax2.text(conf + 2, i, f'{conf:.1f}%', 
                va='center', ha='left', fontsize=10, fontweight='bold')
    
    # Add top prediction annotation
    top_class = classes[0]
    top_conf = confidences[0]
    ax2.text(0.5, 1.05, f'Top Prediction: {top_class} ({top_conf:.1f}%)', 
            transform=ax2.transAxes, ha='center', fontsize=12, 
            fontweight='bold', color='darkred',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"📊 Visualization saved as: {save_path}")
    plt.show()

def detect_skin_cancer(image_path, show_visualization=True):
    """
    Detect skin cancer type in an image.
    
    Args:
        image_path (str): Path to the image file
        show_visualization (bool): Whether to show visualization
        
    Returns:
        dict: Prediction results
    """
    try:
        print(f"🔍 Analyzing image: {os.path.basename(image_path)}...")
        
        # Run prediction
        result = model.predict(image_path)
        predictions = result.json()
        
        # Check if predictions exist
        pred_list = predictions.get('predictions')
        if not pred_list or not isinstance(pred_list, list) or len(pred_list) == 0:
            print("❌ No predictions returned from the model.")
            return None
        
        # Print detailed results
        sorted_preds, top_class = print_results(predictions)
        
        # Create visualization
        if show_visualization:
            print("\n📊 Generating visualization...")
            visualize_results(image_path, predictions)
        
        return predictions
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return None

def batch_process(image_folder):
    """Process multiple images in a folder"""
    import glob
    
    # Supported image formats
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(image_folder, ext)))
        image_files.extend(glob.glob(os.path.join(image_folder, ext.upper())))
    
    if not image_files:
        print(f"❌ No images found in folder: {image_folder}")
        return
    
    print(f"📁 Found {len(image_files)} images. Processing...\n")
    
    results_summary = []
    
    for i, img_path in enumerate(image_files, 1):
        print(f"\n{'='*70}")
        print(f"Processing {i}/{len(image_files)}: {os.path.basename(img_path)}")
        print(f"{'='*70}")
        
        result = detect_skin_cancer(img_path, show_visualization=False)
        
        if result:
            pred_data = result['predictions'][0]
            top_class = pred_data['predicted_classes'][0]
            top_conf = pred_data['predictions'][top_class]['confidence'] * 100
            
            results_summary.append({
                'file': os.path.basename(img_path),
                'prediction': top_class,
                'confidence': top_conf
            })
    
    # Print summary
    print("\n" + "="*70)
    print("📋 BATCH PROCESSING SUMMARY")
    print("="*70)
    print(f"{'Image':<30} {'Prediction':<30} {'Confidence'}")
    print("-"*70)
    for res in results_summary:
        print(f"{res['file']:<30} {res['prediction']:<30} {res['confidence']:>6.2f}%")
    print("="*70)

if __name__ == "__main__":
    print("🏥 Skin Cancer Classification System")
    print("="*70 + "\n")
    
    # Choose mode
    print("Select mode:")
    print("1. Single image analysis")
    print("2. Batch process folder")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        # Single image mode
        image_path = r"C:\OneDrive\图片\Screenshots\Screenshot 2025-10-05 082319.png"
        
        # You can also ask user for input
        # image_path = input("Enter image path: ").strip()
        
        if os.path.exists(image_path):
            results = detect_skin_cancer(image_path, show_visualization=True)
            if results:
                print("\n✅ Analysis completed successfully!")
            else:
                print("\n❌ Analysis failed.")
        else:
            print(f"❌ Image not found: {image_path}")
            
    elif choice == "2":
        # Batch processing mode
        folder_path = input("Enter folder path: ").strip()
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            batch_process(folder_path)
        else:
            print(f"❌ Folder not found: {folder_path}")
    else:
        print("❌ Invalid choice!")