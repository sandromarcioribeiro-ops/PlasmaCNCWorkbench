"""FreeCAD GUI commands for the Plasma CNC workbench."""

import os
from math import cos, pi, sin
from textwrap import dedent

from .gcode import PlasmaJob, loops_from_simple_polylines, save_mach3_gcode
from .presets import MACH3_MILD_STEEL_3MM


def _qt():
    try:
        from PySide import QtGui

        return QtGui
    except ImportError:
        from PySide2 import QtWidgets

        return QtWidgets


def _icon_path():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "resources", "plasma_cnc.svg")


def _circle(cx, cy, radius, segments=40):
    return [
        (cx + radius * cos(2 * pi * i / segments), cy + radius * sin(2 * pi * i / segments))
        for i in range(segments)
    ]


def _capsule(length=220.0, height=72.0, segments=32):
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


class PlasmaCNCShowGuideCommand:
    def GetResources(self):
        return {
            "MenuText": "Guia Plasma Mach3",
            "ToolTip": "Mostra o passo a passo inicial para gerar corte plasma Mach3",
            "Pixmap": _icon_path(),
        }

    def Activated(self):
        QtGui = _qt()
        message = dedent(
            """
            Plasma CNC Workbench - MVP

            Fluxo recomendado:
            1. Selecione a face superior da chapa.
            2. Gere ou selecione os contornos 2D.
            3. Classifique furos/recortes como INTERNOS.
            4. Classifique a borda da peca como EXTERNA.
            5. Use preset Mach3 Plasma.
            6. Gere o G-code e teste primeiro com a tocha desligada.

            Esta primeira versao ja tem o gerador Mach3 no codigo.
            A proxima etapa sera ligar esta tela a selecao real da face no FreeCAD.
            """
        ).strip()

        QtGui.QMessageBox.information(None, "Plasma CNC", message)

    def IsActive(self):
        return True


class PlasmaCNCGenerateSampleCommand:
    def GetResources(self):
        return {
            "MenuText": "Gerar exemplo Mach3",
            "ToolTip": "Gera um G-code Mach3 de exemplo com furos primeiro e contorno por ultimo",
            "Pixmap": _icon_path(),
        }

    def Activated(self):
        QtGui = _qt()
        path, _selected_filter = QtGui.QFileDialog.getSaveFileName(
            None,
            "Salvar G-code Mach3",
            "catarina_mach3_plasma.tap",
            "Mach3 G-code (*.tap *.nc);;Todos os arquivos (*.*)",
        )
        if not path:
            return

        loops = loops_from_simple_polylines(
            internal_loops=[_circle(-50.0, 0.0, 6.35), _circle(68.0, 0.0, 6.35)],
            external_loops=[_capsule()],
        )
        job = PlasmaJob(
            name="Catarina Router Corte Chapa - exemplo",
            loops=loops,
            preset=MACH3_MILD_STEEL_3MM,
        )
        save_mach3_gcode(job, path)
        QtGui.QMessageBox.information(
            None,
            "Plasma CNC",
            "G-code Mach3 gerado.\n\nTeste primeiro no Mach3 com a tocha desligada.",
        )

    def IsActive(self):
        return True
