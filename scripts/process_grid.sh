#!/bin/bash
# process_grid.sh
# Input: shapefile (epsg 3857) with planning grids
# Output: postgres sql file 

thisdir=`dirname $BASH_SOURCE`

# Variables that change frequently/on every import
#SHP="_ofr_data/shp/OFR_OffshorePlanningGrid_200m_DSTbuild4_EPSG3857_9Feb2015.shp"
#FINAL="_ofr_data/ofr_planning_grid_9Feb2015.sql"
SHP="_ofr_data/shp/OFR_OffshorePlanningGrid_200m_DSTbuild8_EPSG3857_13Mar2015.shp"
FINAL="_ofr_data/ofr_planning_grid_13Mar2015.sql"

################################################################################
# Probably no need to touch anything below here
################################################################################

# Path will not change by json file may need to be updated
FIELDMAP="$thisdir/field_map.json"

# Probably won't need to touch these if running from root project dir
TMP="/tmp/ofr_planning_grid.sql"
TRANSLATE="python $thisdir/translate.py"
VALIDATE="python $thisdir/validate_fields.py"

# Do some sanity checks on the fieldnames
$VALIDATE $SHP $FIELDMAP
if [ $? -ne 0 ]; then
    echo "NOT VALID"
    exit 1
fi 

# export shp to dump format sql
# -d option handles dropping table before creation
# -g option specifies geometry column name
shp2pgsql -d -D -s 3857 -i -I -W LATIN1 \
    -g geometry $SHP public.scenarios_gridcell > $TMP

# Replace gid with id
sed -i 's/gid serial/id serial/' $TMP
sed -E -i 's/PRIMARY KEY \(gid\)/PRIMARY KEY \(id\)/' $TMP

# Change field names to match django model
$TRANSLATE $TMP $FIELDMAP > $FINAL
 
# Add a centroid geometry column in new transaction 
cat << EOT >> $FINAL

BEGIN;
SELECT AddGeometryColumn('public','scenarios_gridcell','centroid','3857','POINT',2);
UPDATE "public"."scenarios_gridcell" SET "centroid" = ST_Centroid("geometry");
CREATE INDEX ON "public"."scenarios_gridcell" USING GIST ("centroid");
COMMIT;
EOT

echo "------"
echo "SUCCESS. sql file created; load into database on VM/Prod server with"
echo "psql -U postgres -d marco -f $FINAL"
echo "------"
