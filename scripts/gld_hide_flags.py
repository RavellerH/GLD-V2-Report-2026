# -*- coding: utf-8 -*-
"""Display switches shared by the certification-document builders.

HIDE_SIDE_ANTENNA: withhold every figure that shows the superseded antenna position (antenna on the SIDE of the
base enclosure). The current production unit has the antenna on the top face of the base. Set to False to
restore the figures.
"""
HIDE_SIDE_ANTENNA = True

# image files (cert_doc_photos / cert_doc_drawings / instruction_manual_cad)
SIDE_ANTENNA_FILES = {
    "3._Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg",
    "Casing_Belakang.jpg",
    "bracket-mounting-drawing.png",
    "gld_atex_case_v3_dimensioned.png",
}
# drawing-register references in Section 2.6.a.1
SIDE_ANTENNA_MREFS = {"M-A1", "M-A2", "M-B1", "M-B2", "M-B3", "M-B4", "M-B5", "M-B6", "M-B7", "M-E7", "M-E9"}

WITHHELD_NOTE = ("Withheld in this issue: these drawings show a superseded antenna position (antenna on the side of "
                 "the base enclosure). The current production unit has the antenna on the top face of the base "
                 "(Figures 4-118, 4-124 and 4-125). Revised drawings will be issued.")


def hidden_file(fn):
    return HIDE_SIDE_ANTENNA and fn in SIDE_ANTENNA_FILES


def hidden_ref(ref):
    return HIDE_SIDE_ANTENNA and ref in SIDE_ANTENNA_MREFS
