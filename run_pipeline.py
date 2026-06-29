
import plotly.graph_objects as go
import geometry
import process_cloud
import config

def generate_browser_verification(lidar_points, aligned_centers):
    
    print(" Launching verification visualization matrix graphics...")
    
    # Further subset points down for lightweight browser rendering engine safety
    visualization_points = lidar_points[::10] 
    
    trace_lidar = go.Scatter3d(
        x=visualization_points[:, 0], y=visualization_points[:, 1], z=visualization_points[:, 2],
        mode='markers', marker=dict(size=1, color='lightgray', opacity=0.4),
        name='Metric LiDAR Target Mesh'
    )

    trace_cameras = go.Scatter3d(
        x=aligned_centers[:, 0], y=aligned_centers[:, 1], z=aligned_centers[:, 2],
        mode='markers', marker=dict(size=5, color='lime', opacity=1.0),
        name='Synchronized Camera Paths'
    )

    layout = go.Layout(
        title='Production Data Review: Camera Optimization Paths inside Metric Space',
        scene=dict(aspectmode='data', bgcolor='white'),
        paper_bgcolor='black',
        font=dict(color='white'),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    fig = go.Figure(data=[trace_lidar, trace_cameras], layout=layout)
    fig.write_html(config.VERIFICATION_HTML_OUT)
    print(f"[+] Quality assurance plot written cleanly to: {config.VERIFICATION_HTML_OUT}")

def main():
    print(" STARTING DENSE DATASET PRODUCTION PIPELINE RUN \n")
    
    try:
        #geometry transforms
        M_rot_scale, t_trans, R_trans_norm = geometry.load_transformation_matrix()
        images_txt_lines, aligned_centers = geometry.build_camera_structures(
            M_rot_scale, t_trans, R_trans_norm
        )
        geometry.write_files(images_txt_lines)
        
        # Downsample the point cloud
        clean_lidar_matrix = process_cloud.downsample()
        
        # check in browser
        generate_browser_verification(clean_lidar_matrix, aligned_centers)
        
        print("\n PIPELINE EXECUTION SUCCESSFUL — READY FOR 3DGS TRAINING ")
        
    except Exception as e:
        print(f"\n Pipeline terminated due to critical compilation failure: {str(e)}")

if __name__ == "__main__":
    main()