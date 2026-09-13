"""GUI registration for the Plasma CNC workbench."""

import FreeCADGui as Gui


class PlasmaCNCWorkbench(Gui.Workbench):
    MenuText = "Plasma CNC"
    ToolTip = "Preparar cortes de plasma CNC e gerar G-code Mach3"

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
