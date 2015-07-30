rio-interpolate
===============

Interpolate raster values from GeoJSON geometry

Installation:
-------------

::

    git clone git@github.com:mapbox/rio-interpolate.git`

    cd rio-interpolate

    pip install -e .

Usage:
------

::

    fio cat {geojson} | rio interpolate {raster}
