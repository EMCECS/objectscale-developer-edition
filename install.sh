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
sh start-minikube.sh
