Marine Planner Lite

## Bring up a Virtual Machine for Development with Vagrant, Chef and Fabric
```bash
vagrant plugin install vagrant-vbguest
vagrant up
fab vagrant bootstrap
fab vagrant runserver
```

## Provision a fresh Server with Chef and Fabric
Add your ssh public key to scripts/node_staging.json.  Edit the fabfile.py and set the staging host.  Tested with Ubuntu 12.04 (precise pangolin).

```bash
fab staging:root@hostname prepare
fab staging:eknuth@hostname deploy
```
