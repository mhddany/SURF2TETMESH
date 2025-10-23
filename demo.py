from surf2tetmesh import Surf2TetMesh
import tkinter as tk
from tkinter import filedialog

def main():
    # Initialize Tkinter root
    root = tk.Tk()
    root.withdraw()  # hide main window

    # Select STL file
    stl_file = filedialog.askopenfilename(title="Select STL file", filetypes=[("STL files","*.stl")])
    if not stl_file:
        print("No STL file selected. Exiting.")
        return

    # Create object and generate FEM mesh
    fem_obj = Surf2TetMesh(stl_file)
    fem_obj.generate_fem()
    
    # compare surface and volumetric mesh
    fem_obj.plot_surf_and_vol_mesh()  

    # Plot mesh and normals
    fem_obj.plot_mesh_and_normals(scale=0.1)
    
    # Save FEM mesh
    save_file = filedialog.asksaveasfilename(title="Save FEM mesh", defaultextension=".vtu",
                                             filetypes=[("VTK Unstructured Grid","*.vtu"), 
                                                        ("VTK Legacy","*.vtk")])
    if save_file:
        fem_obj.save_fem_mesh(save_file)
    else:
        print("FEM mesh not saved.")
if __name__ == "__main__":
    main()
