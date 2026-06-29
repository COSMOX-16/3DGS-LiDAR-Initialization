import numpy as np
from plyfile import PlyData, PlyElement
import config

def downsample():
    if not config.INPUT_PLY_FILE.exists():
        raise FileNotFoundError(".ply does not exist")

    ply_data = PlyData.read(config.INPUT_PLY_FILE)
    vertex = ply_data['vertex']
    
    decimation_factor = config.downsample_factor

    x = vertex['x'][::decimation_factor]
    y = vertex['y'][::decimation_factor]
    z = vertex['z'][::decimation_factor]

    has_colors = 'red' in vertex.data.dtype.names
    red = vertex['red'][::decimation_factor] if has_colors else np.ones_like(x, dtype=np.uint8) * 128
    green = vertex['green'][::decimation_factor] if has_colors else np.ones_like(x, dtype=np.uint8) * 128
    blue = vertex['blue'][::decimation_factor] if has_colors else np.ones_like(x, dtype=np.uint8) * 128
    
    
    has_normals = 'nx' in vertex.data.dtype.names
    nx = vertex['nx'][::decimation_factor] if has_normals else np.zeros_like(x)
    ny = vertex['ny'][::decimation_factor] if has_normals else np.zeros_like(x)
    nz = vertex['nz'][::decimation_factor] if has_normals else np.zeros_like(x)

    num_points = len(x)
    print(f"[+] Post-decimation dataset density: {num_points} vertices.")
    
    # Construct structured 
    vertex_data = np.empty(num_points, dtype=[
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4'),
        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')
    ])
    
    # Bind typed properties securely to array elements
    vertex_data['x'] = x.astype(np.float32)
    vertex_data['y'] = y.astype(np.float32)
    vertex_data['z'] = z.astype(np.float32)
    vertex_data['nx'] = nx.astype(np.float32)
    vertex_data['ny'] = ny.astype(np.float32)
    vertex_data['nz'] = nz.astype(np.float32)
    vertex_data['red'] = red
    vertex_data['green'] = green
    vertex_data['blue'] = blue
    
    # Package 
    print(f" Encoding binary PLY elements to destination path......")
    el = PlyElement.describe(vertex_data, 'vertex')
    PlyData([el], text=False).write(config.POINTS3D_PLY_OUT)
    
    print(f"Optimization successful! Structured elements written to: {config.POINTS3D_PLY_OUT}")
    return np.vstack([vertex_data['x'], vertex_data['y'], vertex_data['z']]).T