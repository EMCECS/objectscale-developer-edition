# optional upgrade helm

#wget http://asdrepo.isus.emc.com:8081/artifactory/ecs-build/com/github/helm/helm/3.5.4/helm-v3.5.4-linux-amd64.tar.gz
#tar xf helm-*
#chmod +x linux-amd64/helm
#cp linux-amd64/helm /usr/local/bin/

#Check if dev-tools already exists
DEV_REPO=./dev-tools/
if [ ! -d "$DEV_REPO" ]; then
	#Clone deployment repo
	git clone https://eos2git.cec.lab.emc.com/ECS/dev-tools
	cd dev-tools/objectscale/deployment

	#Clone charts repo
	git clone https://eos2git.cec.lab.emc.com/ECS/objectscale-charts.git
	cd objectscale-charts
	make chart-dep
	cd ../
fi

cd ./dev-tools/objectscale/deployment


#Start minikube
./start-minikube.sh

#Wait for minikube
kubectl -n metallb-system rollout status deployment/controller
kubectl -n kube-system rollout status deployment/coredns

cd ./dev-tools/objectscale/deployment
#Install Decks/Kahm
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/application/master/config/crd/bases/app.k8s.io_applications.yaml
./install-decks-kahm.sh
kubectl rollout status deployment/decks

#Install Objectscale Manager
./install-objectscale-manager.sh

kubectl rollout status deployment/atlas-operator
kubectl rollout status deployment/objectscale-dcm
kubectl rollout status deployment/objectscale-federation
kubectl rollout status deployment/objectscale-gateway
kubectl rollout status deployment/objectscale-iam
kubectl rollout status deployment/objectscale-manager-bookkeeper-operator
kubectl rollout status deployment/objectscale-manager-pravega-operator
kubectl rollout status deployment/objectscale-service-pod
kubectl rollout status deployment/objectscale-operator
kubectl rollout status deployment/zookeeper-operator

#Install ECS Cluster
./install-ecs-cluster.sh

