#!/bin/sh
set -xu

# delete ECS cluster
OBJECTSTORE_RELEASE=$(kubectl get --no-headers ecs | awk '{print $1}')
helm delete ${OBJECTSTORE_RELEASE}

sleep 5

# remove objectscale manager
helm delete $(helm list -q)

# delete PVCs
kubectl delete pvc  --all

# clean up storage in case any left
rm -rf /tmp/hostpath-provisioner/*

# clean logs
rm *\.log\.*
