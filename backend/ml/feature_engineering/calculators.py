"""Pure mathematical calculations for feature engineering.

This module contains deterministic, stateless functions that compute
derived features from raw maternal health data.

All functions are pure: same input always produces same output,
with no side effects.
"""

from typing import Union


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """
    Calculate Body Mass Index (BMI).

    BMI = weight (kg) / (height (m))^2

    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters

    Returns:
        BMI value (float)

    Raises:
        ValueError: If weight or height is not positive
    """
    if weight_kg <= 0:
        raise ValueError(f"Weight must be positive, got {weight_kg}")
    if height_cm <= 0:
        raise ValueError(f"Height must be positive, got {height_cm}")

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def calculate_map(systolic_bp: int, diastolic_bp: int) -> float:
    """
    Calculate Mean Arterial Pressure (MAP).

    MAP = (SBP + 2 × DBP) / 3

    Clinical interpretation:
    - Normal: < 80 mmHg
    - Elevated: 80-90 mmHg
    - High: > 90 mmHg

    Args:
        systolic_bp: Systolic blood pressure (mmHg)
        diastolic_bp: Diastolic blood pressure (mmHg)

    Returns:
        MAP in mmHg (float)

    Raises:
        ValueError: If blood pressure values are not positive
    """
    if systolic_bp <= 0:
        raise ValueError(f"Systolic BP must be positive, got {systolic_bp}")
    if diastolic_bp <= 0:
        raise ValueError(f"Diastolic BP must be positive, got {diastolic_bp}")

    map_value = (systolic_bp + 2 * diastolic_bp) / 3
    return round(map_value, 2)


def calculate_pulse_pressure(systolic_bp: int, diastolic_bp: int) -> int:
    """
    Calculate Pulse Pressure.

    Pulse Pressure = SBP - DBP

    Clinical significance:
    - Normal: 40-60 mmHg
    - Elevated: > 60 mmHg (may indicate arterial stiffness)
    - Low: < 40 mmHg (may indicate low cardiac output)

    Args:
        systolic_bp: Systolic blood pressure (mmHg)
        diastolic_bp: Diastolic blood pressure (mmHg)

    Returns:
        Pulse pressure in mmHg (int)

    Raises:
        ValueError: If systolic_bp is not greater than diastolic_bp
    """
    if systolic_bp <= 0:
        raise ValueError(f"Systolic BP must be positive, got {systolic_bp}")
    if diastolic_bp <= 0:
        raise ValueError(f"Diastolic BP must be positive, got {diastolic_bp}")
    if systolic_bp <= diastolic_bp:
        raise ValueError(
            f"Systolic ({systolic_bp}) must be > Diastolic ({diastolic_bp})"
        )

    return systolic_bp - diastolic_bp


def calculate_gestational_trimester(weeks_pregnant: int) -> int:
    """
    Calculate gestational trimester from weeks of pregnancy.

    Trimesters:
    - First: 1-13 weeks (0)
    - Second: 14-26 weeks (1)
    - Third: 27-42 weeks (2)

    Args:
        weeks_pregnant: Number of weeks of pregnancy

    Returns:
        Trimester as integer (0, 1, or 2)

    Raises:
        ValueError: If weeks_pregnant is not in valid range [1, 42]
    """
    if not isinstance(weeks_pregnant, int):
        raise ValueError(f"Weeks must be integer, got {type(weeks_pregnant)}")
    if weeks_pregnant < 1 or weeks_pregnant > 42:
        raise ValueError(
            f"Pregnancy weeks must be 1-42, got {weeks_pregnant}"
        )

    if weeks_pregnant <= 13:
        return 0
    elif weeks_pregnant <= 26:
        return 1
    else:
        return 2


