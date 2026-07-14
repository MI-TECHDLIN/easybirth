"""Input validation to reject impossible or clinically unrealistic values.

This module protects the ML pipeline by validating inputs before they
reach feature engineering or the model.
"""

from typing import Dict, Any, List, Tuple


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def _validate_age(age: int) -> Tuple[bool, str]:
    """Validate age value."""
    if not isinstance(age, int):
        return False, f"Age must be integer, got {type(age).__name__}"
    if age < 15:
        return False, f"Age too young for pregnancy: {age} years"
    if age > 49:
        return False, f"Age too old for pregnancy: {age} years"
    return True, ""


def _validate_pregnancy_weeks(weeks: int) -> Tuple[bool, str]:
    """Validate pregnancy weeks."""
    if not isinstance(weeks, int):
        return False, f"Weeks must be integer, got {type(weeks).__name__}"
    if weeks < 1:
        return False, f"Pregnancy weeks must be positive, got {weeks}"
    if weeks > 42:
        return False, f"Pregnancy weeks cannot exceed 42, got {weeks}"
    return True, ""


def _validate_height(height_cm: float) -> Tuple[bool, str]:
    """Validate height."""
    if not isinstance(height_cm, (int, float)):
        return False, f"Height must be numeric, got {type(height_cm).__name__}"
    if height_cm < 130:
        return False, f"Height too short (< 130 cm): {height_cm}"
    if height_cm > 210:
        return False, f"Height too tall (> 210 cm): {height_cm}"
    return True, ""


def _validate_weight(weight_kg: float) -> Tuple[bool, str]:
    """Validate weight."""
    if not isinstance(weight_kg, (int, float)):
        return False, f"Weight must be numeric, got {type(weight_kg).__name__}"
    if weight_kg < 35:
        return False, f"Weight too low (< 35 kg): {weight_kg}"
    if weight_kg > 200:
        return False, f"Weight too high (> 200 kg): {weight_kg}"
    return True, ""


def _validate_blood_pressure(
    systolic_bp: int, diastolic_bp: int
) -> Tuple[bool, str]:
    """Validate blood pressure values."""
    if not isinstance(systolic_bp, int):
        return (
            False,
            f"Systolic BP must be integer, got {type(systolic_bp).__name__}",
        )
    if not isinstance(diastolic_bp, int):
        return (
            False,
            f"Diastolic BP must be integer, got {type(diastolic_bp).__name__}",
        )

    if systolic_bp < 60:
        return False, f"Systolic BP too low (< 60): {systolic_bp}"
    if systolic_bp > 220:
        return False, f"Systolic BP too high (> 220): {systolic_bp}"

    if diastolic_bp < 40:
        return False, f"Diastolic BP too low (< 40): {diastolic_bp}"
    if diastolic_bp > 140:
        return False, f"Diastolic BP too high (> 140): {diastolic_bp}"

    if systolic_bp <= diastolic_bp:
        return (
            False,
            f"Systolic ({systolic_bp}) must be > Diastolic ({diastolic_bp})",
        )

    return True, ""


def _validate_heart_rate(heart_rate: int) -> Tuple[bool, str]:
    """Validate heart rate."""
    if not isinstance(heart_rate, int):
        return (
            False,
            f"Heart rate must be integer, got {type(heart_rate).__name__}",
        )
    if heart_rate < 40:
        return False, f"Heart rate too low (< 40 bpm): {heart_rate}"
    if heart_rate > 180:
        return False, f"Heart rate too high (> 180 bpm): {heart_rate}"
    return True, ""


def _validate_temperature(temp_celsius: float) -> Tuple[bool, str]:
    """Validate body temperature."""
    if not isinstance(temp_celsius, (int, float)):
        return (
            False,
            f"Temperature must be numeric, got {type(temp_celsius).__name__}",
        )
    if temp_celsius < 35:
        return False, f"Temperature too low (hypothermia): {temp_celsius}°C"
    if temp_celsius > 42:
        return False, f"Temperature too high (dangerous): {temp_celsius}°C"
    return True, ""


def _validate_blood_sugar(blood_sugar: float) -> Tuple[bool, str]:
    """Validate blood glucose."""
    if not isinstance(blood_sugar, (int, float)):
        return (
            False,
            f"Blood sugar must be numeric, got {type(blood_sugar).__name__}",
        )
    if blood_sugar < 40:
        return False, f"Blood sugar too low (severe hypoglycemia): {blood_sugar}"
    if blood_sugar > 500:
        return False, f"Blood sugar too high (dangerous): {blood_sugar}"
    return True, ""


def _validate_oxygen_saturation(spo2: float) -> Tuple[bool, str]:
    """Validate oxygen saturation (SpO2)."""
    if not isinstance(spo2, (int, float)):
        return (
            False,
            f"SpO2 must be numeric, got {type(spo2).__name__}",
        )
    if spo2 < 70:
        return False, f"SpO2 critically low (< 70%): {spo2}"
    if spo2 > 100:
        return False, f"SpO2 cannot exceed 100%: {spo2}"
    return True, ""


def _validate_hemoglobin(hemoglobin: float) -> Tuple[bool, str]:
    """Validate hemoglobin level."""
    if not isinstance(hemoglobin, (int, float)):
        return (
            False,
            f"Hemoglobin must be numeric, got {type(hemoglobin).__name__}",
        )
    if hemoglobin < 5:
        return False, f"Hemoglobin too low (< 5 g/dL): {hemoglobin}"
    if hemoglobin > 20:
        return False, f"Hemoglobin too high (> 20 g/dL): {hemoglobin}"
    return True, ""


