import os
import numpy as np

import napari
from allensdk.core.reference_space_cache import ReferenceSpaceCache
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

import neuro.atlas_viewer as atlas

# ------------------------- Mouse connectivity cache ------------------------- #
mcc = MouseConnectivityCache(manifest_file=os.path.join(atlas.mouse_connectivity_cache, "manifest.json"))
structure_tree = mcc.get_structure_tree()

# ------------------------- Download/Load atlas data ------------------------- #

spacecache = ReferenceSpaceCache(
	manifest=os.path.join(atlas.cache_dir, "manifest.json"),  # downloaded files are stored relative to here
	resolution=atlas.resolution,
	reference_space_key="annotation/ccf_2017"  # use the latest version of the CCF
	)
template = spacecache.get_template_volume()[0]
annotated_volume, _ = spacecache.get_annotation_volume()
