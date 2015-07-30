import click
import rio_interpolate
import json

@click.command()
@click.argument('sampleraster', type=click.Path(exists=True))
@click.argument('geojson', default='-', required=False)
@click.option('--bidx', '-b', default=1)
@click.option('--outfile', '-o', default=None)
@click.pass_context
def interpolate(ctx, geojson, sampleraster, bidx, outfile):
    try:
        inGeoJSON = click.open_file(geojson).readlines()
    except IOError:
        inGeoJSON = [geojson]
    features = list(i for i in rio_interpolate.filterBadJSON(inGeoJSON))

    for feat in features:
        bounds = rio_interpolate.getBounds(features)

        ras_vals = rio_interpolate.loadRaster(sampleraster, bounds, bidx)
        output_values = rio_interpolate.interpolatePoints(
        ras_vals,
        rio_interpolate.parseLine(features[0]),
        bounds)

        feat['geometry']['coordinates'] = [f for f in rio_interpolate.addAttr(feat, output_values)]

    if outfile:
        with open(outfile, 'w') as oFile:
            oFile.write(json.dumps({
                "type": "FeatureCollection",
                "features": list(features)
                }))
    else:
        for feat in features:
            try:
                click.echo(json.dumps(feat).rstrip())
            except IOError as e:
                pass

if __name__ == '__main__':
    interpolate()
