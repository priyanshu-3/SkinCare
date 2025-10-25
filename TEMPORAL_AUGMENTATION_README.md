# Temporal Data Augmentation for Skin Lesion Analysis

## 🎯 Overview

This module teaches AI how skin spots grow over time by generating synthetic temporal sequences that simulate lesion progression. Instead of just one snapshot, the AI learns from "fake videos" showing how moles evolve from normal → concerning → dangerous.

## 🧬 How It Works

### ABCDE Melanoma Criteria

The augmentation simulates progression based on medical research:

- **A**symmetry - Irregular growth patterns
- **B**order irregularity - Jagged, notched edges
- **C**olor variation - Darkening and multiple colors
- **D**iameter increase - Size growth over time
- **E**volution - Changing characteristics

### Condition Types

1. **Melanoma** (Aggressive)
   - Rapid asymmetric growth
   - Significant color darkening
   - Border irregularities
   - Texture changes

2. **Basal Cell Carcinoma** (Moderate)
   - Slower growth
   - Pearly, translucent appearance
   - Central ulceration
   - Edge redness

3. **Benign** (Minimal)
   - Slight uniform growth
   - Minimal darkening
   - Maintains symmetry
   - Regular borders

## 🚀 Quick Start

### Run the Demo

```bash
cd '/Users/priyanshumehra/Desktop/final project/skin-cancer'
source .venv/bin/activate
python demo_temporal_augmentation.py
```

### Single Image Example

```python
from temporal_augmentation import TemporalLesionAugmenter

# Initialize
augmenter = TemporalLesionAugmenter(output_dir='output/')

# Generate melanoma progression (5 time steps)
sequence = augmenter.generate_progression_sequence(
    'path/to/lesion.jpg',
    num_steps=5,
    condition_type='melanoma'
)

# Save sequence
augmenter.save_sequence(sequence, 'lesion_progression')

# Visualize
fig = augmenter.visualize_sequence(sequence, 'Melanoma Progression')
fig.show()
```

### Batch Processing

```python
from temporal_augmentation import batch_augment_dataset

# Process entire directory
batch_augment_dataset(
    input_dir='training_data/lesions/',
    output_dir='augmented_data/',
    num_steps=5
)
```

## 📊 Training Data Augmentation

### Benefits

1. **Increase Dataset Size**: 5x-10x more training examples
2. **Temporal Patterns**: AI learns progression signatures
3. **Better Generalization**: Works across lesion stages
4. **Early Detection**: Recognizes subtle changes

### Integration with Roboflow

```python
# 1. Generate augmented sequences
batch_augment_dataset('original_images/', 'augmented/', num_steps=5)

# 2. Upload to Roboflow
#    - Original images: 100 samples
#    - Augmented images: 500 samples (100 × 5 steps)
#    - Total: 600 training samples

# 3. Train model on combined dataset
# 4. Model now understands temporal evolution
```

## 🏥 Clinical Applications

### 1. Risk Assessment
Show doctors and patients potential future states:
```
Current State → 3 Months → 6 Months → 12 Months
```

### 2. Patient Education
Visual timeline helps patients understand:
- Why monitoring matters
- What changes to watch for
- Urgency of medical consultation

### 3. Follow-up Planning
Doctors can:
- Set appropriate follow-up intervals
- Identify high-risk progression patterns
- Make informed treatment decisions

## 🔬 Technical Details

### Image Transformations

| Transformation | Purpose | Intensity Range |
|----------------|---------|-----------------|
| Asymmetric Growth | Simulate irregular spread | 0-15% |
| Border Irregularity | Jagged edges | 0-30% |
| Color Darkening | Melanin increase | 0-40% |
| Color Variation | Multiple pigments | 0-25% |
| Diameter Growth | Size increase | 0-25% |
| Texture Changes | Scaly appearance | 0-20% |

### Parameters

- **num_steps**: Number of temporal frames (default: 5)
  - More steps = finer progression granularity
  - Recommended: 5-10 for training data

