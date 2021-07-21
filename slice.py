#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from paraview.simple import *


parser = argparse.ArgumentParser(description='Slice cgns files.')

parser.add_argument('path', type=str, nargs='?', help='cgns file path', default='.')
parser.add_argument('-x', action='store_true', default=False,
                    help='Slice in the x direction')
parser.add_argument('-y', action='store_true', default=False,
                    help='Slice in the y direction')
parser.add_argument('-z', action='store_true', default=False,
                    help='Slice in the z direction')
parser.add_argument('--field',  type=str, default="Velocity",
                    help='Field to visualise')

parser.add_argument('--loc',  type=float, default=0,
                    help='Slice location in the slice normal direction')

args = parser.parse_args()

if args.x:
    slice_name = "x"
    Normal = [1, 0, 0]
    Origin = [args.loc, 0, 0]
if args.y:
    slice_name = "y"
    Normal = [0, 1, 0]
    Origin = [0, args.loc, 0]
if args.z:
    slice_name = "z"
    Normal = [0, 0, -1]
    Origin = [0, 0, args.loc]

field = args.field

cgnsfile = args.path

export_filename = "{}_slice_{}_{}.png".format(os.path.splitext(cgnsfile)[0],
                                              slice_name, 
                                              field)



solutionCgns = CGNSSeriesReader(registrationName='solution.cgns', FileNames=[cgnsfile])
solutionCgns.Bases = ['Base_Volume_elements']
solutionCgns.CellArrayStatus = []

solutionCgns.CellArrayStatus = [field]

renderView1 = GetActiveViewOrCreate('RenderView')

slice_obj = Slice(registrationName='slice_obj', Input=solutionCgns)
slice_obj.SliceType.Origin = Origin
slice_obj.SliceType.Normal = Normal

slice_objDisplay = Show(slice_obj, renderView1, 'GeometryRepresentation')

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
if field == "Velocity":
    ColorBy(slice_objDisplay, ('CELLS', field, 'Magnitude'))
else:
    ColorBy(slice_objDisplay, ('CELLS', field))

# rescale color and/or opacity maps used to include current data range
slice_objDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice_objDisplay.SetScalarBarVisibility(renderView1, True)

ArrayRange = slice_obj.CellData.GetArray(field).GetRange(-1)


variableLUT = GetColorTransferFunction(field)
variableLUT.RescaleTransferFunction(ArrayRange[0], ArrayRange[1])

# get layout
layout1 = GetLayout()
layout1.SetSize(1920, 1080)

renderView1.InteractionMode = '2D'

renderView1.CameraPosition = [0, 0, 0]
renderView1.CameraFocalPoint = Normal
renderView1.ResetCamera() 

# save screenshot
SaveScreenshot(export_filename, renderView1, ImageResolution=[1920, 1080])
print("{} saved".format(export_filename))


