import numpy as np
from sklearn.decomposition import PCA
import trimesh
import argparse


def orient_points(points):
    pca = PCA(n_components=3)
    pca.fit(points)
    components = pca.components_
    up = abs(components[2])

    z_axis = np.array([0, 0, 1])
    rotation_axis = np.cross(up, z_axis)
    rotation_axis /= np.linalg.norm(rotation_axis)
    cos_theta = np.dot(up, z_axis)
    sin_theta = np.sqrt(1 - cos_theta**2)
    K = np.array(
        [
            [0, -rotation_axis[2], rotation_axis[1]],
            [rotation_axis[2], 0, -rotation_axis[0]],
            [-rotation_axis[1], rotation_axis[0], 0],
        ]
    )
    mat = np.eye(3) + sin_theta * K + (1 - cos_theta) * np.dot(K, K)
    oriented_points = np.dot(points, mat.T)
    return oriented_points


def load_mesh(path):
    scene = trimesh.load(path)
    meshes = [
        geometry
        for geometry in scene.geometry.values()
        if isinstance(geometry, trimesh.Trimesh)
    ]

    mesh = meshes[0]
    if len(meshes) > 1:
        mesh = trimesh.util.concatenate(meshes)

    vertices = np.array(mesh.vertices)
    faces = np.array(mesh.faces)
    return vertices, faces


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    args = parser.parse_args()

    path = args.path
    vertices, faces = load_mesh(path)
    vertices = orient_points(vertices)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.export(path)
