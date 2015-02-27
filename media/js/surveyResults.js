
var app = app || {};

app.surveyResults = (function() {

	// var surveyLayerNames = ['All Activities', 'Boating', 'Recreational fishing', 'Commercial fishing', 'SCUBA diving by boat', 'SCUBA diving from shore (includes kayak)', 'Snorkel\/freediving from shore (includes kayak)', 'Snorkel\/freediving from vessel', 'Watersports'];
	var surveyLayerNames = ['All Activities', 'Boater Use', 'Commercial Fishing Use', 'Extractive Diving Use', 'Recreational Fishing Use', 'Research Use', 'SCUBA Diving Use', 'Spearfishing Use', 'Water Sports']

	var bins = [{
		'color': '#F8FAB9',
		'label': '1 - 3',
		'lower': 1,
		'upper': 3
	},
	{
		'color': '#F6DB87',
		'label': '4 - 10',
		'lower': 4,
		'upper': 10
	},
	{
		'color': '#F49E5A',
		'label': '11 - 27',
		'lower': 11,
		'upper': 27
	},
	{
		'color': '#DC4041',
		'label': '28 - 569',
		'lower': 28,
		'upper': 569
	}];

	var legend = {'colors': []};
    legend.colors.push({'color': bins[0].color, 'label': bins[0].label});
    legend.colors.push({'color': bins[1].color, 'label': bins[1].label});            
    legend.colors.push({'color': bins[2].color, 'label': bins[2].label});
    legend.colors.push({'color': bins[3].color, 'label': bins[3].label});

	var getSurveyStylingRules = function(property) {
		if (property === 'All Activities') {
			property = 'Total Activity Days';
		}
	    var first = new OpenLayers.Rule({
	        filter: new OpenLayers.Filter.Comparison({
	            type: OpenLayers.Filter.Comparison.BETWEEN,
	            property: property,
	            lowerBoundary: bins[0].lower,
	            upperBoundary: bins[0].upper
	        }),
	        symbolizer: {
	            fillColor: bins[0].color,
	            fillOpacity: .8,
	            strokeWidth: 0
	        }
	    });
	    var second = new OpenLayers.Rule({
	        filter: new OpenLayers.Filter.Comparison({
	            type: OpenLayers.Filter.Comparison.BETWEEN,
	            property: property,
	            lowerBoundary: bins[1].lower,
	            upperBoundary: bins[1].upper
	        }),
	        symbolizer: {
	            fillColor: bins[1].color,
	            fillOpacity: .8,
	            strokeWidth: 0
	        }
	    });
	    var third = new OpenLayers.Rule({
	        filter: new OpenLayers.Filter.Comparison({
	            type: OpenLayers.Filter.Comparison.BETWEEN,
	            property: property,
	            lowerBoundary: bins[2].lower,
	            upperBoundary: bins[2].upper
	        }),
	        symbolizer: {
	            fillColor: bins[2].color,
	            fillOpacity: .8,
	            strokeWidth: 0
	        }
	    });
	    var fourth = new OpenLayers.Rule({
	        filter: new OpenLayers.Filter.Comparison({
	            type: OpenLayers.Filter.Comparison.BETWEEN,
	            property: property,
	            lowerBoundary: bins[3].lower,
	            upperBoundary: bins[3].upper
	        }),
	        symbolizer: {
	            fillColor: bins[3].color,
	            fillOpacity: .8,
	            strokeWidth: 0
	        }
	    });
	    return [first, second, third, fourth];
	};

	return {
		surveyLayerNames: surveyLayerNames,
		legendColors: legend,
		getSurveyStylingRules: getSurveyStylingRules
	}

})();
