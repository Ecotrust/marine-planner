Marine Planner Lite

## Bring up a Virtual Machine for Development with Vagrant, Chef and Fabric
```bash
vagrant plugin install vagrant-vbguest
vagrant up
fab vagrant bootstrap
NOTE for Windows machines: http://www.voidspace.org.uk/python/modules.shtml#pycrypto 
fab vagrant runserver
```

You development server will be available on http://localhost:8000.

## Provision a fresh Server with Chef and Fabric
Create a node file with the name scripts/cookbook/node_staging.json from the template in scripts/cookbook/node_staging.json.template.  Set the postgresql password and add your ssh public key to scripts/node_staging.json.  Tested with Ubuntu 12.04 (precise pangolin).

These commands install all the prerequisites for running marine planner, including postgresql/postgis, python and all the required modules in a virtual environment as well as gunicorn and nginx to serve the static files.

```bash
fab staging:root@hostname prepare
fab staging:username@hostname deploy
```

###Sample config file
```javascript
{
    "user": "www-data",
    "servername": "staging.example.com",
    "dbname": "marine-planner",
    "staticfiles": "/usr/local/apps/marine-planner/mediaroot",
    "mediafiles": "/usr/local/apps/marine-planner/mediaroot",
    "users": [
        {
            "name": "jsmith",
            "key": "ssh-rsa AAAAB3sdkfjhsdkhjfdjkhfffdj.....fhfhfjdjdfhQ== jsmith@machine.local"
        }
    ],
    "postgresql": {
        "password": {
            "postgres": "some random password here"
        }
    },
    "run_list": [
        "marine-planner::default"
    ]
}
```

After the prepare command runs you will no longer be able to login as root with a password.  The prepare command creates one or more users with sudo access based on the list of users specified in the json file.
