"""Ready-to-use plasma presets.

Values are conservative starting points and must be validated on scrap material.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PlasmaPreset:
    name: str
    kerf_mm: float
    feed_mm_min: float
    pierce_delay_s: float
    safe_z_mm: float
    pierce_z_mm: float
    cut_z_mm: float


MACH3_MILD_STEEL_3MM = PlasmaPreset(
    name="Mach3 Aco carbono 3mm - inicial",
    kerf_mm=1.2,
    feed_mm_min=1200.0,
    pierce_delay_s=0.7,
    safe_z_mm=5.0,
    pierce_z_mm=2.0,
    cut_z_mm=1.5,
)

MACH3_MILD_STEEL_5MM = PlasmaPreset(
    name="Mach3 Aco carbono 5mm - inicial",
    kerf_mm=1.4,
    feed_mm_min=850.0,
    pierce_delay_s=1.0,
    safe_z_mm=5.0,
    pierce_z_mm=2.2,
    cut_z_mm=1.5,
)

DEFAULT_PRESETS = [MACH3_MILD_STEEL_3MM, MACH3_MILD_STEEL_5MM]

