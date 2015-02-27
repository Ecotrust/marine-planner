from general.utils import format_precision

def get_min(grid_cells, field):
    min = getattr(grid_cells[0], field)
    for gc in grid_cells:
        if getattr(gc, field) < min:
            min = getattr(gc, field)
    return min

def get_max(grid_cells, field):
    max = getattr(grid_cells[0], field)
    for gc in grid_cells:
        if getattr(gc, field) > max:
            max = gc.depth_max
    return max

def get_range(grid_cells, field):
    min = getattr(grid_cells[0], field)
    max = getattr(grid_cells[0], field)
    for gc in grid_cells:
        if getattr(gc, field) < min:
            min = getattr(gc, field)
        if getattr(gc, field) > max:
            max = getattr(gc, field)
    return min, max

def get_value_count(grid_cells, field, value):
	count = 0
	for gc in grid_cells:
		if getattr(gc, field) == value:
			count += 1
	return count

def get_sum(grid_cells, field):
    sum = 0
    for gc in grid_cells:
        sum += getattr(gc, field)
    return sum 

def get_average(grid_cells, field):
    cell_count = grid_cells.count()
    if cell_count == 0:
        return 0
    sum = get_sum(grid_cells, field)
    return sum / cell_count

def get_unique_values(grid_cells, field):
    values = []
    for gc in grid_cells:
        value = getattr(gc, field)
        if value not in values:
            values.append(value)
    return values

