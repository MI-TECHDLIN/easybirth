"""Encodes categorical features into machine-learning friendly numeric formats.

This module converts human-readable categories into numeric representations
that machine learning models can process.
"""

from typing import Union


def encode_bmi_category(bmi_category: Union[int, str]) -> int:
    """
    Encode BMI category to numeric representation.

    Encoding:
    - 0 → Underweight
    - 1 → Normal
    - 2 → Overweight
    - 3 → Obese

    Args:
        bmi_category: BMI category as int (0-3) or string name

    Returns:
        Encoded numeric value (0-3)

    Raises:
        ValueError: If category is invalid
    """
    if isinstance(bmi_category, int):
        if bmi_category not in (0, 1, 2, 3):
            raise ValueError(f"Invalid BMI category: {bmi_category}")
        return bmi_category

    # String encoding
    encoding_map = {
        "Underweight": 0,
        "Normal": 1,
        "Overweight": 2,
        "Obese": 3,
    }

    if bmi_category not in encoding_map:
        raise ValueError(f"Unknown BMI category: {bmi_category}")

    return encoding_map[bmi_category]


def encode_bp_category(bp_category: Union[int, str]) -> int:
    """
    Encode blood pressure category to numeric representation.

    Encoding:
    - 0 → Normal
    - 1 → Elevated
    - 2 → Stage 1 Hypertension
    - 3 → Stage 2 Hypertension

    Args:
        bp_category: BP category as int (0-3) or string name

    Returns:
        Encoded numeric value (0-3)

    Raises:
        ValueError: If category is invalid
    """
    if isinstance(bp_category, int):
        if bp_category not in (0, 1, 2, 3):
            raise ValueError(f"Invalid BP category: {bp_category}")
        return bp_category

    # String encoding
    encoding_map = {
        "Normal": 0,
        "Elevated": 1,
        "Stage 1 Hypertension": 2,
        "Stage 2 Hypertension": 3,
    }

    if bp_category not in encoding_map:
        raise ValueError(f"Unknown BP category: {bp_category}")

    return encoding_map[bp_category]


def encode_trimester(trimester: Union[int, str]) -> int:
    """
    Encode trimester to numeric representation.

    Encoding:
    - 0 → First Trimester
    - 1 → Second Trimester
    - 2 → Third Trimester

    Args:
        trimester: Trimester as int (0-2) or string name

    Returns:
        Encoded numeric value (0-2)

    Raises:
        ValueError: If trimester is invalid
    """
    if isinstance(trimester, int):
        if trimester not in (0, 1, 2):
            raise ValueError(f"Invalid trimester: {trimester}")
        return trimester

    # String encoding
    encoding_map = {
        "First Trimester": 0,
        "First Trimester (1-13 weeks)": 0,
        "Second Trimester": 1,
        "Second Trimester (14-26 weeks)": 1,
        "Third Trimester": 2,
        "Third Trimester (27-42 weeks)": 2,
    }

    if trimester not in encoding_map:
        raise ValueError(f"Unknown trimester: {trimester}")

    return encoding_map[trimester]


def encode_urban_rural(urban_rural: Union[int, str]) -> int:
    """
    Encode urban/rural setting.

    Encoding:
    - 0 → Rural
    - 1 → Urban

    Args:
        urban_rural: Location as int (0 or 1) or string ("urban"/"rural")

    Returns:
        Encoded numeric value (0 or 1)

    Raises:
        ValueError: If value is invalid
    """
    if isinstance(urban_rural, int):
        if urban_rural not in (0, 1):
            raise ValueError(f"Invalid urban_rural value: {urban_rural}")
        return urban_rural

    # String encoding
    location_str = urban_rural.lower().strip()
    encoding_map = {
        "urban": 1,
        "rural": 0,
    }

    if location_str not in encoding_map:
        raise ValueError(f"Unknown location: {urban_rural}")

    return encoding_map[location_str]


def encode_age_group(age_group: Union[int, str]) -> int:
    """
    Encode age group to numeric representation.

    Encoding:
    - 0 → Teen Pregnancy
    - 1 → Optimal Age
    - 2 → Advanced Maternal Age
    - 3 → High-Risk Advanced Age

    Args:
        age_group: Age group as int (0-3) or string name

    Returns:
        Encoded numeric value (0-3)

    Raises:
        ValueError: If age group is invalid
    """
    if isinstance(age_group, int):
        if age_group not in (0, 1, 2, 3):
            raise ValueError(f"Invalid age group: {age_group}")
        return age_group

    # String encoding
    encoding_map = {
        "Teen Pregnancy": 0,
        "Teen Pregnancy (<18)": 0,
        "Optimal Age": 1,
        "Optimal Age (18-34)": 1,
        "Advanced Maternal Age": 2,
        "Advanced Maternal Age (35-39)": 2,
        "High-Risk Advanced Age": 3,
        "High-Risk Advanced Age (40+)": 3,
    }

    if age_group not in encoding_map:
        raise ValueError(f"Unknown age group: {age_group}")

    return encoding_map[age_group]


def encode_accessibility(accessibility: Union[int, str]) -> int:
    """
    Encode accessibility to hospital.

    Encoding:
    - 0 → Good Access
    - 1 → Moderate Access
    - 2 → Poor Access

    Args:
        accessibility: Accessibility as int (0-2) or string name

    Returns:
        Encoded numeric value (0-2)

    Raises:
        ValueError: If accessibility is invalid
    """
    if isinstance(accessibility, int):
        if accessibility not in (0, 1, 2):
            raise ValueError(f"Invalid accessibility: {accessibility}")
        return accessibility

    # String encoding
    encoding_map = {
        "Good Access": 0,
        "Moderate Access": 1,
        "Poor Access": 2,
    }

    if accessibility not in encoding_map:
        raise ValueError(f"Unknown accessibility: {accessibility}")

    return encoding_map[accessibility]


def encode_severity(severity: Union[int, str]) -> int:
    """
    Encode symptom severity level.

    Encoding:
    - 0 → No Symptoms
    - 1 → Mild
    - 2 → Moderate
    - 3 → Severe

    Args:
        severity: Severity as int (0-3) or string name

    Returns:
        Encoded numeric value (0-3)

    Raises:
        ValueError: If severity is invalid
    """
    if isinstance(severity, int):
        if severity not in (0, 1, 2, 3):
            raise ValueError(f"Invalid severity: {severity}")
        return severity

    # String encoding
    encoding_map = {
        "No Symptoms": 0,
        "Mild": 1,
        "Moderate": 2,
        "Severe": 3,
    }

    if severity not in encoding_map:
        raise ValueError(f"Unknown severity: {severity}")

    return encoding_map[severity]
