"""
Demo script for temporal augmentation
Run this to test the temporal progression feature
"""

import os
from temporal_augmentation import TemporalLesionAugmenter, batch_augment_dataset
import matplotlib.pyplot as plt

def demo_single_image():
    """Demo: Generate progression for a single image"""
    print("=" * 70)
    print("DEMO: Single Image Temporal Progression")
    print("=" * 70)
    
    # Initialize augmenter
    augmenter = TemporalLesionAugmenter(output_dir='demo_output/temporal')
    
    # Find a test image from uploads
    test_images = []
    if os.path.exists('static/uploads'):
        for file in os.listdir('static/uploads'):
            if file.endswith(('.jpg', '.jpeg', '.png')) and not file.startswith('viz_'):
                test_images.append(os.path.join('static/uploads', file))
    
    if not test_images:
        print("\n❌ No test images found in static/uploads/")
        print("Please upload an image through the web interface first.")
        return
    
    test_image = test_images[0]
    print(f"\nUsing test image: {test_image}")
    
    # Test all three condition types
    conditions = ['melanoma', 'basal_cell', 'benign']
    
    for condition in conditions:
        print(f"\n{'='*60}")
        print(f"Generating {condition.upper()} progression...")
        print(f"{'='*60}")
        
        # Generate sequence
        sequence = augmenter.generate_progression_sequence(
            test_image,
            num_steps=5,
            condition_type=condition
        )
        
        # Save sequence
        base_name = f"demo_{condition}"
        saved_paths = augmenter.save_sequence(sequence, base_name)
        
        # Visualize
        fig = augmenter.visualize_sequence(
            sequence,
            f"{condition.replace('_', ' ').title()} Progression Over Time"
        )
        
        viz_path = f'demo_output/temporal/{base_name}_visualization.png'
        fig.savefig(viz_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved: {viz_path}")
        plt.close(fig)
    
    print("\n" + "="*70)
    print("✅ Demo complete! Check demo_output/temporal/ for results")
    print("="*70)


def demo_batch_processing():
    """Demo: Batch process multiple images"""
    print("\n" + "=" * 70)
    print("DEMO: Batch Processing")
    print("=" * 70)
    
    input_dir = 'static/uploads'
    output_dir = 'demo_output/batch_temporal'
    
    if not os.path.exists(input_dir):
        print(f"\n❌ Input directory not found: {input_dir}")
        return
    
    # Count images
    image_count = len([f for f in os.listdir(input_dir) 
                      if f.endswith(('.jpg', '.jpeg', '.png')) 
                      and not f.startswith('viz_')])
    
    if image_count == 0:
        print(f"\n❌ No images found in {input_dir}")
        return
    
    print(f"\nFound {image_count} images to process")
    print(f"Generating 5 temporal steps for each image...")
    print(f"Output directory: {output_dir}\n")
    
    # Batch process
    batch_augment_dataset(input_dir, output_dir, num_steps=5)
    
    print("\n✅ Batch processing complete!")


def show_use_cases():
    """Display use cases for temporal augmentation"""
    print("\n" + "=" * 70)
    print("USE CASES FOR TEMPORAL AUGMENTATION")
    print("=" * 70)
    
    use_cases = """
    1. **Training Data Augmentation**
       - Increase dataset size by 5x-10x
       - Teach AI to recognize progression patterns
       - Better generalization across lesion stages
    
    2. **Risk Assessment**
       - Show patients potential future states
       - Help doctors explain progression risks
       - Visual timeline for follow-up planning
    
    3. **Early Detection Training**
       - AI learns subtle early-stage changes
       - Recognizes dangerous progression patterns
       - Improves sensitivity to evolving lesions
    
    4. **Patient Education**
       - Visual explanation of "what to watch for"
       - Understanding urgency of medical consultation
       - Demonstrating importance of monitoring
    
    5. **Research Applications**
       - Study temporal patterns in skin cancer
       - Validate against longitudinal patient data
       - Develop progression prediction models
    """
    
    print(use_cases)
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    
    next_steps = """
    To integrate with your training pipeline:
    
    1. Collect training images in a directory
    2. Run batch augmentation:
       ```python
       from temporal_augmentation import batch_augment_dataset
       batch_augment_dataset('training_data/', 'augmented_data/', num_steps=5)
       ```
    
    3. Train your model with both original and augmented images
    4. The model learns temporal patterns automatically
    
    For real-time feature in the web app:
    - Call augmenter during analysis
    - Show "potential progression" alongside current diagnosis
    - Help doctors visualize future risk
    """
    
    print(next_steps)


if __name__ == "__main__":
    print("\n" + "🔬" * 35)
    print("TEMPORAL LESION AUGMENTATION - DEMO")
    print("🔬" * 35 + "\n")
    
    print("This tool simulates how skin lesions evolve over time")
    print("Based on medical research (ABCDE melanoma criteria)")
    print("\nSelect demo mode:")
    print("1. Single image demonstration (all condition types)")
    print("2. Batch process all uploaded images")
    print("3. Show use cases and next steps")
    print("4. Run all demos")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            demo_single_image()
        elif choice == '2':
            demo_batch_processing()
        elif choice == '3':
            show_use_cases()
        elif choice == '4':
            demo_single_image()
            demo_batch_processing()
            show_use_cases()
        else:
            print("\n❌ Invalid choice. Running single image demo...")
            demo_single_image()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have images in static/uploads/ directory")

