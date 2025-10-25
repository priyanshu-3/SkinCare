"""
Temporal Data Augmentation for Skin Lesion Analysis
Simulates how skin lesions progress over time using image transformations
Based on ABCDE melanoma detection criteria
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
from pathlib import Path


class TemporalLesionAugmenter:
    """
    Generates synthetic temporal sequences showing lesion progression
    Simulates: Asymmetry, Border irregularity, Color changes, Diameter growth, Evolution
    """
    
    def __init__(self, output_dir='augmented_temporal'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_progression_sequence(self, image_path, num_steps=5, condition_type='melanoma'):
        """
        Generate a temporal sequence showing lesion progression
        
        Args:
            image_path: Path to input lesion image
            num_steps: Number of time steps to generate (default: 5)
            condition_type: Type of condition ('melanoma', 'benign', 'basal_cell')
        
        Returns:
            List of augmented images representing progression over time
        """
        # Load image
        img = Image.open(image_path).convert('RGB')
        original_size = img.size
        
        # Generate progression sequence
        sequence = [img]  # T0: Original image
        
        if condition_type == 'melanoma':
            # Melanoma progression: aggressive changes
            sequence.extend(self._generate_melanoma_progression(img, num_steps - 1))
        elif condition_type == 'basal_cell':
            # Basal cell carcinoma: slower, pearly changes
            sequence.extend(self._generate_basal_cell_progression(img, num_steps - 1))
        else:
            # Benign: minimal changes
            sequence.extend(self._generate_benign_progression(img, num_steps - 1))
        
        return sequence
    
    def _generate_melanoma_progression(self, img, steps):
        """Simulate melanoma progression (ABCDE criteria)"""
        sequence = []
        
        for step in range(1, steps + 1):
            intensity = step / steps  # 0.2, 0.4, 0.6, 0.8, 1.0
            
            augmented = img.copy()
            
            # A: Asymmetry - gradual irregular growth
            augmented = self._apply_asymmetric_growth(augmented, intensity * 0.15)
            
            # B: Border irregularity - jagged edges
            augmented = self._apply_border_irregularity(augmented, intensity * 0.3)
            
            # C: Color variation - darkening and variegation
            augmented = self._apply_color_darkening(augmented, intensity * 0.4)
            augmented = self._apply_color_variation(augmented, intensity * 0.25)
            
            # D: Diameter increase
            augmented = self._apply_diameter_growth(augmented, 1 + intensity * 0.25)
            
            # E: Evolution - texture changes
            augmented = self._apply_texture_changes(augmented, intensity * 0.2)
            
            sequence.append(augmented)
        
        return sequence
    
    def _generate_basal_cell_progression(self, img, steps):
        """Simulate basal cell carcinoma progression (slower, pearly appearance)"""
        sequence = []
        
        for step in range(1, steps + 1):
            intensity = step / steps
            
            augmented = img.copy()
            
            # Subtle size increase
            augmented = self._apply_diameter_growth(augmented, 1 + intensity * 0.15)
            
            # Pearly, translucent appearance
            augmented = self._apply_pearly_effect(augmented, intensity * 0.3)
            
            # Central ulceration development
            augmented = self._apply_central_depression(augmented, intensity * 0.2)
            
            # Slight redness at edges
            augmented = self._apply_edge_redness(augmented, intensity * 0.25)
            
            sequence.append(augmented)
        
        return sequence
    
    def _generate_benign_progression(self, img, steps):
        """Simulate benign lesion (minimal changes)"""
        sequence = []
        
        for step in range(1, steps + 1):
            intensity = step / steps * 0.5  # Much slower changes
            
            augmented = img.copy()
            
            # Minimal uniform growth
            augmented = self._apply_diameter_growth(augmented, 1 + intensity * 0.08)
            
            # Slight darkening
            augmented = self._apply_color_darkening(augmented, intensity * 0.15)
            
            # Maintain symmetry and regular borders
            augmented = ImageEnhance.Sharpness(augmented).enhance(1 + intensity * 0.1)
            
            sequence.append(augmented)
        
        return sequence
    
    # === Transformation Functions ===
    
    def _apply_asymmetric_growth(self, img, intensity):
        """Create asymmetric growth pattern"""
        width, height = img.size
        img_array = np.array(img)
        
        # Create asymmetric scaling map
        y_scale = 1 + intensity * np.random.uniform(0.5, 1.5)
        x_scale = 1 + intensity * np.random.uniform(0.5, 1.5)
        
        # Apply non-uniform scaling
        new_height = int(height * y_scale)
        new_width = int(width * x_scale)
        
        img_resized = cv2.resize(img_array, (new_width, new_height))
        
        # Crop or pad to original size
        if new_height > height or new_width > width:
            start_y = (new_height - height) // 2
            start_x = (new_width - width) // 2
            img_array = img_resized[start_y:start_y+height, start_x:start_x+width]
        else:
            pad_y = (height - new_height) // 2
            pad_x = (width - new_width) // 2
            img_array = np.pad(img_resized, 
                             ((pad_y, height-new_height-pad_y), 
                              (pad_x, width-new_width-pad_x), 
                              (0, 0)), mode='edge')
        
        return Image.fromarray(img_array)
    
    def _apply_border_irregularity(self, img, intensity):
        """Create irregular, jagged borders"""
        if intensity < 0.1:
            return img
        
        # Apply erosion and dilation with random structuring elements
        img_array = np.array(img)
        kernel_size = max(3, int(intensity * 7))
        
        # Random irregular kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        
        # Slight morphological operations on edges
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # Blend edges back
        mask = dilated.astype(float) / 255.0 * intensity
        mask = np.stack([mask]*3, axis=-1)
        
        result = img_array.astype(float) * (1 - mask * 0.3) + mask * 50
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    def _apply_color_darkening(self, img, intensity):
        """Darken the lesion"""
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(1 - intensity * 0.4)
    
    def _apply_color_variation(self, img, intensity):
        """Add color variegation (multiple colors)"""
        img_array = np.array(img).astype(float)
        height, width = img_array.shape[:2]
        
        # Create random color patches
        num_patches = int(intensity * 5)
        for _ in range(num_patches):
            # Random patch location
            center_y = np.random.randint(height // 4, 3 * height // 4)
            center_x = np.random.randint(width // 4, 3 * width // 4)
            radius = np.random.randint(width // 10, width // 4)
            
            # Random color shift
            color_shift = np.random.uniform(-30, 30, 3)
            
            # Create circular mask
            y, x = np.ogrid[:height, :width]
            mask = ((x - center_x)**2 + (y - center_y)**2 <= radius**2).astype(float)
            mask = cv2.GaussianBlur(mask, (21, 21), 0)
            mask = np.stack([mask]*3, axis=-1)
            
            # Apply color shift
            img_array += mask * color_shift * intensity
        
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)
    
    def _apply_diameter_growth(self, img, scale_factor):
        """Increase lesion size"""
        width, height = img.size
        new_size = (int(width * scale_factor), int(height * scale_factor))
        resized = img.resize(new_size, Image.LANCZOS)
        
        # Center crop to original size
        left = (new_size[0] - width) // 2
        top = (new_size[1] - height) // 2
        return resized.crop((left, top, left + width, top + height))
    
    def _apply_texture_changes(self, img, intensity):
        """Add texture changes (rough, scaly appearance)"""
        if intensity < 0.1:
            return img
        
        # Add noise to simulate texture
        img_array = np.array(img).astype(float)
        noise = np.random.normal(0, intensity * 15, img_array.shape)
        img_array += noise
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        
        # Slight unsharp mask for texture
        img_pil = Image.fromarray(img_array)
        img_pil = img_pil.filter(ImageFilter.UnsharpMask(radius=2, percent=int(intensity * 150)))
        
        return img_pil
    
    def _apply_pearly_effect(self, img, intensity):
        """Create pearly, translucent appearance for basal cell"""
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1 - intensity * 0.3)
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1 + intensity * 0.2)
        
        return img
    
    def _apply_central_depression(self, img, intensity):
        """Create central ulceration/depression"""
        if intensity < 0.3:
            return img
        
        img_array = np.array(img).astype(float)
        height, width = img_array.shape[:2]
        
        # Create radial gradient (darker in center)
        y, x = np.ogrid[:height, :width]
        center_y, center_x = height // 2, width // 2
        radius = min(width, height) // 4
        
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        mask = np.maximum(0, 1 - dist / radius)
        mask = np.stack([mask]*3, axis=-1)
        
        # Darken center
        img_array = img_array * (1 - mask * intensity * 0.5)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    def _apply_edge_redness(self, img, intensity):
        """Add redness at edges"""
        img_array = np.array(img).astype(float)
        height, width = img_array.shape[:2]
        
        # Create edge mask
        y, x = np.ogrid[:height, :width]
        center_y, center_x = height // 2, width // 2
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        inner_radius = min(width, height) // 4
        outer_radius = min(width, height) // 3
        
        mask = np.zeros((height, width))
        mask[(dist >= inner_radius) & (dist <= outer_radius)] = 1
        mask = cv2.GaussianBlur(mask, (15, 15), 0)
        
        # Add red tint
        img_array[:, :, 0] += mask * intensity * 30  # Red channel
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    def save_sequence(self, sequence, base_name, output_dir=None):
        """Save temporal sequence to disk"""
        if output_dir is None:
            output_dir = self.output_dir
        
        os.makedirs(output_dir, exist_ok=True)
        saved_paths = []
        
        for idx, img in enumerate(sequence):
            filename = f"{base_name}_t{idx}.jpg"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath, quality=95)
            saved_paths.append(filepath)
            print(f"Saved: {filepath}")
        
        return saved_paths
    
    def visualize_sequence(self, sequence, title="Lesion Progression Over Time"):
        """Visualize the temporal sequence"""
        num_images = len(sequence)
        fig, axes = plt.subplots(1, num_images, figsize=(4 * num_images, 4))
        
        if num_images == 1:
            axes = [axes]
        
        for idx, (ax, img) in enumerate(zip(axes, sequence)):
            ax.imshow(img)
            ax.axis('off')
            ax.set_title(f'T{idx}', fontsize=14, fontweight='bold')
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig


def batch_augment_dataset(input_dir, output_dir, num_steps=5):
    """
    Batch process a directory of lesion images to create temporal augmentations
    
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save augmented sequences
        num_steps: Number of temporal steps per image
    """
    augmenter = TemporalLesionAugmenter(output_dir)
    
    # Supported image formats
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    image_files = []
    for ext in image_extensions:
        image_files.extend(Path(input_dir).glob(f'*{ext}'))
        image_files.extend(Path(input_dir).glob(f'*{ext.upper()}'))
    
    print(f"Found {len(image_files)} images in {input_dir}")
    
    for img_path in image_files:
        print(f"\nProcessing: {img_path.name}")
        
        # Infer condition type from filename (you can customize this logic)
        filename_lower = img_path.name.lower()
        if 'melanoma' in filename_lower:
            condition = 'melanoma'
        elif 'basal' in filename_lower or 'bcc' in filename_lower:
            condition = 'basal_cell'
        else:
            condition = 'benign'
        
        # Generate progression sequence
        sequence = augmenter.generate_progression_sequence(
            str(img_path), 
            num_steps=num_steps, 
            condition_type=condition
        )
        
        # Save sequence
        base_name = img_path.stem
        saved_paths = augmenter.save_sequence(sequence, base_name, output_dir)
        
        # Optionally visualize
        # fig = augmenter.visualize_sequence(sequence, f"Progression: {base_name}")
        # fig.savefig(os.path.join(output_dir, f"{base_name}_sequence.png"), dpi=150)
        # plt.close(fig)
    
    print(f"\nAugmentation complete! Generated {len(image_files) * num_steps} new images.")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    # Example usage
    print("=" * 70)
    print("Temporal Lesion Augmentation Pipeline")
    print("=" * 70)
    
    # Example: Process a single image
    augmenter = TemporalLesionAugmenter(output_dir='augmented_temporal')
    
    # You can test with an existing uploaded image
    test_image = "static/uploads/images.jpeg"  # Change to your test image
    
    if os.path.exists(test_image):
        print(f"\nGenerating progression sequence for: {test_image}")
        
        # Generate melanoma progression
        sequence = augmenter.generate_progression_sequence(
            test_image, 
            num_steps=5, 
            condition_type='melanoma'
        )
        
        # Save and visualize
        augmenter.save_sequence(sequence, "example_melanoma")
        fig = augmenter.visualize_sequence(sequence, "Melanoma Progression Example")
        fig.savefig('augmented_temporal/example_progression.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print("\n✅ Example progression generated successfully!")
    else:
        print(f"\nTest image not found: {test_image}")
        print("Please update the path to an existing lesion image.")
    
    # Uncomment to batch process a directory:
    # batch_augment_dataset('training_data/lesions/', 'augmented_temporal/', num_steps=5)