def count_symptoms(
    headache: int = 0,
    blurred_vision: int = 0,
    swollen_feet: int = 0,
    bleeding: int = 0,
    abdominal_pain: int = 0,
    fever: int = 0,
    reduced_fetal_movement: int = 0,
    severe_vomiting: int = 0,
    difficulty_breathing: int = 0,
) -> int:
    """
    Count total number of reported symptoms.

    All symptoms are binary (0 or 1).

    Args:
        headache: Presence of headache (0 or 1)
        blurred_vision: Presence of blurred vision (0 or 1)
        swollen_feet: Presence of swollen feet (0 or 1)
        bleeding: Presence of bleeding (0 or 1)
        abdominal_pain: Presence of abdominal pain (0 or 1)
        fever: Presence of fever (0 or 1)
        reduced_fetal_movement: Reduced fetal movement (0 or 1)
        severe_vomiting: Presence of severe vomiting (0 or 1)
        difficulty_breathing: Difficulty breathing (0 or 1)

    Returns:
        Total symptom count (0-9)

    Raises:
        ValueError: If any symptom is not 0 or 1
    """
    symptoms = [
        headache,
        blurred_vision,
        swollen_feet,
        bleeding,
        abdominal_pain,
        fever,
        reduced_fetal_movement,
        severe_vomiting,
        difficulty_breathing,
    ]

    for i, symptom in enumerate(symptoms):
        if symptom not in (0, 1):
            raise ValueError(f"Symptom must be 0 or 1, got {symptom}")

    return sum(symptoms)


def compute_age_group(age: int) -> int:
    """
    Compute age group category for clinical significance.

    Age groups:
    - 0: Less than 18 years (teen pregnancy)
    - 1: 18-34 years (optimal)
    - 2: 35-39 years (advanced maternal age)
    - 3: 40+ years (high-risk advanced maternal age)

    Args:
        age: Age in years

    Returns:
        Age group as integer (0, 1, 2, or 3)

    Raises:
        ValueError: If age is not in valid range [15, 49]
    """
    if not isinstance(age, int):
        raise ValueError(f"Age must be integer, got {type(age)}")
    if age < 15 or age > 49:
        raise ValueError(f"Age must be 15-49, got {age}")

    if age < 18:
        return 0  # Teen pregnancy
    elif age <= 34:
        return 1  # Optimal age
    elif age <= 39:
        return 2  # Advanced maternal age
    else:
        return 3  # High-risk advanced maternal age


def compute_bmi_category(bmi: float) -> int:
    """
    Convert BMI to clinical category.

    Categories (WHO standards during pregnancy):
    - 0: Underweight (BMI < 18.5)
    - 1: Normal weight (18.5 ≤ BMI < 25.0)
    - 2: Overweight (25.0 ≤ BMI < 30.0)
    - 3: Obese (BMI ≥ 30.0)

    Args:
        bmi: BMI value

    Returns:
        BMI category as integer (0, 1, 2, or 3)

    Raises:
        ValueError: If BMI is not in valid range [10, 60]
    """
    if bmi < 10 or bmi > 60:
        raise ValueError(f"BMI must be 10-60, got {bmi}")

    if bmi < 18.5:
        return 0  # Underweight
    elif bmi < 25.0:
        return 1  # Normal
    elif bmi < 30.0:
        return 2  # Overweight
    else:
        return 3  # Obese


def compute_bp_category(systolic_bp: int, diastolic_bp: int) -> int:
    """
    Convert blood pressure to hypertension category.

    Categories (American Heart Association):
    - 0: Normal (SBP < 120 AND DBP < 80)
    - 1: Elevated (SBP 120-129 AND DBP < 80)
    - 2: Stage 1 Hypertension (SBP 130-139 OR DBP 80-89)
    - 3: Stage 2 Hypertension (SBP ≥ 140 OR DBP ≥ 90)

    Args:
        systolic_bp: Systolic blood pressure (mmHg)
        diastolic_bp: Diastolic blood pressure (mmHg)

    Returns:
        BP category as integer (0, 1, 2, or 3)

    Raises:
        ValueError: If BP values are not in valid range [60/40, 220/140]
    """
    if systolic_bp < 60 or systolic_bp > 220:
        raise ValueError(f"Systolic BP must be 60-220, got {systolic_bp}")
    if diastolic_bp < 40 or diastolic_bp > 140:
        raise ValueError(f"Diastolic BP must be 40-140, got {diastolic_bp}")

    if systolic_bp < 120 and diastolic_bp < 80:
        return 0  # Normal
    elif 120 <= systolic_bp < 130 and diastolic_bp <= 80:
        return 1  # Elevated
    elif (130 <= systolic_bp < 140 or (80 <= diastolic_bp < 90)):
        return 2  # Stage 1
    else:
        return 3  # Stage 2


