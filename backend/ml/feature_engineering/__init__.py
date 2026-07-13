"""Feature engineering module for maternal health risk prediction."""

from .calculators import (
    calculate_bmi,
    calculate_map,
    calculate_pulse_pressure,
    calculate_gestational_trimester,
    count_symptoms,
    compute_age_group,
)
from .transformers import (
    transform_bmi_category,
    transform_bp_category,
    transform_age_group_label,
    transform_trimester_label,
)
from .validators import validate_input
from .encoders import (
    encode_bmi_category,
    encode_bp_category,
    encode_trimester,
    encode_urban_rural,
)
from .feature_pipeline import engineer_features

__all__ = [
    "calculate_bmi",
    "calculate_map",
    "calculate_pulse_pressure",
    "calculate_gestational_trimester",
    "count_symptoms",
    "compute_age_group",
    "transform_bmi_category",
    "transform_bp_category",
    "transform_age_group_label",
    "transform_trimester_label",
    "validate_input",
    "encode_bmi_category",
    "encode_bp_category",
    "encode_trimester",
    "encode_urban_rural",
    "engineer_features",
]

