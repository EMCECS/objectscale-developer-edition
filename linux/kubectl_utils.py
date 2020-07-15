import subprocess
import getpass 
import os
class kubectl_utility:
	is_valid_install: bool
	
	def __init__(self):
		self.is_valid_install = False

	def install_kubectl(self):
		exist = subprocess.call('command -v kubectl', shell=True)
		if exist == 0:
			print ("Kubectl is installed. Skipping Kubectl installation.")
		else:
			print ("Kubectl is not installed. Starting Kubectl installation.")

			# Update & Install Snapd before trying to install kubectl
			subprocess.run(['sudo', 'apt', 'update'])
			subprocess.run(['sudo', 'apt', 'install', 'snapd'])

			# Install kubectl
			subprocess.run(['sudo', 'snap', 'install', 'kubectl', '--classic'])
			
			# Move folders for proper permissions
			login = getpass.getuser()
			homedir = os.getenv("HOME")
			kubestring = "/home/" + login + "/.kube"
			minikubestring = "/home/" + login + "/.minikube"
			subprocess.run(['sudo', 'mv', kubestring, minikubestring, homedir])
			
			kubestring = homedir + "/.kube"
			minikubestring = homedir + "/.minikube"
			subprocess.run(['sudo', 'chown', '-R', login, kubestring, minikubestring])
			
			print("Kubectl installation complete.")
		
	def movedirs(self):
		# Move folders for proper permissions
		login = getpass.getuser()
		homedir = os.getenv("HOME")
		kubestring = "/home/" + login + "/.kube"
		minikubestring = "/home/" + login + "/.minikube"
		subprocess.run(['sudo', 'mv', kubestring, minikubestring, homedir])
			
		kubestring = homedir + "/.kube"
		minikubestring = homedir + "/.minikube"
		subprocess.run(['sudo', 'chown', '-R', login, kubestring, minikubestring])
	
	def clean_kubectl(self):
		print("Removing Kubectl.")
		subprocess.run(['sudo', 'snap', 'remove', 'kubectl'])
		subprocess.run(['sudo', 'rm', '-rf', '/usr/local/bin/kubectl'])
