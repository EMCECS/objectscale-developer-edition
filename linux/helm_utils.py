import subprocess

class helm_utility:
	is_valid_install: bool

	def __init__(self):
		self.is_valid_install = False

	def install_helm(self):
		# Install Helm required packages
		subprocess.run(['sudo', 'apt-get', 'clean'])
		subprocess.run(['sudo', 'apt-get', 'update'])
		subprocess.run(['sudo', 'apt', 'install', 'snapd'])
		subprocess.run(['sudo', 'apt', 'install', '-y', 'socat'])
		subprocess.run(['sudo', 'snap', 'install', 'helm', '--classic'])

		print("Helm installation complete.")

		# TODO
		# Setup ECS Flex HELM Repo
		# FIX REPO_PRIVATE_TOKEN (PULL FROM ARGS)
		# subprocess.run(['helm', 'repo', 'add', 'deos', 'https://"$REPO_PRIVATE_TOKEN"@raw.githubusercontent.com/emcecs/charts/master/docs'])
		# subprocess.run(['helm', 'repo', 'update'])
		# subprocess.run(['helm', 'repo', 'list'])
		# subprocess.run(['helm', 'search', 'repo', 'deos'])
	
	def clean_helm(self):
		print("Removing Helm.")
		subprocess.run(['sudo', 'snap', 'remove', 'helm'])
		subprocess.run(['sudo', 'rm', '-rf', '/usr/local/bin/helm'])
		print("Helm removal complete.")
