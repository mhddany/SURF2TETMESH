# Surf2TetMesh

![Python](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Convert any STL surface mesh into a tetrahedral FEM mesh using Python.  
Surf2TetMesh visualizes the mesh and surface normals interactively, making it ideal for engineering, biomechanics, and computational simulations.

---

## Demo

![Demo](examples/demo.gif)  
*Interactive visualization of STL → tetrahedral FEM mesh → surface normals.*

---

## Features

- Load any STL file and convert to triangulated mesh
- Generate tetrahedral FEM mesh using TetGen
- Visualize mesh and surface normals interactively
- Adjustable mesh fineness via `maxvolume`
- Save FEM mesh in VTK format

---

## Installation

```powershell
# Clone the repository
git clone https://github.com/yourusername/surf2tetmesh.git
cd surf2tetmesh

# Create Python 3.10 virtual environment
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
