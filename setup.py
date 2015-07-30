from codecs import open as codecs_open
from setuptools import setup, find_packages


# Parse the version from the fiona module.
with open('rio_interpolate/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            break

# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='rio-interpolate',
      version=version,
      description=u"Interpolate raster values from GeoJSON geometry",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Damon Burgett",
      author_email='damon@mapbox.com',
      url='https://github.com/mapbox/rio-interpolate',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'rasterio>=0.23',
          'scipy',
          'fiona'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [rasterio.rio_commands]
      interpolate=rio_interpolate.scripts.cli:interpolate
      """      )
