#!/bin/bash
 
# Constants
red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'
 
# Default values of arguments
METAL_LB_REQUESTED=false
SIZE_OF_DEPLOYMENT="M"
REPO_PRIVATE_TOKEN=""
 
# Disable echo
set -e
 
# Clear screen
clear
 
# Test Color Print
#printf "%s\n" "Test Color Print: in ${red}red${end}, ${grn}green, ${yel}yellow, ${mag}magenta, ${cyn}cyan${end}, white, and ${blu}blue${end}."
 
# Loop through arguments and process them
while getopts ":hpt:" opt; do
  case ${opt} in
    h ) # process option h
      printf  "%s\n" "${grn}Usage:${end}"
      printf  "%s\n" "    ${grn} -h   Display this help message.${end}"
      #printf  "%s\n" "    ${grn} -l   Deploy Metal LB (Not implemented)${end}"
      #printf  "%s\n" "    ${grn} -d   Set the deployment size.  M (Micro) or S (Small) (Not Implemented)${end}"
      printf  "%s\n" "    ${grn} -p   Install Docker${end}"
      printf  "%s\n" "    ${grn} -t   ECS Flex GitHub Private Token${end}"
      exit  0
      ;;
    l ) # process option l
      printf  "%s\n" "${grn}-l option provided${end}"
      ;;
    d ) # process option d
      printf  "%s\n" "${grn}-d option provided${end}"
      ;;
    p ) # process option p
      #printf  "%s\n" "${grn}-p option provided${end}"
      DOCKER_INSTALL="1"
      ;;
    t ) # process option t
      printf  "%s\n" "${grn}-t option provided${end}"
      REPO_PRIVATE_TOKEN=$OPTARG
      ;;
    \? )
      printf  "%s\n" "${grn}Usage:${end}"
      printf  "%s\n" "    ${grn} -h   Display this help message.${end}"
      #printf  "%s\n" "    ${grn} -l   Deploy Metal LB (Not implemented)${end}"
      #printf  "%s\n" "    ${grn} -d   Set the deployment size.  M (Micro) or S (Small) (Not Implemented)${end}"
      printf  "%s\n" "    ${grn} -p   Install Docker${end}"
      printf  "%s\n" "    ${grn} -t   ECS Flex GitHub Private Token${end}"
      exit  0
      ;;
    : )
      printf  "%s\n" "${grn}Invalid option: Parameter %s requires an argument${end}" "$OPTARG" 1>&2
      exit 0
      ;;
  esac
done
 
# Check for mandatory arguments i.e. ECS Flex Github Repo private token
if [ ! "$REPO_PRIVATE_TOKEN" ]; then
  printf  "%s\n\n" "${red}The -t argument is mandatory and must be set to your personal access token for the ECS Flex GitHub Repository.${end}"
  exit 1
fi
 
printf  "%s\n" "${blu} -----------------------------------------------------------------------${end}"
printf  "%s\n" "${blu} About to install ECS Flex with MiniKube on Ubuntu.  This script will: ${end}"
printf  "%s\n" "${blu}     1. Check to ensure Docker is installed.  If not it will install it.${end}"
printf  "%s\n" "${blu}     2. Install MiniKube if needed                                     ${end}"
printf  "%s\n" "${blu}     3. Install Kubectl if needed                                      ${end}"
printf  "%s\n" "${blu}     4. Grab current resolv.conf and copy it to /root/minikube_resolv.conf${end}"
printf  "%s\n" "${blu}     5. Spin up a MiniKube K8s cluster using --vm-driver=none    ${end}"
 
read -p "${grn}Press enter to continue with the setup of ECS Flex with Minikube on Ubuntu or ctrl-c to cancel....${end}"
 
# Lets check if Docker is installed
if [ -x "$(command -v docker)" ]; then
    printf  "%s\n" "${grn}Docker installed.  Continuing.${end}"
    # command
