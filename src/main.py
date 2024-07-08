import argparse
from orient_glb import load_mesh, orient_points
from ply2glb import ply_to_glb

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("output", type=str)
    args = parser.parse_args()
    ply_to_glb(args.input, args.output)

    mesh = load_mesh(args.output)
    vertices = orient_points(mesh.vertices)
    mesh.vertices = vertices
    mesh.export(args.output)
