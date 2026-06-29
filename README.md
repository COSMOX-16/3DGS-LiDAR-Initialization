[ RAW INPUT ASSETS ]
      │
      ├─ COLMAP_SfM.log (C2W Tracking)
      ├─  trans.txt (Similarity Matrix)
      └─  Lidar.ply (800k+ Raw Point Cloud)
      │
      ▼
[ PYTHON PIPELINE ] ◂── ( config.py : Shared Parameters)
      │
      ├─  geometry.py
      │   └─ Calculates matrix alignment & Quaternions
      │
      ├─  process_cloud.py
      │   └─ Safely copies/downsamples binary mesh
      │
      └─  run_pipeline.py
          └─ Master execution controller
      │
      ▼
[ 3DGS TARGET: sparse/0/ ]
      │
      ├─  images.txt (W2C Poses)
      ├─  cameras.txt (Intrinsics)
      └─  points3D.ply (Cleaned Target Mesh)
      │
      ▼
[ FINAL VISUAL CHECKS]
      │
      └─  alignment_test.html (Interactive 3D Plot)



# LiDAR to 3DGS Metric Alignment Pipeline

##  Overview
This repository contains a modular, production-ready data processing pipeline designed to bridge the gap between unscaled Structure-from-Motion (SfM) camera tracking and metric-scale LiDAR scans. 

By applying a calculated similarity transformation to COLMAP-style camera logs, this pipeline mathematically synchronizes 2D image projections with a 3D physical point cloud. It automatically generates a `sparse/0/` directory formatted perfectly for **3D Gaussian Splatting (3DGS)** training, ensuring the network initializes with true real-world scale and geometry.

##  Pipeline Architecture

The pipeline has been refactored from experimental notebooks into a clean, modular Python architecture:

* **`config.py`** The central configuration hub. Contains all hardcoded I/O paths, downsampling factors, and exact camera intrinsics (Resolution, Focal Length, Optical Center) to prevent magic numbers in the core logic.
  
* **`geometry.py`** The mathematical core. Handles:
  * Matrix decomposition (extracting uniform scale, rotation, and translation from an affine transformation matrix).
  * Coordinate transformations mapping Camera-to-World (C2W) poses into physical LiDAR space.
  * Inversions mapping physical poses back to World-to-Camera (W2C) matrices.
  * Formatting Quaternions (converting from SciPy's `x,y,z,w` to COLMAP's strict `w,x,y,z` format).

* **`process_cloud.py`** The resource manager. Safely reads the massive raw LiDAR `.ply` file, applies decimation (downsampling) to prevent memory overload, standardizes attribute bindings (colors and normals), and writes a clean, optimized binary `points3D.ply` file for the 3DGS engine.

* **`run_pipeline.py`** The master execution controller. Orchestrates the geometry transforms and point cloud processing, and utilizes Plotly to render `alignment_test.html`—a lightweight, interactive 3D browser plot used for visual Quality Assurance (QA) of the camera paths before initiating costly GPU training.

## Prerequisites & Installation

Ensure you have Python 3.12+ installed. The pipeline relies on standard scientific and 3D processing libraries.

Install the required dependencies via `pip` or `uv`:
```bash
pip install numpy scipy plyfile plotly