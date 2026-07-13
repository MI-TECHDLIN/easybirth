# Dataset Specification

## Goal

Create a reproducible synthetic dataset for pregnancy risk prediction that is grounded in publicly available maternal health references and clinically plausible rules.

## Target prediction

The model predicts one of four risk levels:

- Low
- Moderate
- High
- Emergency

## Core feature groups

- Demographics: age, height_cm, weight_kg, bmi, weeks_pregnant
- Medical history: previous_pregnancies, previous_c_section, previous_miscarriages, multiple_pregnancy, history_hypertension, history_diabetes, history_pre_eclampsia
- Vital signs: systolic_bp, diastolic_bp, heart_rate, body_temperature, blood_sugar, oxygen_saturation, hemoglobin
- Symptoms: headache, blurred_vision, swollen_feet, bleeding, abdominal_pain, fever, reduced_fetal_movement, severe_vomiting, difficulty_breathing
- Lifestyle: smoker, alcohol, nutrition_score, water_intake, sleep_hours
- Environment: distance_to_hospital, travel_time_minutes, urban_or_rural

## Data generation requirements

- Minimum 5,000 rows for the first synthetic dataset
- Reproducible via a fixed random seed
- No missing values
- Realistic age and pregnancy week ranges
- Realistic physiological and symptom values
- Balanced class distribution for training purposes

## Validation requirements

The synthetic data pipeline must verify:

- No missing values
- Age in a realistic reproductive range
- Pregnancy weeks between 1 and 42
- BMI within plausible bounds
- Blood pressure values within realistic limits
- No duplicate rows
- Expected risk class distribution