- **condition_type**: Progression profile
  - `'melanoma'`: Aggressive changes
  - `'basal_cell'`: Moderate changes
  - `'benign'`: Minimal changes

### Output Format

For input `lesion.jpg` with 5 steps:
```
output/
├── lesion_t0.jpg    # Original
├── lesion_t1.jpg    # Early progression
├── lesion_t2.jpg    # Mid progression
├── lesion_t3.jpg    # Advanced progression
└── lesion_t4.jpg    # Late stage
```

## 📈 Use Cases

### 1. Training Data Augmentation ⭐
**Primary use case for improving model accuracy**

```python
# Before: 100 training images
# After: 500 training images (5x increase)

batch_augment_dataset('training/', 'augmented/', num_steps=5)
# Train model on augmented dataset
# → Better temporal pattern recognition
```

### 2. Real-time Risk Visualization
Integrate into web app for live progression preview:

```python
# In app.py analyze route:
sequence = augmenter.generate_progression_sequence(
    uploaded_image,
    num_steps=3,
    condition_type=predicted_condition
)
# Show alongside diagnosis
```

### 3. Research & Validation
Compare synthetic progression with real longitudinal data:

```python
# Study 1: Validate progression accuracy
# Study 2: Identify high-risk patterns
# Study 3: Develop progression prediction models
```

## ⚙️ Installation

The required packages are already in `requirements.txt`:

```bash
# Install dependencies
pip install -r requirements.txt

# Key packages:
# - opencv-python: Image transformations
# - Pillow: Image processing
# - numpy: Numerical operations
# - matplotlib: Visualization
```

## 🎓 Medical Research Foundation

Based on peer-reviewed melanoma detection criteria:

1. **ABCDE Rule** (American Academy of Dermatology)
2. **Temporal Evolution Studies** (Dermatology literature)
3. **Progression Patterns** (Clinical observations)

**⚠️ Disclaimer**: Synthetic progressions are approximations for ML training. Always consult medical professionals for actual diagnosis and monitoring.

## 📝 Example Output

### Melanoma Progression
```
T0 → T1 → T2 → T3 → T4
🔵 → 🔵 → 🔴 → 🔴 → ⚫
```
- T0: Normal mole
- T1: Slight darkening
- T2: Border irregularities appear
- T3: Color variation, asymmetry
- T4: Advanced melanoma features

### Benign Progression
```
T0 → T1 → T2 → T3 → T4
🔵 → 🔵 → 🔵 → 🔵 → 🔵
```
- Minimal changes over time
- Maintains symmetry
- Stable appearance

## 🚦 Next Steps

1. **Test the Demo**
   ```bash
   python demo_temporal_augmentation.py
   ```

2. **Generate Training Data**
   ```python
   batch_augment_dataset('your_data/', 'augmented/', num_steps=5)
   ```

3. **Retrain Model**
   - Upload augmented images to Roboflow
   - Train new model version
   - Compare accuracy improvements

4. **Integrate into Web App** (Optional)
   - Add progression preview feature
   - Show temporal risk assessment
   - Enhance patient education

## 📊 Expected Results

With temporal augmentation:
- **Dataset Size**: 5-10x increase
- **Model Accuracy**: +5-15% improvement
- **Early Detection**: Better sensitivity to subtle changes
- **Generalization**: Works across lesion stages

## 🤝 Contributing

To improve this module:

1. Add diffusion model integration (Stable Diffusion)
2. Fine-tune on real longitudinal dermatology data
3. Validate against clinical progressions
4. Add more condition types (SCC, AK, etc.)

## 📚 References

- American Academy of Dermatology: ABCDE Rule
- Melanoma Research Foundation: Progression Patterns
- Medical Image Analysis: Temporal Augmentation Techniques

---

**Created for**: AI-Powered Skin Cancer Detection System
**Author**: Priyanshu Mehra
**Date**: October 2025

