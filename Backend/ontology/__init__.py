"""
Cross-lingual pain ontology mapping and terminology alignment.
"""
from .pain_mapping import (
    CHINESE_PAIN_DESCRIPTORS,
    TEMPORAL_PATTERNS,
    ANATOMICAL_LOCATIONS,
    map_chinese_to_english,
    extract_temporal_pattern,
    extract_anatomical_location
)

__all__ = [
    'CHINESE_PAIN_DESCRIPTORS',
    'TEMPORAL_PATTERNS',
    'ANATOMICAL_LOCATIONS',
    'map_chinese_to_english',
    'extract_temporal_pattern',
    'extract_anatomical_location'
]
