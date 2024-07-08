import argparse
import numpy as np
from plyfile import PlyData
import trimesh


def ply_to_glb(input_ply, output_glb):
    ply = PlyData.read(input_ply)
    vertices = np.array([(v["x"], v["y"], v["z"]) for v in ply["vertex"]])
    faces = np.array([f[0] for f in ply["face"]])
    colors = (
        np.array([(v["red"], v["green"], v["blue"]) for v in ply["vertex"]]) / 255.0
    )
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_colors=colors)
    mesh.export(output_glb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("output", type=str)
    args = parser.parse_args()
    ply_to_glb(args.input, args.output)
