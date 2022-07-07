WARNING: FOR INTERNAL USE ONLY
REQUIRES DELL ECS ENTERPRISE GITHUB CREDENTIALS

# Description
Script used to install ObjectScale manager + ECS Cluster in one command.

Based of off https://eos2git.cec.lab.emc.com/ECS/dev-tools/tree/master/objectscale/deployment

# Usage:
Make sure that minikube is not running.
```
minikube stop
minikube delete
```

Run install.sh:
```
sh install.sh
```

# Uninstall:
Run uninstall.sh, this will remove the objectscale manager and ecs cluster.
```
sh uninstall.sh
```
You may also want to scrap your minikube instance as well.
```
minikube stop
minikube delete
```
