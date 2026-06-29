import numpy as np
from pathlib import Path
from scipy.spatial.transform import Rotation as R
import config

def load_transformation_matrix():
    if not config.TRANS_MATRIX_FILE.exists():
        raise FileNotFoundError("Missing trans.txt")

    trans_matrix = np.loadtxt(config.TRANS_MATRIX_FILE)
    M_rot_scale = trans_matrix[:3, :3]
    t_trans = trans_matrix[:3, 3]

    #calculate the scalle

    scale = np.cbrt(np.linalg.det(M_rot_scale))
    R_trans_norm = M_rot_scale / scale

    return M_rot_scale , t_trans, R_trans_norm

def build_camera_structures(M_rot_scale , t_trans, R_trans_norm):
    if not config.SFM_LOG_FILE.exists():
        raise FileNotFoundError("Missing SFM log file")
    
    lines = config.SFM_LOG_FILE.read_text().splitlines()
    images_txt = []
    aligned_centers = []

    for i in range(0,len(lines),5):
        if i + 4>= len(lines):
            break

        block = lines[i:i+5]
        image_id = int(block[0].split()[0])
        
        M = np.array([block[1].split(), block[2].split(), block[3].split()], dtype = np.float64)
        R_log = M[:3,:3]
        t_log = M[:3,3]
        t_c2w_lidar = (M_rot_scale @ t_log) + t_trans
        aligned_centers.append(t_c2w_lidar)

        R_c2w_lidar = R_trans_norm @ R_log


        R_w2c = R_c2w_lidar.T
        t_w2c = -R_w2c @ t_c2w_lidar

        #convert to quanterion vectors

        q_xyzw = R.from_matrix(R_w2c).as_quat()
        qx, qy, qz, qw = q_xyzw

        filename = f"{image_id + 1:06d}.jpg"
         #image_id + 1 bcz the images are named 001, 002 .....
        images_txt.append(
            f"{image_id + 1} {qw} {qx} {qy} {qz} {t_w2c[0]} {t_w2c[1]} {t_w2c[2]} 1 {filename}\n\n") #double \n for leaving one line in between

    return images_txt, np.array(aligned_centers)






def write_files(images_txt):
    with open(config.IMAGES_TXT_OUT, "w") as f:
        f.write("#Aligned images with lidar cordinates \n")
        f.writelines(images_txt)

    with open(config.CAMERAS_TXT_OUT, "w") as f:
        f.write("# Camera Intrinsic Profiling Matrix\n")
        f.write(f"1 PINHOLE {config.camera_width} {config.camera_height} "
                f"{config.focal_x} {config.focal_y} {config.center_x} {config.center_y}\n")
                
    print("Camera and Image geometric text documents successfully updated.")

