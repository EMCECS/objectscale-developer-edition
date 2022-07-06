WARNING: FOR INTERNAL USE ONLY
REQUIRES DELL ECS ENTERPRISE GITHUB CREDENTIALS

# Description
Script used to install ObjectScale manager + ECS Cluster in one command.

Intended for the SLES OS.

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
