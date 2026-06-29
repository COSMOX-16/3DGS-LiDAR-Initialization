import os
from pathlib import Path

TRANS_MATRIX_FILE = Path("Truck_trans.txt")
SFM_LOG_FILE = Path("Truck_COLMAP_SfM.log")
INPUT_PLY_FILE = Path("Truck.ply")

OUTPUT_SPARSE_DIR = Path("sparse/0")
IMAGES_TXT_OUT = OUTPUT_SPARSE_DIR / "images.txt"
CAMERAS_TXT_OUT = OUTPUT_SPARSE_DIR / "cameras.txt"
POINTS3D_PLY_OUT = OUTPUT_SPARSE_DIR / "points3D.ply"
VERIFICATION_HTML_OUT = Path("alignment_test.html")

#camera 
#this one if for the outdoor scenes in the Tank and Temples dataset
camera_width = 1920
camera_height = 1080
focal_x = 1150
focal_y = 1150
center_x = 960
center_y = 540

downsample_factor = 1

os.makedirs(OUTPUT_SPARSE_DIR, exist_ok=True)




