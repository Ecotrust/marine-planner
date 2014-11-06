#!/bin/bash

PROJECT_NAME="marine-planner"

PROJECT_DIR=/home/vagrant/$PROJECT_NAME/mp
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME
APP_DB_NAME="marco"

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip

# see https://docs.google.com/a/pointnineseven.com/document/d/1MbPbDp-Om1iIRb6bqhaKELqyU6x6E2KZ3Wm04tYAxak/edit#
cat << EOF | su - postgres -c psql
CREATE DATABASE marco;
\connect marco
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;

insert into spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text)
values (99996, 'EPSG', 99996, 'Marco Albers', '+proj=aea +lat_1=37.25 +lat_2=40.25 +lat_0=36 +lon_0=-72 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs');

CREATE OPERATOR CLASS gist_geometry_ops
FOR TYPE geometry USING GIST AS
STORAGE box2df,
OPERATOR        1        <<  ,
OPERATOR        2        &<  ,
OPERATOR        3        &&  ,
OPERATOR        4        &>  ,
OPERATOR        5        >>  ,
OPERATOR        6        ~=  ,
OPERATOR        7        ~   ,
OPERATOR        8        @   ,
OPERATOR        9        &<| ,
OPERATOR        10       <<| ,
OPERATOR        11       |>> ,
OPERATOR        12       |&> ,

OPERATOR        13       <-> FOR ORDER BY pg_catalog.float_ops,
OPERATOR        14       <#> FOR ORDER BY pg_catalog.float_ops,
FUNCTION        8        geometry_gist_distance_2d (internal, geometry, int4),

FUNCTION        1        geometry_gist_consistent_2d (internal, geometry, int4),
FUNCTION        2        geometry_gist_union_2d (bytea, internal),
FUNCTION        3        geometry_gist_compress_2d (internal),
FUNCTION        4        geometry_gist_decompress_2d (internal),
FUNCTION        5        geometry_gist_penalty_2d (internal, internal, internal),
FUNCTION        6        geometry_gist_picksplit_2d (internal, internal),
FUNCTION        7        geometry_gist_same_2d (geom1 geometry, geom2 geometry, internal);

EOF

apt-get install python-gdal

# Virtualenv setup for project
su - vagrant -c "/usr/local/bin/virtualenv --system-site-packages $VIRTUALENV_DIR && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache $PIP install pillow && \
    PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache $PIP install -r $PROJECT_DIR/../requirements.txt"

echo "workon $PROJECT_NAME" >> /home/vagrant/.bashrc

# Run syncdb/migrate/update_index
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py syncdb"
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py migrate --noinput"
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py install_media"
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py enable_sharing"

# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/vagrant/.bashrc
export PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache
alias dj="$PYTHON $PROJECT_DIR/manage.py"
alias djrun="dj runserver 0.0.0.0:8000"
EOF
