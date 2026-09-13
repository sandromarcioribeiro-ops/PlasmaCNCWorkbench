from plasma_cnc.gcode import CutLoop, PlasmaJob, generate_mach3_gcode


def test_internal_cuts_are_before_external_cut():
    job = PlasmaJob(
        name="teste",
        loops=[
            CutLoop("contorno", [(0, 0), (10, 0), (10, 10), (0, 10)], inside=False),
            CutLoop("furo", [(4, 4), (6, 4), (6, 6), (4, 6)], inside=True),
        ],
    )

    code = generate_mach3_gcode(job)

    assert code.index("furo - interno") < code.index("contorno - externo")


def test_each_cut_turns_torch_on_and_off():
    job = PlasmaJob(
        name="teste",
        loops=[
            CutLoop("furo", [(4, 4), (6, 4), (6, 6), (4, 6)], inside=True),
            CutLoop("contorno", [(0, 0), (10, 0), (10, 10), (0, 10)], inside=False),
        ],
    )

    code = generate_mach3_gcode(job)

    assert code.count("M3 (liga tocha)") == 2
    assert code.count("M5 (desliga tocha)") == 2
    assert "G4 P0.7" in code

