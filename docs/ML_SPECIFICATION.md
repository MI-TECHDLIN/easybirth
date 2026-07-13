# EasyBirth AI System Specification

**Project:** EasyBirth

**Version:** 0.1.0

**Status:** Draft

**Authors:** EasyBirth AI Team

---

# 1. Overview

EasyBirth is an AI-powered maternal health platform designed to assist pregnant women through intelligent pregnancy risk assessment, personalized recommendations, and continuous monitoring.

The AI system serves as a clinical decision support tool and does not replace licensed healthcare professionals.

The goal is to identify pregnancies that may require additional medical attention as early as possible.

---

# 2. Problem Statement

Pregnancy complications often develop gradually and may not be recognized early enough.

Many expectant mothers lack continuous access to healthcare professionals, especially in underserved communities.

EasyBirth aims to estimate pregnancy risk using available patient information and provide explainable recommendations that encourage timely medical consultation.

---

# 3. Objectives

The AI system should:

- Estimate pregnancy risk.
- Explain why the prediction was made.
- Recommend appropriate next actions.
- Continuously improve as more validated data becomes available.
- Support multilingual users in future releases.

---

# 4. Scope

## Current Version (MVP)

- Pregnancy risk assessment
- Explainable AI
- Rule-based recommendations

## Future Versions

- Voice-based stress analysis
- Pregnancy chatbot
- Personalized nutrition
- Maternal timeline prediction
- Continuous monitoring

---

# 5. Prediction Target

## Primary Target

Predict maternal pregnancy risk.

Output:

- LOW
- MEDIUM
- HIGH

## Secondary Outputs

- Risk probability (0.0–1.0)
- Prediction confidence
- Top contributing factors
- Recommended actions

---

# 6. Input Features

## Demographic

- Age
- Height
- Weight
- Location (optional)
- Education level (future)
- Socioeconomic status (future)

## Pregnancy

- Gestational week
- Number of previous pregnancies
- Previous miscarriages
- Previous complications
- Multiple pregnancy
- Expected delivery date

## Medical History

- Hypertension
- Diabetes
- Anemia
- Heart disease
- Previous cesarean section
- Smoking
- Alcohol consumption

## Vital Signs

- Systolic blood pressure
- Diastolic blood pressure
- Body temperature
- Heart rate
- Hemoglobin
- Blood sugar
- Oxygen saturation (future)

## Symptoms

- Headache
- Swelling
- Bleeding
- Blurred vision
- Dizziness
- Abdominal pain
- Vomiting
- Reduced fetal movement

## Future AI Features

- Voice embeddings
- Stress indicators
- Emotion features
- Sleep patterns
- Wearable device data

---

# 7. Feature Engineering

The backend computes engineered features before inference.

Examples:

- BMI = weight / height²
- Mean arterial pressure (MAP)
- Pulse pressure
- Age group
- Pregnancy trimester
- Blood pressure category
- Hemoglobin category
- Symptom count
- High risk history flag

Feature engineering must remain inside the backend and never be performed by the Flutter application.

---

# 8. Target Labels

- 0 → LOW
- 1 → MEDIUM
- 2 → HIGH

---

# 9. Candidate Models

## Baseline

- Logistic regression
- Decision tree

## Production Candidates

- Random forest
- XGBoost
- LightGBM
- CatBoost

## Future Candidates

- TabNet
- Neural networks

---

# 10. Evaluation Metrics

## Primary

- Recall
- F1 score
- ROC AUC

## Secondary

- Precision
- Accuracy
- Confusion matrix
- False negative rate

Healthcare prioritizes minimizing false negatives.

---

# 11. Explainability

Every prediction must include explainability.

## Methods

- SHAP
- Feature importance
- Natural language explanation

Example:

> High blood pressure contributed most strongly to this assessment.

---

# 12. Recommendation Engine

The recommendation engine combines:

- Model prediction
- Clinical rules
- WHO guidelines

Recommendations should never diagnose diseases. Instead, they recommend actions.

Examples:

- Monitor symptoms
- Visit the nearest clinic
- Schedule an antenatal appointment
- Seek emergency medical attention

---

# 13. Training Pipeline

Synthetic data

↓

Validation

↓

Cleaning

↓

Feature engineering

↓

Training

↓

Evaluation

↓

Model registry

↓

Inference

---

# 14. Inference Pipeline

Incoming request

↓

Validation

↓

Feature engineering

↓

Model prediction

↓

SHAP explanation

↓

Recommendation engine

↓

Response

---

# 15. Model Artifacts

Artifacts should be stored under the model registry location:

- model.pkl
- feature_names.json
- metrics.json
- label_encoder.pkl
- model_card.md

---

# 16. Monitoring

Track:

- Prediction latency
- Prediction distribution
- Confidence scores
- Feature drift
- Data drift
- Model drift
- API errors

---

# 17. Safety

The AI provides decision support only.

It does not replace doctors.

Users must seek professional medical advice for emergencies.

Predictions should always be accompanied by confidence scores and explanations.

---

# 18. Maternal Health Report

To improve the end-user experience, the API should eventually return a structured maternal health report in addition to the core prediction.

Example response structure:

```json
{
  "risk_level": "HIGH",
  "confidence": 0.93,
  "summary": {
    "overall_assessment": "Your current health indicators suggest an elevated pregnancy risk that should be evaluated promptly.",
    "top_factors": [
      "Elevated blood pressure",
      "Previous pregnancy complications",
      "Persistent headache"
    ],
    "recommended_actions": [
      "Schedule an antenatal visit within 24 hours.",
      "Monitor your blood pressure twice daily.",
      "Seek emergency care if symptoms worsen."
    ]
  }
}
```

This report remains consistent with the AI system's role as a decision-support tool rather than a diagnostic system.

---

# 19. Roadmap

## Phase 1

- Pregnancy risk prediction

## Phase 2

- Voice analysis

## Phase 3

- Chatbot

## Phase 4

- Personalized care plans

## Phase 5

- Federated learning
