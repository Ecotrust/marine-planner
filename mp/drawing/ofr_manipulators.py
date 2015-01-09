from scenarios.models import GridCell
from django.contrib.gis.db.models.aggregates import Union

def clip_to_grid(geom):
    intersection = GridCell.objects.filter(centroid__intersects=geom)

    if len(intersection) == 1:
        clipped_shape = intersection[0].geometry.envelope
    else:
        new_shape = intersection.aggregate(Union('geometry'))        
        clipped_shape = new_shape['geometry__union'];

    return clipped_shape