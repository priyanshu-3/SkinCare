"""
Demo: XGBoost Ensemble + XAI Integration
Shows how the complete system works with ensemble predictions and explainability
"""

import os
import numpy as np
from ensemble_model import SkinCancerEnsemble, simulate_cnn_predictions
from explainability import SkinCancerExplainer


def run_ensemble():
    """
    Demonstrate XGBoost Ensemble with uncertainty estimation
    """
    print("="*70)
    print("🚀 XGBoost Ensemble Demo")
    print("="*70)
    
    # Initialize ensemble
    ensemble = SkinCancerEnsemble(model_path='models/xgboost_ensemble.pkl')
    
    # Check if model is trained
    if not ensemble.is_trained:
        print("\n⚠️ Model not trained yet. Training with simulated data...")
        print("(In production, train on real CNN outputs)")
        
        # Generate training data
        n_samples = 500
        classes = [
            'Actinic keratoses', 'Basal cell carcinoma',
            'Benign keratosis-like lesions', 'Dermatofibroma',
            'Melanocytic nevi', 'Melanoma', 'Vascular lesions'
        ]
        
        X_train = []
        y_train = []
        
        for _ in range(n_samples):
            true_class = np.random.choice(classes)
            cnn_preds = simulate_cnn_predictions(true_class, noise_level=0.1)
            metadata = {
                'age': np.random.randint(20, 80),
                'gender': np.random.choice(['male', 'female']),
                'location': 'face'
            }
            features = ensemble.prepare_features(cnn_preds, metadata)
            X_train.append(features.flatten())
            y_train.append(true_class)
        
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        # Train
        ensemble.train(X_train, y_train)
        ensemble.save_model()
    
    # Test prediction
    print("\n" + "="*70)
    print("📊 Testing Prediction with Uncertainty")
    print("="*70)
    
    # Simulate a test case
    test_case = {
        'true_class': 'Melanoma',
        'age': 65,
        'gender': 'male',
        'location': 'back'
    }
    
    print(f"\n🔬 Test Case:")
    print(f"   True Class: {test_case['true_class']}")
    print(f"   Patient: {test_case['age']}yo {test_case['gender']}")
    print(f"   Location: {test_case['location']}")
    
    # Simulate CNN predictions
    cnn_preds = simulate_cnn_predictions(test_case['true_class'], noise_level=0.05)
    
    print(f"\n📈 Simulated CNN Predictions:")
    for model_name, preds in cnn_preds.items():
        top_pred = max(preds.items(), key=lambda x: x[1])
        print(f"   {model_name}: {top_pred[0]} ({top_pred[1]*100:.1f}%)")
    
    # Prepare features
    metadata = {
        'age': test_case['age'],
        'gender': test_case['gender'],
        'location': test_case['location']
    }
    features = ensemble.prepare_features(cnn_preds, metadata)
    
    # Standard prediction
    pred_class, confidence, all_probs = ensemble.predict(features)
    
    print(f"\n🎯 Standard Ensemble Prediction:")
    print(f"   Class: {pred_class}")
    print(f"   Confidence: {confidence:.2f}%")
    
    # Prediction with uncertainty
    uncertainty = ensemble.predict_with_uncertainty(features, n_iterations=20)
    
    print(f"\n🔍 Prediction with Uncertainty Estimation:")
    print(f"   Class: {uncertainty['prediction']}")
    print(f"   Confidence: {uncertainty['confidence']:.2f}% ± {uncertainty['confidence_std']:.2f}%")
    print(f"   Uncertainty Score: {uncertainty['uncertainty_score']:.3f}")
    print(f"   Agreement Rate: {uncertainty['agreement_rate']:.1f}%")
    print(f"   {uncertainty['recommendation']}")
    
    # Feature importance
    print(f"\n📊 Top 5 Most Important Features:")
    importance = ensemble.get_feature_importance()
    for i, (feature, imp) in enumerate(list(importance.items())[:5]):
        print(f"   {i+1}. {feature}: {imp:.4f}")
    
    return ensemble


def run_explainability():
    """
    Demonstrate XAI (Explainability) features
    """
    print("\n" + "="*70)
    print("🔍 XAI (Explainability) Demo")
    print("="*70)
    
    # Initialize explainer
    explainer = SkinCancerExplainer()
    
    # Find a test image
    test_images = [
        "static/uploads/captured.jpg",
        "static/uploads/Screenshot_2025-10-05_082319.png"
    ]
    
    test_image = None
    for img_path in test_images:
        if os.path.exists(img_path):
            test_image = img_path
            break
    
    if not test_image:
        print("\n⚠️ No test images found. Upload an image first.")
        print("   Expected locations:")
        for img in test_images:
            print(f"   - {img}")
        return None
    
    print(f"\n📸 Using test image: {test_image}")
    
    # Generate saliency map (always works)
    print("\n🔍 Generating saliency map...")
    os.makedirs('explanations', exist_ok=True)
    saliency = explainer.generate_saliency_map(
        test_image,
        save_path='explanations/saliency_demo.png'
    )
    
    # Try LIME explanation
    print("\n🔍 Attempting LIME explanation...")
    
    def dummy_predict_fn(images):
        """Dummy prediction function for demo"""
        batch_size = len(images)
        num_classes = 7
        probs = np.random.dirichlet(np.ones(num_classes), size=batch_size)
        return probs
    
    lime_result = explainer.explain_with_lime(
        test_image,
        dummy_predict_fn,
        num_samples=100,  # Reduced for faster demo
        save_path='explanations/lime_demo.png'
    )
    
    if lime_result:
        print("✅ LIME explanation generated")
        print(f"   Top class: {lime_result['top_class']}")
        print(f"   Explanation saved to: {lime_result['visualization_path']}")
    else:
        print("ℹ️ LIME not available. Install with: pip install lime")
    
    print("\n✅ Explainability demo completed!")
    print(f"📁 Check 'explanations/' folder for visualizations")
    
    return explainer


