# Feature Engineering Architecture

**Date**: 2026-07-13  
**Module**: `backend/ml/feature_engineering/`  
**Purpose**: Transform raw maternal health data into ML-ready feature vectors

---

## Overview

This module implements a **layered feature engineering pipeline** following production ML best practices. Each layer is independently testable, modular, and designed for maintainability.

The pipeline follows the principle that **feature quality matters more than model choice** - a well-engineered feature set with a simple model beats poorly engineered features with a complex model.

---

## Architecture

```
Raw Patient Data (CSV or API input)
         ↓
┌─────────────────────────────────┐
│  LAYER 1: validators.py         │  ← Reject invalid inputs
│  Validate realistic ranges      │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  LAYER 2: calculators.py        │  ← Pure math functions
│  Derive numerical features      │
│  BMI, MAP, Pulse Pressure, etc. │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  LAYER 3: transformers.py       │  ← Convert to categories
│  Clinically meaningful groups   │
│  "Obese" vs 32.8               │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  LAYER 4: encoders.py           │  ← Convert to numeric codes
│  ML-friendly numeric codes      │
│  0=Underweight, 1=Normal, etc.  │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  LAYER 5: feature_pipeline.py   │  ← Single orchestration entry
│  Coordinate all layers          │
│  Return engineered DataFrame    │
└─────────────────────────────────┘
         ↓
   ML-Ready Feature Vector
```

---

## Modules

### 1. `calculators.py` — Pure Mathematical Functions

**Purpose**: Deterministic calculations with no side effects.

**Functions**:

#### Basic Vitals
- `calculate_bmi(weight_kg, height_cm)` → float
  - BMI = weight / (height_m)²
  - Range: [10, 60]

- `calculate_map(systolic_bp, diastolic_bp)` → float
  - Mean Arterial Pressure = (SBP + 2×DBP) / 3
  - Clinical: <80 (normal), 80-90 (elevated), >90 (high)

- `calculate_pulse_pressure(systolic_bp, diastolic_bp)` → int
  - Pulse Pressure = SBP - DBP
  - Clinical: 40-60 (normal), >60 (concerning)

#### Categorical Binning
- `calculate_gestational_trimester(weeks_pregnant)` → int
  - 0: First (1-13 weeks)
  - 1: Second (14-26 weeks)
  - 2: Third (27-42 weeks)

- `compute_age_group(age)` → int
  - 0: Teen (<18)
  - 1: Optimal (18-34)
  - 2: Advanced (35-39)
  - 3: High-risk (40+)

- `compute_bmi_category(bmi)` → int
  - 0: Underweight (<18.5)
  - 1: Normal (18.5-24.9)
  - 2: Overweight (25.0-29.9)
  - 3: Obese (≥30.0)

- `compute_bp_category(systolic_bp, diastolic_bp)` → int
  - 0: Normal (SBP<120, DBP<80)
  - 1: Elevated (SBP 120-129, DBP<80)
  - 2: Stage 1 (SBP 130-139 or DBP 80-89)
  - 3: Stage 2 (SBP≥140 or DBP≥90)

#### Aggregations
- `count_symptoms(headache, blurred_vision, ...)` → int
  - Sum of 9 binary symptom fields → [0-9]

- `is_high_risk_age(age)` → int
  - 1 if age < 18 or age > 35, else 0

- `compute_hypertension_risk(history, systolic, diastolic)` → int
  - 1 if history OR Stage 2 BP, else 0

- `compute_diabetes_risk(history, blood_sugar)` → int
  - 1 if history OR glucose > 140, else 0

- `compute_accessibility_index(distance_km, time_min)` → int
  - 0: Good (<10km, <20min)
  - 1: Moderate (10-50km, 20-60min)
  - 2: Poor (>50km, >60min)

- `compute_symptom_severity_score(symptom_count)` → int
  - 0: None (0 symptoms)
  - 1: Mild (1-2 symptoms)
  - 2: Moderate (3-5 symptoms)
  - 3: Severe (6+ symptoms)

- `has_emergency_flag(bleeding, breathing, vomiting, movement)` → int
  - 1 if bleeding OR difficulty_breathing, else 0

---

### 2. `transformers.py` — Categorical Conversions

**Purpose**: Convert integer categories to human-readable labels.

