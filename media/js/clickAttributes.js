
app.clickAttributes = (function() {

	var getSurveyAttributes = function(data) {
		attrs = [];
		for (var key in data) {
		  	if (data.hasOwnProperty(key) && data[key]) {
		  		if (key !== 'Total Activity Days' && key !== 'Other') {
		  			if (data[key] === 1) {
		    			attrs.push({'display': key, 'data': data[key] + ' day'});
		  			} else {
		    			attrs.push({'display': key, 'data': data[key] + ' days'});
		  			}
		  		}
		  	}
		}
		// alphabetize and then put Total at top (or bottom)
		attrs = _.sortBy(attrs, function(obj){ return obj['display']; });
		if (data['Other']) {
			if (data['Other'] === 1) {
				attrs.push({'display': 'Other', 'data': data['Other'] + ' day'});
			} else {
				attrs.push({'display': 'Other', 'data': data['Other'] + ' days'});
			}
		}
		attrs.unshift({'display': 'Total Number of Activity Days', 'data': data['Total Activity Days']});
		return attrs;
	}
	
	// Placeholder in case we want to cusomize the Planning Grid feature attributes
    var getGridAttributes = function (data) {
        attrs = [];
                
        //Wind Speed
        if ('wind_min' in data && 'wind_max' in data) {
            attrs.push({'display': 'Estimated Wind Potential', 'data': data['wind_min'].toFixed(1) + ' to ' + data['wind_max'].toFixed(1) + ' W/m&sup2;'});
        }
        //Depth Range
        if ('bathy_min' in data && 'bathy_max' in data) {
            attrs.push({'display': 'Depth Range', 'data': data['bathy_min'].toFixed(1) + ' to ' + data['bathy_max'].toFixed(1) + ' meters'});
        }
        //Distance to Coastal Substations
        if ('subs_avgd' in data) {
            // attrs.push({'display': 'Minimum Distance to Coastal Substation', 'data': (data['SubS_MinD']/1000).toFixed(1) + ' km'});
            attrs.push({'display': 'Average Distance to Coastal Substation', 'data': (data['subs_avgd']).toFixed(1) + ' km'});
        }
        //Distance to Shore
        if ('coast_avg' in data) {
            // attrs.push({'display': 'Minimum Distance to Shore', 'data': (data['Coast_Min']/1000).toFixed(1) + ' km'});
            attrs.push({'display': 'Average Distance to Shore', 'data': (data['coast_avg']).toFixed(1) + ' km'});
        }
        //Coral Percentage
        if ('coral_p' in data) {
            attrs.push({'display': 'Coral coverage', 'data': data['coral_p'].toFixed(1) + '%'});
        }
        //Mangrove Percentage
        if ('mangrove_p' in data) {
            attrs.push({'display': 'Mangrove coverage', 'data': data['mangrove_p'].toFixed(1) + '%'});
        }
        //Submerged Vegetation Percentage
        if ('subveg_p' in data) {
            attrs.push({'display': 'Submerged Vegetation coverage', 'data': data['subveg_p'].toFixed(1) + '%'});
        }
        //Protected Area Percentage
        if ('protarea_p' in data) {
            attrs.push({'display': 'Protected Area coverage', 'data': data['protarea_p'].toFixed(1) + '%'});
        }
        //Presence/Absence of Conservation Priority Area 
        if ('pr_apc_p' in data && 'vi_apc_p' in data) {
            var total_percentage = data['pr_apc_p'] + data['vi_apc_p'];
            attrs.push({'display': 'Conservation Priority Area coverage', 'data': total_percentage.toFixed(1) + '%'});
        } 
        // Presence/Absence of Special Planning Area
        if ('pr_ape_p' in data) {
            attrs.push({'display': 'Special Planning Area coverage', 'data': data['pr_ape_p'].toFixed(1) + '%'});
        } 
        
        return attrs;
    };

    return {
    	getGridAttributes: getGridAttributes,
    	getSurveyAttributes: getSurveyAttributes
    };

})();