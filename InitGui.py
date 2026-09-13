"""GUI registration for the Plasma CNC workbench."""

import os

import FreeCAD as App
import FreeCADGui as Gui


def _workbench_dir():
    loaded_file = globals().get("__file__")
    if loaded_file:
        return os.path.dirname(os.path.abspath(loaded_file))
    return os.path.join(App.getUserAppDataDir(), "Mod", "PlasmaCNCWorkbench")


class PlasmaCNCWorkbench(Gui.Workbench):
    MenuText = "Plasma CNC"
    ToolTip = "Preparar cortes de plasma CNC e gerar G-code Mach3"
    Icon = os.path.join(_workbench_dir(), "resources", "plasma_cnc.svg")

    def Initialize(self):
        from plasma_cnc.commands import PlasmaCNCGenerateSampleCommand, PlasmaCNCShowGuideCommand

        Gui.addCommand("PlasmaCNC_ShowGuide", PlasmaCNCShowGuideCommand())
        Gui.addCommand("PlasmaCNC_GenerateSample", PlasmaCNCGenerateSampleCommand())
        commands = ["PlasmaCNC_ShowGuide", "PlasmaCNC_GenerateSample"]
        self.appendToolbar("Plasma CNC", commands)
        self.appendMenu("Plasma CNC", commands)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(PlasmaCNCWorkbench())