def get_summary_reports(grid_cells, attributes):

    if grid_cells.count() == 0:
        return
    
    # Number of Grid Cells        
    cell_count = grid_cells.count()
    attributes.append({'title': 'Number of Grid Cells', 'data': format(cell_count, ',d')})

    # Total Area
    total_area = sum([gc.geometry.area for gc in grid_cells])
    attributes.append({'title': 'Total Area', 'data': str(format_precision(total_area / 1000000, 2)) + ' sq km'})    

    # Region
    regions = get_unique_values(grid_cells, 'region')
    if len(regions) == 1:
        attributes.append({'title': 'Region', 'data': regions[0]})
    elif len(regions) > 1:
        attributes.append({'title': 'Regions', 'data': ", ".join(regions)})

    # County
    counties = get_unique_values(grid_cells, 'county')
    if len(counties) == 1:
        attributes.append({'title': 'County', 'data': counties[0]})
    elif len(counties) > 1:
        attributes.append({'title': 'Counties', 'data': ", ".join(counties)})

    # Depth Range
    min_depth = get_min(grid_cells, 'depth_min')
    max_depth = get_max(grid_cells, 'depth_max')
    depth_range = '%s to %s feet' %(format_precision(min_depth,0), format_precision(max_depth,0))
    attributes.append({'title': 'Depth Range', 'data': depth_range})

    # Distance to Shore
    min_distance_to_shore, max_distance_to_shore = get_range(grid_cells, 'shore_distance')
    distance_to_shore = '%s to %s km' %(format_precision(min_distance_to_shore,1), format_precision(max_distance_to_shore,1))
    attributes.append({'title': 'Distance to Shore', 'data': distance_to_shore})

    # Distance to Pier
    min_distance_to_pier, max_distance_to_pier = get_range(grid_cells, 'pier_distance')
    distance_to_pier = '%s to %s km' %(format_precision(min_distance_to_pier,1), format_precision(max_distance_to_pier,1))
    attributes.append({'title': 'Distance to Nearest Pier', 'data': distance_to_pier})

    # Distance to Inlet
    min_distance_to_inlet, max_distance_to_inlet = get_range(grid_cells, 'inlet_distance')
    distance_to_inlet = '%s to %s km' %(format_precision(min_distance_to_inlet,1), format_precision(max_distance_to_inlet,1))
    attributes.append({'title': 'Distance to Nearest Coastal Inlet', 'data': distance_to_inlet})

    # Distance to Outfall
    min_distance_to_outfall, max_distance_to_outfall = get_range(grid_cells, 'inlet_distance')
    distance_to_outfall = '%s to %s km' %(format_precision(min_distance_to_outfall,1), format_precision(max_distance_to_outfall,1))
    attributes.append({'title': 'Distance to Nearest Outfall', 'data': distance_to_outfall})

    # Injury Sites
    title = 'Injury Sites'
    data = 'No Recorded Injury Sites'
    num_injury_sites = get_value_count(grid_cells, 'injury_site', 'Y')
    if num_injury_sites == 1:
        data = '1 cell contains Injury Sites'
    elif num_injury_sites > 1:
        data = str(num_injury_sites) + ' cells contain Injury Sites'
    attributes.append({'title': title, 'data': data})

    # Large Live Corals
    title = 'Large Live Corals'
    data = 'No Known Large Live Corals'
    num_large_live_corals = get_value_count(grid_cells, 'large_live_coral', 'Y')
    if num_large_live_corals == 1:
        data = '1 cell is known to contain Large Live Corals'
    elif num_large_live_corals > 1:
        data = str(num_large_live_corals) + ' cells known to contain Large Live Corals'
    attributes.append({'title': title, 'data': data})

    # Pillar Corals
    title = 'Pillar Corals'
    data = 'No Known Pillar Corals'
    num_pillar_presence = get_value_count(grid_cells, 'pillar_presence', 'P')
    if num_pillar_presence == 1:
        data = '1 cell is known to contain Pillar Corals'
    elif num_pillar_presence > 1:
        data = str(num_pillar_presence) + ' cells are known to contain Pillar Corals'
    attributes.append({'title': title, 'data': data})

    # Anchorages
    title = 'Anchorages'
    data = 'No Designated Anchorages'
    num_anchorages = get_value_count(grid_cells, 'anchorage', 'Y')
    if num_anchorages == 1:
        data ='1 cell contains a Designated Anchorage'
    elif num_anchorages > 1:
        data = str(num_anchorages) + ' cells contain Designated Anchorages'
    attributes.append({'title': title, 'data': data})

    # Mooring Buoys
    title = 'Mooring Buoys'
    data = 'No Mooring Buoys'
    num_mooring_buoys = get_value_count(grid_cells, 'mooring_buoy', 'Y')
    if num_mooring_buoys == 1:
        data = '1 cell contains Mooring Buoy'
    elif num_mooring_buoys > 1:
        data = str(num_mooring_buoys) + ' cells contain Mooring Buoys'
    attributes.append({'title': title, 'data': data})

    # Mapped Impact Source
    title = 'Impact Sources'
    data = 'No Mapped Impact Sources'
    num_impacted = get_value_count(grid_cells, 'impacted', 'Y')
    if num_impacted == 1:
        data = '1 cell contains Mapped Impact Sources'
    elif num_impacted > 1:
        data = str(num_impacted) + ' cells contain Mapped Impact Sources'
    attributes.append({'title': title, 'data': data})

    # Dense Acropora Presence
    title = 'Acropora'
    data = 'No Known Dense Acropora Patches'
    num_acropora = get_value_count(grid_cells, 'acropora_pa', 'Y')
    if num_acropora == 1:
        data = '1 cell is known to contain Dense Acropora Patches'
    elif num_acropora > 1:
        data = str(num_acropora) + ' cells are known to contain Dense Acropora Patches'
    attributes.append({'title': title, 'data': data})

    # Seagrass
    title = 'Seagrass Coverage'
    percent_seagrass = get_average(grid_cells, 'prcnt_sg')
    data = str(format_precision(percent_seagrass, 0)) + '%'
    attributes.append({'title': title, 'data': data})

    # Reef
    title = 'Reef Coverage'
    percent_reef = get_average(grid_cells, 'prcnt_reef')
    data = str(format_precision(percent_reef, 0)) + '%'
    attributes.append({'title': title, 'data': data})

    # Sand
    title = 'Sand Coverage'
    percent_sand = get_average(grid_cells, 'prcnt_sand')
    data = str(format_precision(percent_sand, 0)) + '%'
    attributes.append({'title': title, 'data': data})

    # Artificial Substrate
    title = 'Artificial Substrate Coverage'
    percent_art = get_average(grid_cells, 'prcnt_art')
    data = str(format_precision(percent_art, 0)) + '%'
    attributes.append({'title': title, 'data': data})

    # Dense Acropora cervicornis patches (Area)
    title = 'Dense Acropora'
    acerv_area = get_sum(grid_cells, 'acerv_area')
    data = str(format_precision(acerv_area / 1000000.0, 2)) + ' sq km'
    attributes.append({'title': title, 'data': data})

    # Reef Area
    title = 'Reefs'
    reef_area = get_sum(grid_cells, 'reef_area')
    # if reef_area > 100000:
    #     data = str(format_precision(reef_area / 1000000.0, 1)) + ' sq km'
    # elif reef_area > 0:        
    #     data = str(format(format_precision(reef_area, 0), ',d')) + ' sq meters'
    data = str(format_precision(reef_area / 1000000.0, 2)) + ' sq km'
    attributes.append({'title': title, 'data': data})

    # Seagrass Area
    title = 'Seagrass'
    sg_area = get_sum(grid_cells, 'sg_area')
    data = str(format_precision(sg_area / 1000000.0, 2)) + ' sq km'
    attributes.append({'title': title, 'data': data})

    # Sand Area
    title = 'Sand'
    sand_area = get_sum(grid_cells, 'sand_area')
    data = str(format_precision(sand_area / 1000000.0, 2)) + ' sq km'
    attributes.append({'title': title, 'data': data})

    # Artifical Reef Area
    title = 'Artifical Reefs'
    art_area = get_sum(grid_cells, 'art_area')
    data = str(format_precision(art_area / 1000000.0, 2)) + ' sq km'
    attributes.append({'title': title, 'data': data})

    # Fish Density
    title = 'Estimated # of Fish Organisms per sq meter'
    data = 'None'
    fish_density = get_average(grid_cells, 'fish_density')
    if fish_density > 0:
        data = str(format_precision(fish_density, 0))
    attributes.append({'title': title, 'data': data})

    # Fish Richness
    title = 'Estimated # of Fish Species per survey area'
    data = 'None'
    fish_richness = get_average(grid_cells, 'fish_richness')
    if fish_richness > 0:
        data = str(format_precision(fish_richness, 0))
    attributes.append({'title': title, 'data': data})

    # Coral Cover
    title = 'Average Coral Cover'
    coral_cover = get_average(grid_cells, 'coral_cover')
    data = str(format_precision(coral_cover, 0)) + ' units'
    attributes.append({'title': title, 'data': data})

    # Coral Density
    title = 'Estimated # of Coral Organisms per sq meter'
    coral_density = get_average(grid_cells, 'coral_density')
    data = str(format_precision(coral_density, 0))
    attributes.append({'title': title, 'data': data})

    # Coral Richness
    title = 'Estimated # of Coral Species per survey area'
    coral_richness = get_average(grid_cells, 'coral_richness')
    data = str(format_precision(coral_richness, 0))
    attributes.append({'title': title, 'data': data})

    # Coral Size
    title = 'Average Coral Size'
    coral_size = get_average(grid_cells, 'coral_size')
    data = str(format_precision(coral_size, 0)) + ' units'
    attributes.append({'title': title, 'data': data})