**Functions**:
- `transform_bmi_category(category)` → str
  - 0 → "Underweight"
  - 1 → "Normal"
  - 2 → "Overweight"
  - 3 → "Obese"

- `transform_bp_category(category)` → str
  - Similar mapping for hypertension stages

- `transform_age_group_label(category)` → str
  - 0 → "Teen Pregnancy (<18)"
  - 1 → "Optimal Age (18-34)"
  - etc.

- `transform_trimester_label(category)` → str
- `transform_accessibility_label(category)` → str
- `transform_severity_label(category)` → str

**Purpose**: Used for explanations and human-readable output. Not required for ML.

---

### 3. `validators.py` — Input Validation

**Purpose**: Reject impossible or clinically unrealistic values before they reach the pipeline.

**Coverage**:
- Demographics: Age [15-49], Weeks [1-42]
- Anthropometrics: Height [130-210cm], Weight [35-200kg]
- Vitals: BP [60-220/40-140], HR [40-180bpm], Temp [35-42°C]
- Labs: Blood sugar [40-500], SpO2 [70-100], Hemoglobin [5-20]
- Binary fields: All must be 0 or 1
- Environment: Distance [0-500km], Travel time [0-300min]

**Raises**: `ValidationError` with detailed error messages.

---

### 4. `encoders.py` — Numeric Encoding

**Purpose**: Convert categories to numeric codes that ML models understand.

**Encoding Strategies**:

#### Ordinal Encoding (for ordered categories)
```
BMI Category → [0, 1, 2, 3]  (preserves ordering)
Trimester → [0, 1, 2]
Severity → [0, 1, 2, 3]
```

#### Binary Encoding (for binary categories)
```
Urban/Rural → [0=Rural, 1=Urban]
Binary symptoms → [0, 1]
```

**Functions**:
- `encode_bmi_category(bmi_category)` → int
- `encode_bp_category(bp_category)` → int
- `encode_trimester(trimester)` → int
- `encode_age_group(age_group)` → int
- `encode_urban_rural(location)` → int
- `encode_accessibility(accessibility)` → int
- `encode_severity(severity)` → int

---

### 5. `feature_pipeline.py` — Orchestration

**Purpose**: Single entry point that coordinates all layers.

**Main Function**:
```python
def engineer_features(raw_data: Dict[str, Any]) -> pd.DataFrame
```

**Pipeline Stages**:
1. **Validation** → Reject impossible inputs
2. **Calculation** → Compute derived numerical features
3. **Transformation** → Convert to clinically meaningful categories
4. **Encoding** → Convert categories to numeric codes
5. **DataFrame Creation** → Return single-row DataFrame

**Output DataFrame** contains:
- Original vitals (systolic_bp, diastolic_bp, heart_rate, etc.)
- Derived features (bmi, map, pulse_pressure)
- Computed categories (trimester, age_group, bp_category)
- Risk flags (high_risk_age, hypertension_risk, emergency_flag)
- Aggregations (symptom_count, symptom_severity)
- Encoded versions (trimester_encoded, bp_category_encoded, etc.)
- Medical history (previous_pregnancies, history_hypertension, etc.)
- Symptoms (headache, bleeding, etc.)

**Total Features**: ~45-50 per sample

---

## Feature Groups

### 1. Demographics (5)
- age
- weeks_pregnant
- height_cm
- weight_kg
- age_group

### 2. Computed Vitals (7)
- bmi
- map
- pulse_pressure
- systolic_bp
- diastolic_bp
- heart_rate
- body_temperature

### 3. Labs (5)
- blood_sugar
- oxygen_saturation
- hemoglobin
- [future: white blood cell count, platelets]

### 4. Categories (7)
- trimester (+ trimester_encoded)
- bmi_category (+ encoded)
- bp_category (+ encoded)
- age_group (+ encoded)
- symptom_severity (+ encoded)
- accessibility_index (+ encoded)

### 5. Risk Flags (4)
- high_risk_age
- hypertension_risk
- diabetes_risk
- emergency_flag

### 6. Medical History (7)
- previous_pregnancies
- previous_c_section
- previous_miscarriages
- multiple_pregnancy
- history_hypertension
- history_diabetes
- history_pre_eclampsia

### 7. Symptoms (9)
- headache
- blurred_vision
- swollen_feet
- bleeding
- abdominal_pain
- fever
- reduced_fetal_movement
- severe_vomiting
- difficulty_breathing

