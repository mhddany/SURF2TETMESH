import numpy as np
import pyvista as pv
import tetgen
import trimesh
import os

class Surf2TetMesh:
    """
    Convert STL surface mesh to tetrahedral FEM mesh and visualize normals
    """
    def __init__(self, stl_file):
        self.stl_file = stl_file
        self.load_stl()
        self.fem_mesh = None

    def load_stl(self):
        if not self.stl_file or not os.path.isfile(self.stl_file):
            raise ValueError("STL file path is empty or does not exist.")  
        
        """Load STL and convert to PyVista triangulated mesh"""
        tri_mesh = trimesh.load(self.stl_file)
        
        faces = tri_mesh.faces
        n_faces = faces.shape[0]
        faces_pv = np.hstack([np.full((n_faces,1),3), faces]).flatten()
        self.mesh = pv.PolyData(tri_mesh.vertices, faces_pv)
        print(f"Loaded STL: {self.stl_file}")
        
        # Visualize the STL mesh
        '''
        plotter = pv.Plotter()
        plotter.add_mesh(self.mesh, color='lightgray', show_edges=True)
        plotter.add_text("Original STL", font_size=12)
        plotter.show()
        '''

    def generate_fem(self, order=1, mindihedral=20, minratio=1.5, maxvolume=1.0):
        """Generate tetrahedral FEM mesh using TetGen"""
        tet = tetgen.TetGen(self.mesh)
        tet.tetrahedralize(order=order, mindihedral=mindihedral, minratio=minratio, maxvolume=maxvolume)
        self.fem_mesh = tet.grid
        print(f"Generated FEM mesh with {self.fem_mesh.n_cells} tetrahedra")

    def compute_surface_normals(self):
        """Compute centroids and normals of surface triangles"""
        surf = self.fem_mesh.extract_surface()
        nodes = surf.points
        faces_raw = surf.faces.reshape(-1,4)[:,1:]
        centroids = np.mean(nodes[faces_raw], axis=1)
        v1 = nodes[faces_raw[:,0]]
        v2 = nodes[faces_raw[:,1]]
        v3 = nodes[faces_raw[:,2]]
        normals = np.cross(v2 - v1, v3 - v1)
        normals /= np.linalg.norm(normals, axis=1)[:,np.newaxis]
        return centroids, normals, surf

    def plot_mesh_and_normals(self, scale=0.1):
        """Visualize FEM mesh and surface normals"""
        centroids, normals, surf = self.compute_surface_normals()
        plotter = pv.Plotter()
        plotter.add_mesh(surf, color=[0.7,0.7,0.9], show_edges=True, opacity=0.3)
        plotter.add_arrows(centroids, normals*scale, mag=1.0, color='red')
        plotter.add_axes()
        plotter.show_grid()
        plotter.show()
        
    def plot_surf_and_vol_mesh(self):
        """Visualize surface mesh and volumetric FEM mesh"""
        plotter = pv.Plotter(shape=(1,2))
        plotter.subplot(0,0)
        plotter.add_mesh(self.mesh, color='lightgray', show_edges=True)
        plotter.add_text("Original STL", font_size=12)

        plotter.subplot(0,1)
        plotter.add_mesh(self.fem_mesh, color='lightblue', show_edges=True)
        plotter.add_text("FEM Mesh (TetGen)", font_size=12)

        plotter.show()

    def save_fem_mesh(self, filename):
        """Save FEM mesh to file (VTK or other supported by PyVista/meshio)"""
        if self.fem_mesh is None:
            print("FEM mesh not generated yet!")
            return
        self.fem_mesh.save(filename)
        print(f"Saved FEM mesh to: {filename}")
