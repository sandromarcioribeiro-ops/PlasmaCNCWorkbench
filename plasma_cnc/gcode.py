"""Mach3 plasma G-code generation."""

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from .presets import MACH3_MILD_STEEL_3MM, PlasmaPreset

Point = Tuple[float, float]


@dataclass(frozen=True)
class CutLoop:
    name: str
    points: Sequence[Point]
    inside: bool = False

    @property
    def closed_points(self) -> List[Point]:
        pts = list(self.points)
        if pts and pts[0] != pts[-1]:
            pts.append(pts[0])
        return pts


@dataclass(frozen=True)
class PlasmaJob:
    name: str
    loops: Sequence[CutLoop]
    preset: PlasmaPreset = MACH3_MILD_STEEL_3MM

    @property
    def ordered_loops(self) -> List[CutLoop]:
        internal = [loop for loop in self.loops if loop.inside]
        external = [loop for loop in self.loops if not loop.inside]
        return internal + external


def _fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def generate_mach3_gcode(job: PlasmaJob) -> str:
    lines: List[str] = [
        "(Gerado pelo Plasma CNC Workbench)",
        f"(Projeto: {job.name})",
        f"(Preset: {job.preset.name})",
        "(ATENCAO: testar primeiro com a tocha desligada)",
        "G21 (milimetros)",
        "G90 (coordenadas absolutas)",
        "G17 (plano XY)",
        f"F{_fmt(job.preset.feed_mm_min)}",
        f"G0 Z{_fmt(job.preset.safe_z_mm)}",
    ]

    for index, loop in enumerate(job.ordered_loops, start=1):
        pts = loop.closed_points
        if len(pts) < 2:
            continue

        start_x, start_y = pts[0]
        cut_kind = "interno" if loop.inside else "externo"
        lines.extend(
            [
                "",
                f"(Corte {index}: {loop.name} - {cut_kind})",
                f"G0 Z{_fmt(job.preset.safe_z_mm)}",
                f"G0 X{_fmt(start_x)} Y{_fmt(start_y)}",
                f"G0 Z{_fmt(job.preset.pierce_z_mm)}",
                "M3 (liga tocha)",
                f"G4 P{_fmt(job.preset.pierce_delay_s)} (tempo de perfuracao)",
                f"G1 Z{_fmt(job.preset.cut_z_mm)}",
            ]
        )

        for x, y in pts[1:]:
            lines.append(f"G1 X{_fmt(x)} Y{_fmt(y)}")

        lines.extend(
            [
                "M5 (desliga tocha)",
                f"G0 Z{_fmt(job.preset.safe_z_mm)}",
            ]
        )

    lines.extend(["", "M5", "G0 Z{0}".format(_fmt(job.preset.safe_z_mm)), "M30"])
    return "\n".join(lines) + "\n"


def save_mach3_gcode(job: PlasmaJob, output_path: str) -> None:
    with open(output_path, "w", encoding="ascii", newline="\n") as handle:
        handle.write(generate_mach3_gcode(job))


def loops_from_simple_polylines(
    internal_loops: Iterable[Sequence[Point]],
    external_loops: Iterable[Sequence[Point]],
) -> List[CutLoop]:
    loops: List[CutLoop] = []
    for i, points in enumerate(internal_loops, start=1):
        loops.append(CutLoop(name=f"furo/recorte interno {i}", points=points, inside=True))
    for i, points in enumerate(external_loops, start=1):
        loops.append(CutLoop(name=f"contorno externo {i}", points=points, inside=False))
    return loops