def is_high_risk_age(age: int) -> int:
    """
    Determine if age is high-risk for pregnancy.

    High-risk: age < 18 or age > 35

    Args:
        age: Age in years

    Returns:
        1 if high-risk, 0 otherwise

    Raises:
        ValueError: If age is not in valid range [15, 49]
    """
    if age < 15 or age > 49:
        raise ValueError(f"Age must be 15-49, got {age}")

    return 1 if age < 18 or age > 35 else 0


def compute_hypertension_risk(
    history_hypertension: int, systolic_bp: int, diastolic_bp: int
) -> int:
    """
    Compute combined hypertension risk score.

    Risk if: history of hypertension OR Stage 2 BP detected

    Args:
        history_hypertension: Binary (0 or 1)
        systolic_bp: Systolic blood pressure (mmHg)
        diastolic_bp: Diastolic blood pressure (mmHg)

    Returns:
        1 if high risk, 0 otherwise
    """
    bp_category = compute_bp_category(systolic_bp, diastolic_bp)
    stage_2_hypertension = 1 if bp_category == 3 else 0

    return 1 if (history_hypertension or stage_2_hypertension) else 0


def compute_diabetes_risk(
    history_diabetes: int, blood_sugar: float
) -> int:
    """
    Compute combined diabetes risk score.

    Risk if: history of diabetes OR elevated blood sugar (>140 mg/dL fasting)

    Args:
        history_diabetes: Binary (0 or 1)
        blood_sugar: Blood sugar in mg/dL

    Returns:
        1 if high risk, 0 otherwise
    """
    elevated_glucose = 1 if blood_sugar > 140 else 0
    return 1 if (history_diabetes or elevated_glucose) else 0


def compute_accessibility_index(
    distance_to_hospital_km: int, travel_time_minutes: int
) -> int:
    """
    Compute accessibility to hospital as single index.

    Index:
    - 0: Good access (< 10 km, < 20 min)
    - 1: Moderate access (10-50 km, 20-60 min)
    - 2: Poor access (> 50 km, > 60 min)

    Args:
        distance_to_hospital_km: Distance in kilometers
        travel_time_minutes: Travel time in minutes

    Returns:
        Accessibility index (0, 1, or 2)
    """
    if distance_to_hospital_km < 10 and travel_time_minutes < 20:
        return 0  # Good
    elif distance_to_hospital_km <= 50 and travel_time_minutes <= 60:
        return 1  # Moderate
    else:
        return 2  # Poor


def compute_symptom_severity_score(symptom_count: int) -> int:
    """
    Convert symptom count to severity level.

    Severity:
    - 0: None (0 symptoms)
    - 1: Mild (1-2 symptoms)
    - 2: Moderate (3-5 symptoms)
    - 3: Severe (6+ symptoms)

    Args:
        symptom_count: Total number of symptoms (0-9)

    Returns:
        Severity score (0, 1, 2, or 3)
    """
    if symptom_count == 0:
        return 0
    elif symptom_count <= 2:
        return 1
    elif symptom_count <= 5:
        return 2
    else:
        return 3


def has_emergency_flag(
    bleeding: int = 0,
    difficulty_breathing: int = 0,
    severe_vomiting: int = 0,
    reduced_fetal_movement: int = 0,
) -> int:
    """
    Determine if emergency warning signs are present.

    Emergency flags if: bleeding OR difficulty breathing

    Args:
        bleeding: Binary (0 or 1)
        difficulty_breathing: Binary (0 or 1)
        severe_vomiting: Binary (0 or 1)
        reduced_fetal_movement: Binary (0 or 1)

    Returns:
        1 if emergency conditions present, 0 otherwise
    """
    # Most critical: bleeding + difficulty breathing
    critical = bleeding or difficulty_breathing

    return 1 if critical else 0
