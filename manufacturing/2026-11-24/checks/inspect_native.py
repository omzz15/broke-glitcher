"""Inspect native KiCad geometry and assembly pad layers."""
import json
from pathlib import Path
import wx
app = wx.App(False)
wx.Image.CleanUpHandlers()
import pcbnew as p
root = Path(__file__).resolve().parents[1]
b = p.LoadBoard(str(root / 'source/broke-glitcher.kicad_pcb'))
box = b.GetBoardEdgesBoundingBox()
print('EDGES', [p.ToMM(n) for n in [box.GetX(), box.GetY(), box.GetWidth(), box.GetHeight()]])
print('ORIGIN',b.GetDesignSettings().GetAuxOrigin())
for f in b.GetFootprints():
    if f.GetReference() in ['J1','U4','U6','Y1'] or f.IsDNP() or f.GetReference().startswith('JP'):
        pads=[(pad.GetNumber(),[p.LayerName(l) for l in [p.F_Paste,p.B_Paste] if pad.IsOnLayer(l)]) for pad in f.Pads()]
        print(f.GetReference(),f.GetValue(),pads)
app.Destroy()
