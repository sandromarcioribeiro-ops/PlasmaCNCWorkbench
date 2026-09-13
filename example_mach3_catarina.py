from math import cos, pi, sin
from pathlib import Path

from plasma_cnc.gcode import PlasmaJob, loops_from_simple_polylines, save_mach3_gcode
from plasma_cnc.presets import MACH3_MILD_STEEL_3MM


def circle(cx, cy, radius, segments=40):
    return [
        (cx + radius * cos(2 * pi * i / segments), cy + radius * sin(2 * pi * i / segments))
        for i in range(segments)
    ]


def capsule(length=220.0, height=72.0, segments=32):
    radius = height / 2
    half = (length - height) / 2
    points = []
    for i in range(segments + 1):
        angle = pi / 2 + pi * i / segments
        points.append((-half + radius * cos(angle), radius * sin(angle)))
    for i in range(segments + 1):
        angle = -pi / 2 + pi * i / segments
        points.append((half + radius * cos(angle), radius * sin(angle)))
    return points


loops = loops_from_simple_polylines(
    internal_loops=[circle(-50.0, 0.0, 6.35), circle(68.0, 0.0, 6.35)],
    external_loops=[capsule()],
)

job = PlasmaJob(name="Catarina Router Corte Chapa - exemplo", loops=loops, preset=MACH3_MILD_STEEL_3MM)
output = Path(__file__).with_name("catarina_mach3_plasma.tap")
save_mach3_gcode(job, str(output))
print(output)