### 8. Aggregations (2)
- symptom_count (sum of 9 symptoms)
- symptom_severity (0-3 based on count)

### 9. Lifestyle (4)
- smoker
- alcohol
- nutrition_score
- water_intake

### 10. Environment (3)
- distance_to_hospital
- travel_time_minutes
- urban_rural (+ urban_rural_encoded)

---

## Usage

### Basic Usage
```python
from ml.feature_engineering import engineer_features

raw_data = {
    "age": 28,
    "weeks_pregnant": 32,
    "height_cm": 165.0,
    "weight_kg": 70.0,
    "systolic_bp": 130,
    "diastolic_bp": 85,
    "heart_rate": 82,
    "body_temperature": 36.8,
    "blood_sugar": 95.0,
    "oxygen_saturation": 97.5,
    "hemoglobin": 12.1,
    # ... other fields
}

feature_vector = engineer_features(raw_data)
# Returns: Single-row pandas DataFrame with ~45-50 features

# Use for prediction
prediction = model.predict(feature_vector)
```

### Integration with API
```python
# In api/services/risk_service.py
from ml.feature_engineering import engineer_features

class RiskService:
    def predict(self, payload: RiskAssessmentRequest) -> RiskAssessmentResponse:
        # Convert request to raw data dict
        raw_data = payload.dict()
        
        # Engineer features
        features_df = engineer_features(raw_data)
        
        # Make prediction
        prediction = self.model.predict(features_df)
        
        return RiskAssessmentResponse(...)
```

---

## Testing

### Test Coverage
- **test_calculators.py**: 60+ unit tests for all mathematical functions
- **test_pipeline.py**: 30+ integration tests for the complete pipeline

### Running Tests
```bash
# Test calculators only
pytest ml/feature_engineering/tests/test_calculators.py -v

# Test pipeline integration
pytest ml/feature_engineering/tests/test_pipeline.py -v

# All feature engineering tests
pytest ml/feature_engineering/tests/ -v

# With coverage
pytest ml/feature_engineering/tests/ --cov=ml.feature_engineering
```

### Test Examples
```python
# Unit test for single function
def test_bmi_calculation():
    assert calculate_bmi(70, 170) == 24.22

# Integration test for pipeline
def test_pipeline_produces_dataframe():
    data = {...}
    result = engineer_features(data)
    assert isinstance(result, pd.DataFrame)
    assert "bmi" in result.columns
    assert "emergency_flag" in result.columns
```

---

## Design Principles

### 1. **Separation of Concerns**
Each layer has one responsibility:
- Validators: Only validate
- Calculators: Only calculate
- Transformers: Only transform to text
- Encoders: Only convert to numbers
- Pipeline: Only orchestrate

### 2. **Pure Functions**
All functions in calculators.py are pure:
- Same input → Same output
- No side effects
- Easy to test
- Deterministic

### 3. **Fail Fast**
Validators run first to reject bad data before expensive computation.

### 4. **Reversibility**
Most transformations are reversible (can decode back to categories).

### 5. **No ML Leakage**
- Training data never touches test data
- Feature engineering operates identically on both
- Scaling/normalization happens after train/test split (future)

---

## Future Enhancements

### Short Term
- [ ] Scaling/normalization (StandardScaler, RobustScaler)
- [ ] Feature interaction terms (age × hypertension_risk)
- [ ] Temporal features (day of week, season)
- [ ] Missing value imputation strategies
- [ ] Outlier detection and handling

### Medium Term
- [ ] SHAP-compatible feature explanations
- [ ] Feature importance tracking
- [ ] Online learning feature updates
- [ ] Cross-validation pipeline
- [ ] A/B testing framework

### Long Term
- [ ] Automated feature discovery (AutoML)
- [ ] Federated learning feature engineering
- [ ] Real-time feature computation (streaming)
- [ ] Multi-model ensemble feature engineering

---

## References

- WHO Guidelines on Pregnancy Monitoring
- ML Feature Engineering Best Practices (Google, Stanford)
- Clinical Decision Support Systems (MIT-BIH)
- Production ML Systems Design (Sculley et al., 2015)

---

**Module Status**: ✅ Complete  
**Test Coverage**: ✅ Comprehensive (90+ tests)  
**Production Ready**: ✅ Yes  
**Documentation**: ✅ Complete
