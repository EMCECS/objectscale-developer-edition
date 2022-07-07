# WARNING: 
FOR INTERNAL USE ONLY (REQUIRES DELL ECS ENTERPRISE GITHUB CREDENTIALS)

Running this tool may render previous portions of your cluster inoperable! Please only use this utility on a clean installation. If you use minikube, runing `minikube delete` can ensure this is the case.

# Prerequesite
- Memory: 32G
- Disk space: 256Gi recommended
- Helm: v3.5.4 (can be installed/upgraded in install.sh if enabled)
- minikube: v1.21.0

# Description
Jira Story [OBDEF-18807](https://jira.cec.lab.emc.com/browse/OBSDEF-18807)

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
