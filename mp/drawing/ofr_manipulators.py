from scenarios.models import GridCell
from django.contrib.gis.db.models.aggregates import Union

def clip_to_grid(geom):
    intersection = intersecting_cells(geom)

    if len(intersection) == 1:
        clipped_shape = intersection[0].geometry.envelope
    else:
        new_shape = intersection.aggregate(Union('geometry'))        
        clipped_shape = new_shape['geometry__union'];

    return clipped_shape

def intersecting_cells(geom):
	return GridCell.objects.filter(centroid__intersects=geom)