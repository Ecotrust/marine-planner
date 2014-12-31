from madrona.manipulators.manipulators import BaseManipulator, manipulatorsDict
from scenarios.models import GridCell
from madrona.common.utils import LargestPolyFromMulti
from django.contrib.gis.geos import GEOSGeometry

very_small_area = .0000000001

class ClipToPlanningGrid(BaseManipulator):

    def __init__(self, target_shape, **kwargs):
        self.zero = very_small_area
        self.target_shape = target_shape
        # target = GEOSGeometry(shape)

    def manipulate(self):

        from scenarios.models import GridCell
        from django.contrib.gis.db.models.aggregates import Union

        geom = GEOSGeometry(self.target_shape, srid=3857)
        intersection = GridCell.objects.filter(centroid__intersects=geom)

        if len(intersection) == 1:
        	clipped_shape = intersection[0].geometry.envelope
    	else:
	        new_shape = intersection.aggregate(Union('geometry'))        
        	clipped_shape = new_shape['geometry__union'];

        # return new_shape['geometry__union']
        if clipped_shape and clipped_shape.area <= self.zero:
            largest_poly = None
        else: #there was overlap
            largest_poly = LargestPolyFromMulti(clipped_shape)
    	
        status_html = self.do_template("0")
        return self.result(clipped_shape, status_html)

    	# return self.target_shape
        
    class Options:    
        name = 'ClipToPlanningGrid'
        display_name = 'Clipping to Planning Grid'
        description = 'Clips your drawing to the individual cells of the Planning Grid'
        supported_geom_fields = ['PolygonField']

        html_templates = {
            '0':'manipulators/shape_clip.html', 
            '2':'manipulators/outside_shape.html', 
        }

manipulatorsDict[ClipToPlanningGrid.Options.name] = ClipToPlanningGrid      