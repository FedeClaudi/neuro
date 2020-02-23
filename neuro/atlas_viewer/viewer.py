import os
import numpy as np

import napari

import neuro.atlas_viewer as atlas
from neuro.atlas_viewer.data_manager import structure_tree, template, annotated_volume

import matplotlib.image
# Read image 
image = '/Users/federicoclaudi/Documents/Github/BrainRender/Docs/Media/ZI_cartoon.png'
img = matplotlib.image.imread(image)


# ---------------------------------------------------------------------------- #
#                                     Utils                                    #
# ---------------------------------------------------------------------------- #

def get_structure_from_coords(coords):
    # Get brain regions from clicked voxel
    voxel = np.round(np.array(coords) ).astype(int)
    try:
        structure_id = annotated_volume[voxel[0], voxel[1], voxel[2]]
    except:
        return None

    # Each voxel in the annotation volume is annotated as specifically as possible
    structure = structure_tree.get_structures_by_id([structure_id])[0]
    
    if structure is None:
        structure = 'none'
    else:
        structure = structure['acronym']
    return structure


# ---------------------------------------------------------------------------- #
#                                   Callbacks                                  #
# ---------------------------------------------------------------------------- #

def mouse_click_callback(layer, event):
        coords = np.round(layer.coordinates).astype(int)

        structure = get_structure_from_coords(coords)

        msg = f'clicked at {coords} - structure: {structure}'
        layer.status = msg
        print(msg)




# ---------------------------------------------------------------------------- #
#                                    VIEWER                                    #
# ---------------------------------------------------------------------------- #
with napari.gui_qt():

    # ------------------------------- Atlas viewer ------------------------------- #
    viewer = napari.Viewer(ndisplay=2)

    # Add and orient data
    reference_layer = viewer.add_image(template, name='reference space', scale=[1, 1])
    labels_layer = viewer.add_labels(annotated_volume, name='brain_structures')

    if atlas.orientation.lower() == 'sagittal':
        viewer.dims.order =[2, 1, 0]
    elif atlas.orientation.lower() == 'top':
        viewer.dims.order =[1, 2, 0]
    # otherwise the default is coronal 

    # ? points
    # points = viewer.add_points(np.zeros((0, 3)), size=1)
    # points.mode = 'add'
    

    # ------------------------------ Callback funcs ------------------------------ #
    @reference_layer.mouse_drag_callbacks.append
    def layer_click_callback(layer, event):
        mouse_click_callback(layer, event)
    @labels_layer.mouse_drag_callbacks.append
    def layer_click_callback(layer, event):
        mouse_click_callback(layer, event)




    # ------------------------------- Slice viewer ------------------------------- #
    slice_viewer = napari.Viewer(ndisplay=2, title='slice viewer')

    slice_viewer.add_image(img)

# print("you clicked on:")
# print(points.data)