else
    # Install Docker from pacakges if configured - otherwise try the repo.  Docker Repos for Ubuntu are flaky
    if [ $DOCKER_INSTALL = "1" ]; then
      printf  "%s\n" "${red}Docker not installed on Ubuntu and install requested.  Installing Docker....${end}"
 
      # Install Docker required packages
      sudo apt-get clean
      sudo apt-get update
      sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
 
      # Add Docker's GPG Key
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
 
 
      # Remove docker files
      sudo apt-get remove docker docker-engine docker.io containerd runc
 
      # Set Docker Stable Repository
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
 
      # Install Docker CE
      sudo apt-get update
      sudo apt-get install -y docker-ce docker-ce-cli containerd.io
 
      # Add current user to Docker Group
      sudo usermod -aG docker "$USER"
 
      # Enable Docker Service
      sudo systemctl enable docker
 
      # Start Docker Service
      sudo systemctl start docker
 
      printf  "%s\n" "${red}Docker CE has been installed.  Please logout and back into the server.  Then re-launch this script${end}"
    else
      printf  "%s\n" "${red}Docker not installed on Ubuntu and install NOT requested.  Please install Docker before continuing.${end}"
    fi
 
    exit 0
 
fi
 
# Create a working directory and change to it
cd ~ || exit
mkdir -p ecs_flex_ubuntu
cd ~/ecs_flex_ubuntu || exit
 
# Install Minikube if NOT  installed
if [ -x "$(command -v minikube)" ]; then
    printf  "%s\n" "${grn}Minikube installed.  Continuing.${end}"
else
    printf  "%s\n\n" "${yel}Minikube is not installed.  Installing....${end}"
    sudo -i curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo -i chmod +x minikube
    sudo -i cp minikube /usr/local/bin
    sudo -i rm minikube
    printf  "%s\n\n" "${grn}Minikube version $(minikube version | head -n1 | cut -d: -f2) installed.${end}"
fi
 
# Install kubectl if NOT  installed
if [ -x "$(command -v kubectl)" ]; then
    printf  "%s\n" "${grn}kubectl installed.  Continuing.${end}"
    # command
else
    printf  "%s\n\n " "${yel}kubectl is not installed.  Installing....${end}"
    sudo apt-get update && sudo apt-get install -y apt-transport-https
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    printf  "%s\n" "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
    sudo apt-get update
    sudo apt-get install -y kubectl
    printf  "%s\n\n" "${grn}kubectl installed.${end}"
fi
 
# Install resolve.conf file
printf  "%s\n\n" "${grn}Copying running resolv.conf file to /root/minikube_resolv.conf.${end}"
sudo -i cp /run/systemd/resolve/resolv.conf /root/minikube_resolv.conf
 
# Create Kuberneters cluster on Minikube
sudo apt-get install -y conntrack
 
printf "%s\n\n" "${yel}Starting minikube cluster creation....${end}"
 
sudo -i minikube start --vm-driver=none --extra-config=kubelet.resolv-conf=/root/minikube_resolv.conf --extra-config=kubelet.eviction-hard="memory.available<500Mi,nodefs.available<1Gi,imagefs.available<2Gi" --extra-config=kubelet.eviction-minimum-reclaim="memory.available=0Mi,nodefs.available=500Mi,imagefs.available=1Gi"
printf "%s\n\n" "${grn}minikube cluster creation completed.  Run 'kubectl get pods -n kube-system' to view the K8s cluster pods.${end}"
 
printf "%s\n\n" "${grn}Copying kubernetes admin.conf to local .kube/config.${end}"
mkdir -p "$HOME"/.kube
sudo cp /etc/kubernetes/admin.conf "$HOME"/.kube/config
sudo chown "$USER":"$USER" "$HOME"/.kube/config
 
# Install HELM
printf "%s\n" "${yel}Installing Helm..... ${end}"
sudo apt install -y socat
sudo snap install helm --classic
 
printf "%s\n\n" "${grn}Helm installation completed.  Setting up Helm repos for ECS Flex${end}"
 
# Setup ECS Flex HELM Repo
helm repo add deos https://"$REPO_PRIVATE_TOKEN"@raw.githubusercontent.com/emcecs/charts/master/docs
helm repo update
helm repo list
helm search repo deos
 
# Insall ECS Flex Components
printf "%s\n" "${yel}Installing Objectscale Manager for ECS Flex using Helm....${end}"
helm install objs-mgr deos/objectscale-manager --set global.registry=harbor.lss.emc.com/ecs
 
printf "%s\n" "${yel}Installing ECS Flex cluster using Helm....${end}"
helm install deos/ecs-cluster --set global.registry=harbor.lss.emc.com/ecs --generate-name --set storageServer.persistence.size=100Gi --set performanceProfile=Micro --set provision.enabled=True --set storageServer.persistence.protected=True --set enableAdvancedStatistics=False --set managementGateway.service.type=NodePort --set s3.service.type=NodePort
 
printf "%s\n\n" "${grn}ECS Flex components installation completed.  Run 'kubectl get pods' to view running pods.${end}"