def run_integration():
    """
    Demonstrate full integration of Ensemble + XAI
    """
    print("\n" + "="*70)
    print("🎉 Full System Integration Demo")
    print("="*70)
    
    print("\n📌 This shows how all components work together:")
    print("   1. Multiple CNN predictions")
    print("   2. Patient metadata")
    print("   3. XGBoost ensemble")
    print("   4. Uncertainty estimation")
    print("   5. Explainability (LIME/SHAP/Saliency)")
    
    # Simulate a complete analysis
    patient = {
        'name': 'John Doe',
        'age': 58,
        'gender': 'male',
        'location': 'shoulder'
    }
    
    print(f"\n👤 Patient Information:")
    print(f"   Name: {patient['name']}")
    print(f"   Age: {patient['age']}")
    print(f"   Gender: {patient['gender']}")
    print(f"   Lesion Location: {patient['location']}")
    
    # Step 1: CNN Predictions
    print(f"\n🔬 Step 1: Multiple CNN Model Predictions")
    suspected_class = 'Melanoma'
    cnn_preds = simulate_cnn_predictions(suspected_class, noise_level=0.08)
    
    for model_name, preds in cnn_preds.items():
        top_pred = max(preds.items(), key=lambda x: x[1])
        print(f"   {model_name}: {top_pred[0]} ({top_pred[1]*100:.1f}%)")
    
    # Step 2: Ensemble Prediction
    print(f"\n🎯 Step 2: XGBoost Ensemble with Uncertainty")
    
    ensemble = SkinCancerEnsemble(model_path='models/xgboost_ensemble.pkl')
    
    if ensemble.is_trained:
        metadata = {
            'age': patient['age'],
            'gender': patient['gender'],
            'location': patient['location']
        }
        
        features = ensemble.prepare_features(cnn_preds, metadata)
        uncertainty = ensemble.predict_with_uncertainty(features, n_iterations=20)
        
        print(f"   Final Prediction: {uncertainty['prediction']}")
        print(f"   Confidence: {uncertainty['confidence']:.1f}% ± {uncertainty['confidence_std']:.1f}%")
        print(f"   Uncertainty: {uncertainty['uncertainty_score']:.3f}")
        print(f"   {uncertainty['recommendation']}")
    else:
        print("   ⚠️ Ensemble not trained. Train first with ensemble_model.py")
    
    # Step 3: Explainability
    print(f"\n🔍 Step 3: Explainability Analysis")
    print("   ✅ Saliency map: Shows important regions")
    print("   ✅ LIME: Local interpretable explanations")
    print("   ✅ SHAP: Feature importance")
    print("   (See run_explainability() for actual generation)")
    
    # Step 4: Clinical Decision Support
    print(f"\n🏥 Step 4: Clinical Decision Support")
    print("   Based on the analysis:")
    
    if ensemble.is_trained and uncertainty['uncertainty_score'] > 0.2:
        print("   ⚠️ HIGH UNCERTAINTY DETECTED")
        print("   Recommendation: Immediate dermatologist consultation")
        print("   Priority: HIGH")
    elif ensemble.is_trained and uncertainty['prediction'] in ['Melanoma', 'Basal cell carcinoma']:
        print("   ⚠️ HIGH RISK CONDITION DETECTED")
        print("   Recommendation: Schedule dermatologist appointment within 1 week")
        print("   Priority: HIGH")
    else:
        print("   ✅ Standard monitoring recommended")
        print("   Follow-up: 3-6 months")
    
    print("\n" + "="*70)
    print("✅ Complete System Demo Finished!")
    print("="*70)


def main():
    """
    Main demo function
    """
    print("\n")
    print("┌" + "─"*68 + "┐")
    print("│" + " "*15 + "XGBoost + XAI Integration Demo" + " "*23 + "│")
    print("│" + " "*15 + "Skin Cancer Detection System" + " "*24 + "│")
    print("└" + "─"*68 + "┘")
    
    # Menu
    while True:
        print("\n" + "="*70)
        print("Select Demo:")
        print("="*70)
        print("1. XGBoost Ensemble Demo")
        print("2. XAI (Explainability) Demo")
        print("3. Full System Integration Demo")
        print("4. Run All Demos")
        print("5. Exit")
        print("="*70)
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            run_ensemble()
        elif choice == '2':
            run_explainability()
        elif choice == '3':
            run_integration()
        elif choice == '4':
            run_ensemble()
            run_explainability()
            run_integration()
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()

