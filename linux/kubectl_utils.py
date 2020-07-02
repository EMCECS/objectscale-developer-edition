import subprocess

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

			# Update & Install
			# subprocess.run(['sudo', 'apt-get', 'update'])
			# subprocess.run(['sudo', 'apt-get', 'install', '-y', 'apt-transport-https'])

			# Add GPG Key
			# readin = subprocess.Popen(["curl", "-s", "https://packages.cloud.google.com/apt/doc/apt-key.gpg"], stdout=subprocess.PIPE)
			# readout = subprocess.Popen(["sudo", "apt-key", "add"], stdin=readin.stdout, stdout=subprocess.PIPE)
			# readin = readout.communicate()[0]

			# Add to Kubernetes List
			# readin = subprocess.Popen(["printf", "deb https://apt.kubernetes.io/ kubernetes-xenial main"], stdout=subprocess.PIPE)
			# readout = subprocess.Popen(["sudo", "tee", "-a", "/etc/apt/sources.list.d/kubernetes.list"], stdin=readin.stdout, stdout=subprocess.PIPE)
			# readin = readout.communicate()[0]

			# Update & Install
			# subprocess.run(['sudo', 'apt-get', 'update'])
			# subprocess.run(['sudo', 'apt-get', 'install', '-y', 'kubectl'])

			# this only works on linux distributions that support snap
			subprocess.run(['sudo', 'apt', 'update'])
			subprocess.run(['sudo', 'apt', 'install', 'snapd'])
			subprocess.run(['sudo', 'install', 'kubectl', '--classic'])
			print("Kubectl installation complete.")

	def clean_kubectl(self):
		print("Removing Kubectl.")
		subprocess.run(['sudo', 'snap', 'remove', 'kubectl'])
		subprocess.run(['sudo', 'rm', '-rf', '/usr/local/bin/kubectl'])
		print("Kubectl removal complete.")