def _validate_binary_field(value: int, field_name: str) -> Tuple[bool, str]:
    """Validate binary (0/1) fields."""
    if value not in (0, 1):
        return False, f"{field_name} must be 0 or 1, got {value}"
    return True, ""


def _validate_distance(distance_km: int) -> Tuple[bool, str]:
    """Validate distance to hospital."""
    if not isinstance(distance_km, int):
        return (
            False,
            f"Distance must be integer, got {type(distance_km).__name__}",
        )
    if distance_km < 0:
        return False, f"Distance cannot be negative: {distance_km}"
    if distance_km > 500:
        return False, f"Distance > 500 km seems unrealistic: {distance_km}"
    return True, ""


def _validate_travel_time(travel_minutes: int) -> Tuple[bool, str]:
    """Validate travel time to hospital."""
    if not isinstance(travel_minutes, int):
        return (
            False,
            f"Travel time must be integer, got {type(travel_minutes).__name__}",
        )
    if travel_minutes < 0:
        return False, f"Travel time cannot be negative: {travel_minutes}"
    if travel_minutes > 300:
        return False, f"Travel time > 300 min seems unrealistic: {travel_minutes}"
    return True, ""


def validate_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate all input fields and raise error if any are invalid.

    Args:
        data: Dictionary of patient data

    Returns:
        The same data dictionary if all validations pass

    Raises:
        ValidationError: If any field fails validation
    """
    errors = []

    # Validate demographics
    if "age" in data:
        valid, msg = _validate_age(data["age"])
        if not valid:
            errors.append(f"age: {msg}")

    if "weeks_pregnant" in data:
        valid, msg = _validate_pregnancy_weeks(data["weeks_pregnant"])
        if not valid:
            errors.append(f"weeks_pregnant: {msg}")

    if "height_cm" in data:
        valid, msg = _validate_height(data["height_cm"])
        if not valid:
            errors.append(f"height_cm: {msg}")

    if "weight_kg" in data:
        valid, msg = _validate_weight(data["weight_kg"])
        if not valid:
            errors.append(f"weight_kg: {msg}")

    # Validate vitals
    # Validate systolic and diastolic individually if provided, and validate the
    # pair if both are present (to check relational constraints like Systolic > Diastolic)
    if "systolic_bp" in data:
        sbp = data["systolic_bp"]
        if not isinstance(sbp, int):
            errors.append(f"systolic_bp: Systolic BP must be integer, got {type(sbp).__name__}")
        else:
            if sbp < 60:
                errors.append(f"systolic_bp: Systolic BP too low (< 60): {sbp}")
            if sbp > 220:
                errors.append(f"systolic_bp: Systolic BP too high (> 220): {sbp}")

    if "diastolic_bp" in data:
        dbp = data["diastolic_bp"]
        if not isinstance(dbp, int):
            errors.append(f"diastolic_bp: Diastolic BP must be integer, got {type(dbp).__name__}")
        else:
            if dbp < 40:
                errors.append(f"diastolic_bp: Diastolic BP too low (< 40): {dbp}")
            if dbp > 140:
                errors.append(f"diastolic_bp: Diastolic BP too high (> 140): {dbp}")

    if "systolic_bp" in data and "diastolic_bp" in data:
        valid, msg = _validate_blood_pressure(
            data["systolic_bp"], data["diastolic_bp"]
        )
        if not valid:
            errors.append(f"blood_pressure: {msg}")

    if "heart_rate" in data:
        valid, msg = _validate_heart_rate(data["heart_rate"])
        if not valid:
            errors.append(f"heart_rate: {msg}")

    if "body_temperature" in data:
        valid, msg = _validate_temperature(data["body_temperature"])
        if not valid:
            errors.append(f"body_temperature: {msg}")

    if "blood_sugar" in data:
        valid, msg = _validate_blood_sugar(data["blood_sugar"])
        if not valid:
            errors.append(f"blood_sugar: {msg}")

    if "oxygen_saturation" in data:
        valid, msg = _validate_oxygen_saturation(data["oxygen_saturation"])
        if not valid:
            errors.append(f"oxygen_saturation: {msg}")

    if "hemoglobin" in data:
        valid, msg = _validate_hemoglobin(data["hemoglobin"])
        if not valid:
            errors.append(f"hemoglobin: {msg}")

    # Validate binary fields
    binary_fields = [
        "previous_c_section",
        "previous_miscarriages",
        "multiple_pregnancy",
        "history_hypertension",
        "history_diabetes",
        "history_pre_eclampsia",
        "headache",
        "blurred_vision",
        "swollen_feet",
        "bleeding",
        "abdominal_pain",
        "fever",
        "reduced_fetal_movement",
        "severe_vomiting",
        "difficulty_breathing",
        "smoker",
        "alcohol",
    ]

    for field in binary_fields:
        if field in data:
            valid, msg = _validate_binary_field(data[field], field)
            if not valid:
                errors.append(f"{field}: {msg}")

    # Validate environment
    if "distance_to_hospital" in data:
        valid, msg = _validate_distance(data["distance_to_hospital"])
        if not valid:
            errors.append(f"distance_to_hospital: {msg}")

    if "travel_time_minutes" in data:
        valid, msg = _validate_travel_time(data["travel_time_minutes"])
        if not valid:
            errors.append(f"travel_time_minutes: {msg}")

    if errors:
        error_msg = "Input validation failed:\n" + "\n".join(errors)
        raise ValidationError(error_msg)

    return data
