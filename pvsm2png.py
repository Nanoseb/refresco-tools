#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Export png from cgns and paraview state file
# Usage:
# pvpython pvsm2png.py statefile.pvsm solution.cgns
# MIT license: Sebastien Lemaire

import os
import sys
import xml.etree.ElementTree as ET
from paraview.simple import *


def usage():
    print("""Render image from state file (.pvsm) and cgns data
Usage:
pvpython {} state_file.pvsm solution.cgns""".format(sys.argv[0]))
    exit()

if len(sys.argv) < 3:
    usage()

if sys.argv[1].endswith(".pvsm"):
    state_file = sys.argv[1]
    cgns_file = sys.argv[2]
elif  sys.argv[2].endswith(".pvsm"):
    state_file = sys.argv[2]
    cgns_file = sys.argv[1]
else:
    print(".pvsm file not found")
    usage()

export_filename = "{}_export.png".format(os.path.splitext(state_file)[0])

# Find source name in state file
state_root = ET.parse(state_file)

sources = state_root.findall("ServerManagerState/ProxyCollection[@name='sources']/Item")
source_name = None
for source in sources[::-1]:
    if source.attrib['name'].endswith(".cgns"):
        source_name = source.attrib['name']
        break

if source_name == None:
    source_name = state_root.find("ServerManagerState/ProxyCollection[@name='sources']/Item[last()]").attrib['name']

source_name = source_name.replace(".", "")
source_name = source_name.replace("-", "")
kwargs = {source_name+"FileNames": [cgns_file]}

# Load state file in paraview
print("Loading {} in ParaView using {} state file".format(cgns_file, state_file))
LoadState(state_file, LoadStateDataFileOptions='Choose File Names',
          DataDirectory=os.path.splitext(cgns_file)[0], **kwargs)

# find view
renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

# save screenshot
SaveScreenshot(export_filename, renderView1) 
print("{} saved".format(export_filename))

