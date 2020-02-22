import os
import numpy as np

from skimage import data

import napari
from allensdk.core.reference_space_cache import ReferenceSpaceCache


import neuro.atlas_viewer as atlas

# ------------------------- Download/Load atlas data ------------------------- #

spacecache = ReferenceSpaceCache(
    manifest=os.path.join(atlas.cache_dir, "manifest.json"),  # downloaded files are stored relative to here
    resolution=atlas.resolution,
    reference_space_key="annotation/ccf_2017"  # use the latest version of the CCF
    )
template = spacecache.get_template_volume()[0]
annotated_volume, _ = spacecache.get_annotation_volume()

# --------------------------------- Visualise -------------------------------- #

with napari.gui_qt():

    viewer = napari.Viewer(ndisplay=2)
    # add the volume
    viewer.add_image(template, name='reference space', scale=[1, 1])
    viewer.add_labels(annotated_volume, name='brain_structures')

    points = viewer.add_points(np.zeros((0, 3)), size=1)
    points.mode = 'add'
    
    if atlas.orientation.lower() == 'sagittal':
        viewer.dims.order =[2, 1, 0]
    elif atlas.orientation.lower() == 'top':
        viewer.dims.order =[1, 2, 0]
    # otherwise the default is coronal 

    # @viewer.mouse_press_callbacks.append
    # def test(viewer, event):
    #     print(event)

print("you clicked on:")
print(points.data)

a = 1