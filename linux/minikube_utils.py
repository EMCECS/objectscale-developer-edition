import subprocess

class minikube_utility:
	is_valid_install: bool
	
	def __init__(self):
		self.is_valid_install = False

	def install_minikube(self):
		exist = subprocess.call('command -v minikube', shell=True)
		if exist == 0:
			print ("Minikube is installed. Skipping Minikube installation.")
		else:
			print ("Minikube is not installed. Starting Minikube installation.")
		
			subprocess.run(['sudo', '-i', 'curl', '-Lo', 'minikube', "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"])
			subprocess.run(['sudo', '-i', 'chmod', '+x', 'minikube'])
			subprocess.run(['sudo', '-i', 'cp', 'minikube', "/usr/local/bin"])
			subprocess.run(['sudo', '-i', 'rm', 'minikube'])
			
			print ("Minikube installation complete.")
			return
	
	def clean_minikube():
		print("Cleaning Minikube.")
		subprocess.run(['minikube', 'stop'])
		subprocess.run(['minikube', 'delete'])
		subprocess.run(['docker', 'stop'])
		subprocess.run(['rm', '-r', '~/.kube', '~/.minikube'])
		subprocess.run(['sudo', 'rm', '/usr/local/bin/localkube'])
		subprocess.run(['sudo', 'rm', '/usr/local/bin/minikube'])
		print("Cleaning Minikube complete.")
