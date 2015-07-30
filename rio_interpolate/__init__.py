#!/usr/bin/env python
import click
import json
import numpy as np
from scipy import interpolate
import rasterio as rio
import fiona
from rasterio import coords

__version__ = '0.0.0'


def filterBadJSON(feat):
    for f in feat:
        try:
            yield json.loads(f)
        except:
            pass

def getBounds(features):
    xy = np.vstack(list(f['geometry']['coordinates'] for f in features))

    return coords.BoundingBox(
        xy[:,0].min(),
        xy[:,1].min(),
        xy[:,0].max(),
        xy[:,1].max()
        )

def parseLine(feat):
    return np.array(feat['geometry']['coordinates'])

def addAttr(geoJSON, values):
    for f, v in zip(geoJSON['geometry']['coordinates'], values):
        for i, a in enumerate(v):
            f.append(a.item())
            yield f

def loadRaster(sampleraster, bounds, bidx):
    with rio.open(sampleraster) as src:
        upperLeft = src.index(bounds.left, bounds.top)
        lowerRight = src.index(bounds.right, bounds.bottom)

        out = np.zeros((1, lowerRight[0] - upperLeft[0] + 1, lowerRight[1] - upperLeft[1] + 1), dtype=src.meta['dtype'])
        return np.array([src.read(bidx, out=out, window=((upperLeft[0], lowerRight[0] + 1),(upperLeft[1], lowerRight[1] + 1)), boundless=True)[2:]])

def interpolatePoints(array, points, pointbounds):
    depth, rows, cols = array.shape

    y = np.linspace(pointbounds.bottom, pointbounds.top, rows)
    x = np.linspace(pointbounds.left, pointbounds.right, cols)

    return np.rot90(np.array(
        [interpolate.interpn((x, y), np.rot90(arr, k=3), points, bounds_error=False).astype(array.dtype) for arr in array]
        )[::-1], k=3)
