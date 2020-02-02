#!/usr/bin/env python

import argparse
from pathlib import Path
import math

import torch
import numpy as np
from PIL import Image

import tenviz
import tenviz.io
import tenviz.geometry

_SHADER_PATH = Path(__file__).parent


def generate_cylindrical_texcoord(mesh):
    """
    Generates cylindrical texture coordinates for the mesh.
    """
    texcoords = torch.zeros(mesh.verts.size(0), 2)

    texcoords[:, 0] = math.pi + torch.atan2(mesh.verts[:, 2], mesh.verts[:, 0])

    ymin = mesh.verts[:, 1].min()
    ymax = mesh.verts[:, 1].max()

    texcoords[:, 1] = (mesh.verts[:, 1] - ymin) / (ymax - ymin)

    return texcoords*32


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mesh_file", metavar="mesh-file",
                        help="Input mesh file")
    args = parser.parse_args()

    context = tenviz.Context()
    geo = tenviz.io.read_3dobject(args.mesh_file).torch()

    geo.normals = tenviz.geometry.compute_normals(geo.verts, geo.faces)
    texcoords = generate_cylindrical_texcoord(geo)

    hatch_files = (_SHADER_PATH / 'assets').glob("h*.png")
    hatch_files = sorted(hatch_files)

    with context.current():
        hatch_texs = []
        for img_file in hatch_files:
            image = torch.from_numpy(
                np.array(Image.open(str(img_file)).convert('RGB')))
            hatch_texs.append(tenviz.tex_from_tensor(image))

        draw = tenviz.DrawProgram(tenviz.DrawMode.Triangles,
                                  vert_shader_file=_SHADER_PATH / "hatching.vert",
                                  frag_shader_file=_SHADER_PATH / "hatching.frag",
                                  ignore_missing=True)

        num_tones = min(6, len(hatch_texs))
        # Shared between shaders
        draw['NumTones'] = num_tones
        draw['LightPos'] = torch.tensor([0.0, 10.0, 10.0])

        # Vertex shader
        draw['in_position'] = geo.verts
        draw['in_normal'] = geo.normals
        draw['in_texcoord'] = texcoords

        draw['Modelview'] = tenviz.MatPlaceholder.Modelview
        draw['ProjectionModelview'] = tenviz.MatPlaceholder.ProjectionModelview
        draw['NormalModelview'] = tenviz.MatPlaceholder.NormalModelview

        # Fragment shader
        draw['LightAmbient'] = torch.tensor([1.0, 1.0, 1.0])
        draw['LightDiffuse'] = torch.tensor([1.0, 1.0, 1.0])
        draw['Ambient'] = torch.tensor([0.8, 0.7, 0.2123])
        draw['Diffuse'] = torch.tensor([0.9, 0.125, 0.583])

        for k in range(num_tones):
            draw['hatches[{}]'.format(k)] = hatch_texs[k]

        draw.indices.from_tensor(geo.faces)

    viewer = context.viewer([draw], tenviz.CameraManipulator.TrackBall)
    viewer.title = "Hatching shading"
    while True:
        key = viewer.wait_key(1)
        if key < 0:
            break


if __name__ == '__main__':
    _main()
