"""Transforms numerical values into clinically meaningful categories.

This module converts computed features into human-readable, clinically
relevant categories.
"""


def transform_bmi_category(bmi_category: int) -> str:
    """
    Transform BMI category integer to human-readable label.

    Args:
        bmi_category: BMI category (0, 1, 2, or 3)

    Returns:
        Human-readable BMI category label

    Raises:
        ValueError: If category is not in range [0, 3]
    """
    categories = {
        0: "Underweight",
        1: "Normal",
        2: "Overweight",
        3: "Obese",
    }
    if bmi_category not in categories:
        raise ValueError(f"BMI category must be 0-3, got {bmi_category}")
    return categories[bmi_category]


def transform_bp_category(bp_category: int) -> str:
    """
    Transform blood pressure category integer to label.

    Args:
        bp_category: BP category (0, 1, 2, or 3)

    Returns:
        Human-readable BP category label

    Raises:
        ValueError: If category is not in range [0, 3]
    """
    categories = {
        0: "Normal",
        1: "Elevated",
        2: "Stage 1 Hypertension",
        3: "Stage 2 Hypertension",
    }
    if bp_category not in categories:
        raise ValueError(f"BP category must be 0-3, got {bp_category}")
    return categories[bp_category]


def transform_age_group_label(age_group: int) -> str:
    """
    Transform age group integer to descriptive label.

    Args:
        age_group: Age group (0, 1, 2, or 3)

    Returns:
        Human-readable age group label

    Raises:
        ValueError: If age_group is not in range [0, 3]
    """
    groups = {
        0: "Teen Pregnancy (<18)",
        1: "Optimal Age (18-34)",
        2: "Advanced Maternal Age (35-39)",
        3: "High-Risk Advanced Age (40+)",
    }
    if age_group not in groups:
        raise ValueError(f"Age group must be 0-3, got {age_group}")
    return groups[age_group]


def transform_trimester_label(trimester: int) -> str:
    """
    Transform trimester integer to descriptive label.

    Args:
        trimester: Trimester (0, 1, or 2)

    Returns:
        Human-readable trimester label

    Raises:
        ValueError: If trimester is not in range [0, 2]
    """
    trimesters = {
        0: "First Trimester (1-13 weeks)",
        1: "Second Trimester (14-26 weeks)",
        2: "Third Trimester (27-42 weeks)",
    }
    if trimester not in trimesters:
        raise ValueError(f"Trimester must be 0-2, got {trimester}")
    return trimesters[trimester]


def transform_accessibility_label(accessibility_index: int) -> str:
    """
    Transform accessibility index to descriptive label.

    Args:
        accessibility_index: Accessibility index (0, 1, or 2)

    Returns:
        Human-readable accessibility label

    Raises:
        ValueError: If index is not in range [0, 2]
    """
    labels = {
        0: "Good Access",
        1: "Moderate Access",
        2: "Poor Access",
    }
    if accessibility_index not in labels:
        raise ValueError(
            f"Accessibility index must be 0-2, got {accessibility_index}"
        )
    return labels[accessibility_index]


def transform_severity_label(severity_score: int) -> str:
    """
    Transform symptom severity score to label.

    Args:
        severity_score: Severity score (0, 1, 2, or 3)

    Returns:
        Human-readable severity label

    Raises:
        ValueError: If score is not in range [0, 3]
    """
    labels = {
        0: "No Symptoms",
        1: "Mild",
        2: "Moderate",
        3: "Severe",
    }
    if severity_score not in labels:
        raise ValueError(f"Severity score must be 0-3, got {severity_score}")
    return labels[severity_score]
