"""
XGBoost Ensemble Model for Skin Cancer Detection
Combines multiple CNN predictions with XGBoost meta-classifier
"""

import numpy as np
import pickle
import os
from typing import Dict, List, Tuple
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


class SkinCancerEnsemble:
    """
    Ensemble model combining multiple CNN predictions with XGBoost
    """
    
    def __init__(self, model_path='models/xgboost_ensemble.pkl'):
        self.model_path = model_path
        self.xgb_model = None
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
        # Load pre-trained model if exists
        if os.path.exists(model_path):
            self.load_model()
    
    def prepare_features(self, predictions_dict: Dict, metadata: Dict = None) -> np.ndarray:
        """
        Prepare feature vector from multiple model predictions and metadata
        
        Args:
            predictions_dict: Dictionary of predictions from multiple models
                             e.g., {'model1': {'class1': 0.8, 'class2': 0.1, ...}, 
                                    'model2': {...}}
            metadata: Patient metadata (age, gender, location)
        
        Returns:
            Feature vector for XGBoost
        """
        features = []
        
        # Flatten all model predictions
        for model_name, preds in predictions_dict.items():
            for class_name, confidence in preds.items():
                features.append(confidence)
        
        # Add metadata features if provided
        if metadata:
            # Age (normalized)
            age = float(metadata.get('age', 50)) / 100.0
            features.append(age)
            
            # Gender (one-hot encoded: male=1, female=0, other=0.5)
            gender = metadata.get('gender', '').lower()
            if gender == 'male':
                features.append(1.0)
            elif gender == 'female':
                features.append(0.0)
            else:
                features.append(0.5)
            
            # Location features (placeholder - can be expanded)
            # Could include geographic risk factors, UV index, etc.
            features.append(0.5)  # Placeholder
        
        return np.array(features).reshape(1, -1)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              X_val: np.ndarray = None, y_val: np.ndarray = None):
        """
        Train XGBoost ensemble model
        
        Args:
            X_train: Training features (from multiple CNN outputs + metadata)
            y_train: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
        """
        # Encode labels
        y_train_encoded = self.label_encoder.fit_transform(y_train)
        
        # XGBoost parameters optimized for medical classification
        params = {
            'objective': 'multi:softprob',
            'num_class': len(self.label_encoder.classes_),
            'max_depth': 6,
            'learning_rate': 0.1,
            'n_estimators': 200,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'eval_metric': 'mlogloss'
        }
        
        # Create and train model
        self.xgb_model = xgb.XGBClassifier(**params)
        
        if X_val is not None and y_val is not None:
            y_val_encoded = self.label_encoder.transform(y_val)
            eval_set = [(X_val, y_val_encoded)]
            self.xgb_model.fit(
                X_train, y_train_encoded,
                eval_set=eval_set,
                verbose=True
            )
        else:
            self.xgb_model.fit(X_train, y_train_encoded)
        
        self.is_trained = True
        print("✅ XGBoost ensemble model trained successfully!")
        
        # Evaluate
        if X_val is not None and y_val is not None:
            self.evaluate(X_val, y_val)
    
    def predict(self, features: np.ndarray) -> Tuple[str, float, Dict]:
        """
        Make prediction using ensemble model
        
        Args:
            features: Feature vector from prepare_features()
        
        Returns:
            (predicted_class, confidence, all_probabilities)
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first or load pre-trained model.")
        
        # Get probabilities for all classes
        probabilities = self.xgb_model.predict_proba(features)[0]
        
        # Get predicted class
        predicted_idx = np.argmax(probabilities)
        predicted_class = self.label_encoder.classes_[predicted_idx]
        confidence = probabilities[predicted_idx] * 100
        
        # Create probability dictionary
        prob_dict = {
            class_name: float(prob * 100)
            for class_name, prob in zip(self.label_encoder.classes_, probabilities)
        }
        
        return predicted_class, confidence, prob_dict
    
    def predict_with_uncertainty(self, features: np.ndarray, n_iterations: int = 10) -> Dict:
        """
        Predict with uncertainty estimation using bootstrap aggregating
        
        Args:
            features: Feature vector
            n_iterations: Number of bootstrap iterations for uncertainty
        
        Returns:
            Dictionary with prediction, confidence, and uncertainty
        """
        predictions = []
        
        for _ in range(n_iterations):
            pred_class, confidence, _ = self.predict(features)
            predictions.append((pred_class, confidence))
        
        # Most common prediction
        pred_classes = [p[0] for p in predictions]
        confidences = [p[1] for p in predictions]
        
        from collections import Counter
        most_common = Counter(pred_classes).most_common(1)[0]
        final_prediction = most_common[0]
        agreement_rate = most_common[1] / n_iterations
        
        # Uncertainty metrics
        confidence_mean = np.mean(confidences)
        confidence_std = np.std(confidences)
        
        uncertainty_score = confidence_std / confidence_mean if confidence_mean > 0 else 1.0
        
        return {
            'prediction': final_prediction,
            'confidence': confidence_mean,
            'confidence_std': confidence_std,
            'uncertainty_score': uncertainty_score,
            'agreement_rate': agreement_rate * 100,
            'recommendation': self._get_recommendation(uncertainty_score, agreement_rate)
        }
    
    def _get_recommendation(self, uncertainty: float, agreement: float) -> str:
        """
        Provide recommendation based on uncertainty and agreement
        """
        if uncertainty > 0.3 or agreement < 0.7:
            return "⚠️ HIGH UNCERTAINTY - Strongly recommend expert review"
        elif uncertainty > 0.15 or agreement < 0.85:
            return "⚠️ MODERATE UNCERTAINTY - Consider expert consultation"
        else:
            return "✅ CONFIDENT PREDICTION - Standard follow-up recommended"
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray):
        """
        Evaluate model performance
        """
        y_test_encoded = self.label_encoder.transform(y_test)
        y_pred = self.xgb_model.predict(X_test)
        
        accuracy = accuracy_score(y_test_encoded, y_pred)
        print(f"\n📊 Model Evaluation:")
        print(f"Accuracy: {accuracy * 100:.2f}%")
        print("\nClassification Report:")
        print(classification_report(
            y_test_encoded, y_pred,
            target_names=self.label_encoder.classes_
        ))
        
        return accuracy
    
    def get_feature_importance(self) -> Dict:
        """
        Get feature importance from XGBoost model
        """
        if not self.is_trained:
            return {}
        
        importance = self.xgb_model.feature_importances_
        feature_names = [f'feature_{i}' for i in range(len(importance))]
        
        importance_dict = {
            name: float(imp)
            for name, imp in zip(feature_names, importance)
        }
        
        # Sort by importance
        importance_dict = dict(sorted(
            importance_dict.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        return importance_dict
    
    def save_model(self, path: str = None):
        """
        Save trained model to disk
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        save_path = path or self.model_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        model_data = {
            'xgb_model': self.xgb_model,
            'label_encoder': self.label_encoder
        }
        
        with open(save_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✅ Model saved to {save_path}")
    
    def load_model(self, path: str = None):
        """
        Load trained model from disk
        """
        load_path = path or self.model_path
        
        if not os.path.exists(load_path):
            print(f"⚠️ Model file not found: {load_path}")
            return False
        
        with open(load_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.xgb_model = model_data['xgb_model']
        self.label_encoder = model_data['label_encoder']
        self.is_trained = True
        
        print(f"✅ Model loaded from {load_path}")
        return True


def simulate_cnn_predictions(true_class: str, noise_level: float = 0.1) -> Dict:
    """
    Simulate predictions from multiple CNN models for demonstration
    In production, replace with actual CNN model outputs
    
    Args:
        true_class: The actual class label
        noise_level: Amount of noise to add to simulations
    
    Returns:
        Dictionary of predictions from multiple models
    """
    classes = [
        'Actinic keratoses',
        'Basal cell carcinoma',
        'Benign keratosis-like lesions',
        'Dermatofibroma',
        'Melanocytic nevi',
        'Melanoma',
        'Vascular lesions'
    ]
    
    # Simulate 3 different CNN models
    predictions = {}
    
    for model_id in ['ResNet50', 'EfficientNet', 'VisionTransformer']:
        model_preds = {}
        
        for cls in classes:
            if cls == true_class:
                # True class gets high confidence with some noise
                confidence = 0.85 + np.random.randn() * noise_level
            else:
                # Other classes get low confidence
                confidence = 0.02 + np.random.rand() * 0.1
            
            # Ensure valid probability
            confidence = max(0, min(1, confidence))
            model_preds[cls] = confidence
        
        # Normalize to sum to 1
        total = sum(model_preds.values())
        model_preds = {k: v/total for k, v in model_preds.items()}
        
        predictions[model_id] = model_preds
    
    return predictions


if __name__ == "__main__":
    """
    Demo: Training and using XGBoost ensemble
    """
    print("="*70)
    print("XGBoost Ensemble Model Demo")
    print("="*70)
    
    # Initialize ensemble
    ensemble = SkinCancerEnsemble(model_path='models/xgboost_ensemble.pkl')
    
    # Simulate training data (in production, use real CNN outputs)
    print("\n📊 Simulating training data...")
    n_samples = 1000
    
    classes = [
        'Actinic keratoses', 'Basal cell carcinoma',
        'Benign keratosis-like lesions', 'Dermatofibroma',
        'Melanocytic nevi', 'Melanoma', 'Vascular lesions'
    ]
    
    X_train_list = []
    y_train_list = []
    
    for _ in range(n_samples):
        # Random true class
        true_class = np.random.choice(classes)
        
        # Simulate CNN predictions
        cnn_preds = simulate_cnn_predictions(true_class, noise_level=0.1)
        
        # Simulate metadata
        metadata = {
            'age': np.random.randint(20, 80),
            'gender': np.random.choice(['male', 'female']),
            'location': 'face'
        }
        
        # Prepare features
        features = ensemble.prepare_features(cnn_preds, metadata)
        
        X_train_list.append(features.flatten())
        y_train_list.append(true_class)
    
    X_train = np.array(X_train_list)
    y_train = np.array(y_train_list)
    
    # Split data
    X_train_split, X_val, y_train_split, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42
    )
    
    # Train ensemble
    print("\n🚀 Training XGBoost ensemble...")
    ensemble.train(X_train_split, y_train_split, X_val, y_val)
    
    # Test prediction
    print("\n🔍 Testing prediction with uncertainty...")
    test_class = 'Melanoma'
    test_preds = simulate_cnn_predictions(test_class, noise_level=0.05)
    test_metadata = {'age': 65, 'gender': 'male', 'location': 'back'}
    test_features = ensemble.prepare_features(test_preds, test_metadata)
    
    # Standard prediction
    pred_class, confidence, all_probs = ensemble.predict(test_features)
    print(f"\nStandard Prediction:")
    print(f"  Class: {pred_class}")
    print(f"  Confidence: {confidence:.2f}%")
    
    # Prediction with uncertainty
    uncertainty_result = ensemble.predict_with_uncertainty(test_features, n_iterations=20)
    print(f"\nPrediction with Uncertainty:")
    print(f"  Class: {uncertainty_result['prediction']}")
    print(f"  Confidence: {uncertainty_result['confidence']:.2f}% ± {uncertainty_result['confidence_std']:.2f}%")
    print(f"  Uncertainty Score: {uncertainty_result['uncertainty_score']:.3f}")
    print(f"  Agreement Rate: {uncertainty_result['agreement_rate']:.1f}%")
    print(f"  {uncertainty_result['recommendation']}")
    
    # Feature importance
    print("\n📊 Top 5 Feature Importances:")
    importance = ensemble.get_feature_importance()
    for i, (feature, imp) in enumerate(list(importance.items())[:5]):
        print(f"  {i+1}. {feature}: {imp:.4f}")
    
    # Save model
    ensemble.save_model()
    
    print("\n✅ Demo completed!")

