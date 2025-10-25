"""
XAI (Explainable AI) Module for Skin Cancer Detection
Implements LIME and SHAP for interpretable predictions
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from PIL import Image
import cv2
import os
from typing import Tuple, Dict, Callable


class SkinCancerExplainer:
    """
    Explainability tools for skin cancer detection models
    Uses LIME (Local Interpretable Model-agnostic Explanations)
    and SHAP (SHapley Additive exPlanations)
    """
    
    def __init__(self):
        self.lime_explainer = None
        self.shap_explainer = None
        
    def explain_with_lime(self, 
                         image_path: str,
                         predict_fn: Callable,
                         top_labels: int = 3,
                         num_samples: int = 1000,
                         save_path: str = None) -> Dict:
        """
        Generate LIME explanation for image classification
        
        Args:
            image_path: Path to input image
            predict_fn: Function that takes image and returns probabilities
            top_labels: Number of top classes to explain
            num_samples: Number of samples for LIME
            save_path: Path to save explanation visualization
        
        Returns:
            Dictionary with explanation data
        """
        try:
            from lime import lime_image
            from skimage.segmentation import mark_boundaries
            
            # Load and preprocess image
            img = Image.open(image_path).convert('RGB')
            img_array = np.array(img)
            
            # Resize to model input size
            img_resized = cv2.resize(img_array, (224, 224))
            
            # Initialize LIME explainer
            if self.lime_explainer is None:
                self.lime_explainer = lime_image.LimeImageExplainer()
            
            # Generate explanation
            print("🔍 Generating LIME explanation...")
            explanation = self.lime_explainer.explain_instance(
                img_resized,
                predict_fn,
                top_labels=top_labels,
                hide_color=0,
                num_samples=num_samples
            )
            
            # Get top predicted class
            top_class = explanation.top_labels[0]
            
            # Get positive and negative regions
            temp, mask = explanation.get_image_and_mask(
                top_class,
                positive_only=True,
                num_features=10,
                hide_rest=False
            )
            
            # Create visualization
            if save_path:
                self._visualize_lime(
                    img_resized, temp, mask, 
                    explanation, top_class, save_path
                )
            
            # Extract important features
            important_features = explanation.local_exp[top_class]
            
            return {
                'explanation': explanation,
                'top_class': top_class,
                'important_features': important_features,
                'visualization_path': save_path
            }
        
        except ImportError:
            print("⚠️ LIME not installed. Install with: pip install lime")
            return {}
        except Exception as e:
            print(f"❌ Error generating LIME explanation: {e}")
            return {}
    
    def _visualize_lime(self, original_img, lime_img, mask, explanation, top_class, save_path):
        """
        Create visualization of LIME explanation
        """
        from skimage.segmentation import mark_boundaries
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Original image
        axes[0].imshow(original_img)
        axes[0].set_title('Original Image', fontsize=14, fontweight='bold')
        axes[0].axis('off')
        
        # LIME explanation (positive regions)
        axes[1].imshow(mark_boundaries(lime_img, mask))
        axes[1].set_title(f'Important Regions\n(Class {top_class})', 
                         fontsize=14, fontweight='bold')
        axes[1].axis('off')
        
        # Heatmap
        axes[2].imshow(original_img)
        axes[2].imshow(mask, alpha=0.5, cmap='hot')
        axes[2].set_title('Attention Heatmap', fontsize=14, fontweight='bold')
        axes[2].axis('off')
        
        plt.suptitle('LIME Explainability Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ LIME visualization saved to {save_path}")
    
    def explain_with_shap(self,
                         features: np.ndarray,
                         model,
                         feature_names: list = None,
                         save_path: str = None) -> Dict:
        """
        Generate SHAP explanation for tabular features (ensemble model)
        
        Args:
            features: Feature vector (e.g., from ensemble model)
            model: Trained model with predict_proba method
            feature_names: Names of features
            save_path: Path to save explanation visualization
        
        Returns:
            Dictionary with SHAP values
        """
        try:
            import shap
            
            # Initialize SHAP explainer
            print("🔍 Generating SHAP explanation...")
            
            # Use TreeExplainer for XGBoost
            if hasattr(model, 'get_booster'):
                explainer = shap.TreeExplainer(model)
            else:
                explainer = shap.KernelExplainer(model.predict_proba, features)
            
            # Calculate SHAP values
            shap_values = explainer.shap_values(features)
            
            # Visualize
            if save_path:
                self._visualize_shap(
                    shap_values, features, 
                    feature_names, save_path
                )
            
            return {
                'shap_values': shap_values,
                'explainer': explainer,
                'visualization_path': save_path
            }
        
        except ImportError:
            print("⚠️ SHAP not installed. Install with: pip install shap")
            return {}
        except Exception as e:
            print(f"❌ Error generating SHAP explanation: {e}")
            return {}
    
    def _visualize_shap(self, shap_values, features, feature_names, save_path):
        """
        Create visualization of SHAP values
        """
        import shap
        
        plt.figure(figsize=(12, 6))
        
        # If multi-class, use the first class for visualization
        if isinstance(shap_values, list):
            shap_values_plot = shap_values[0]
        else:
            shap_values_plot = shap_values
        
        # Create waterfall plot
        if feature_names:
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values_plot[0],
                    base_values=0,
                    data=features[0],
                    feature_names=feature_names
                ),
                show=False
            )
        else:
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values_plot[0],
                    base_values=0,
                    data=features[0]
                ),
                show=False
            )
        
        plt.title('SHAP Feature Importance', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ SHAP visualization saved to {save_path}")
    
    def generate_grad_cam(self,
                         image_path: str,
                         model,
                         layer_name: str,
                         save_path: str = None) -> np.ndarray:
        """
        Generate Grad-CAM visualization for CNN models
        
        Args:
            image_path: Path to input image
            model: Trained CNN model
            layer_name: Name of layer to visualize
            save_path: Path to save visualization
        
        Returns:
            Grad-CAM heatmap
        """
        try:
            # Load image
            img = Image.open(image_path).convert('RGB')
            img_array = np.array(img)
            img_resized = cv2.resize(img_array, (224, 224))
            
            # Normalize
            img_normalized = img_resized / 255.0
            img_batch = np.expand_dims(img_normalized, axis=0)
            
            # This is a placeholder - actual implementation depends on framework
            # For TensorFlow/Keras:
            # from tensorflow.keras.models import Model
            # grad_model = Model([model.inputs], [model.get_layer(layer_name).output, model.output])
            # ...
            
            print("⚠️ Grad-CAM implementation requires specific CNN framework")
            print("   Placeholder: Use TensorFlow/Keras or PyTorch Grad-CAM")
            
            return None
        
        except Exception as e:
            print(f"❌ Error generating Grad-CAM: {e}")
            return None
    
    def create_comprehensive_explanation(self,
                                        image_path: str,
                                        predict_fn: Callable,
                                        ensemble_features: np.ndarray,
                                        ensemble_model,
                                        output_dir: str = 'explanations') -> Dict:
        """
        Create comprehensive explanation using multiple XAI methods
        
        Args:
            image_path: Path to input image
            predict_fn: Image prediction function
            ensemble_features: Features for ensemble model
            ensemble_model: Trained ensemble model
            output_dir: Directory to save explanations
        
        Returns:
            Dictionary with all explanations
        """
        os.makedirs(output_dir, exist_ok=True)
        
        results = {}
        
        # LIME explanation for image
        print("\n📊 Generating LIME explanation...")
        lime_path = os.path.join(output_dir, 'lime_explanation.png')
        lime_result = self.explain_with_lime(
            image_path, predict_fn, 
            save_path=lime_path
        )
        results['lime'] = lime_result
        
        # SHAP explanation for ensemble
        print("\n📊 Generating SHAP explanation...")
        shap_path = os.path.join(output_dir, 'shap_explanation.png')
        feature_names = [f'Feature_{i}' for i in range(ensemble_features.shape[1])]
        shap_result = self.explain_with_shap(
            ensemble_features, ensemble_model,
            feature_names=feature_names,
            save_path=shap_path
        )
        results['shap'] = shap_result
        
        print(f"\n✅ Comprehensive explanations saved to {output_dir}/")
        
        return results
    
    def generate_saliency_map(self, image_path: str, save_path: str = None) -> np.ndarray:
        """
        Generate simple saliency map using edge detection
        (Fallback method when LIME/SHAP not available)
        
        Args:
            image_path: Path to input image
            save_path: Path to save visualization
        
        Returns:
            Saliency map
        """
        # Load image
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Sobel edge detection
        sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        
        # Magnitude
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        magnitude = np.uint8(magnitude / magnitude.max() * 255)
        
        # Create visualization
        if save_path:
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            
            axes[0].imshow(img_rgb)
            axes[0].set_title('Original Image', fontsize=14, fontweight='bold')
            axes[0].axis('off')
            
            axes[1].imshow(magnitude, cmap='hot')
            axes[1].set_title('Saliency Map', fontsize=14, fontweight='bold')
            axes[1].axis('off')
            
            axes[2].imshow(img_rgb)
            axes[2].imshow(magnitude, alpha=0.5, cmap='hot')
            axes[2].set_title('Overlay', fontsize=14, fontweight='bold')
            axes[2].axis('off')
            
            plt.suptitle('Saliency Analysis', fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"✅ Saliency map saved to {save_path}")
        
        return magnitude


if __name__ == "__main__":
    """
    Demo: XAI explainability features
    """
    print("="*70)
    print("XAI (Explainability) Module Demo")
    print("="*70)
    
    # Initialize explainer
    explainer = SkinCancerExplainer()
    
    # Demo with a sample image (replace with actual image)
    test_image = "static/uploads/captured.jpg"
    
    if os.path.exists(test_image):
        print(f"\n📸 Using test image: {test_image}")
        
        # Generate saliency map (works without LIME/SHAP)
        print("\n🔍 Generating saliency map...")
        saliency = explainer.generate_saliency_map(
            test_image,
            save_path='explanations/saliency_map.png'
        )
        
        # Demo predict function (placeholder)
        def dummy_predict_fn(images):
            """Dummy prediction function for demo"""
            batch_size = len(images)
            num_classes = 7
            # Return random probabilities
            probs = np.random.dirichlet(np.ones(num_classes), size=batch_size)
            return probs
        
        # Try LIME explanation
        print("\n🔍 Attempting LIME explanation...")
        lime_result = explainer.explain_with_lime(
            test_image,
            dummy_predict_fn,
            save_path='explanations/lime_explanation.png'
        )
        
        if lime_result:
            print("✅ LIME explanation generated successfully")
        else:
            print("ℹ️ Install lime: pip install lime")
        
        print("\n✅ Demo completed!")
        print(f"📁 Check 'explanations/' folder for outputs")
    
    else:
        print(f"\n⚠️ Test image not found: {test_image}")
        print("Please upload an image first or update the path")

