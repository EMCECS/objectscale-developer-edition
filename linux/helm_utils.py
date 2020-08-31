import subprocess

class helm_utility:
	is_valid_install: bool

	def __init__(self):
		self.is_valid_install = False

	def install_helm(self):
		exist = subprocess.call('command helm version', shell=True)
		if exist == 0:
			return

		# Install Helm required packages
		subprocess.run(['sudo', 'apt-get', 'clean'])
		subprocess.run(['sudo', 'apt-get', 'update'])
		subprocess.run(['sudo', 'apt', 'install', 'snapd'])
		subprocess.run(['sudo', 'apt', 'install', '-y', 'socat'])
		subprocess.run(['sudo', 'snap', 'install', 'helm', '--classic'])

		print("Helm installation complete.")

		# Ignore commented section, being completed inside of objectscale_utils
		# print("Setting up Helm repos.")
		# TODO
		# Setup ECS Flex HELM Repo
		# FIX REPO_PRIVATE_TOKEN (PULL FROM ARGS)
		# subprocess.run(['helm', 'repo', 'add', 'deos', 'https://^@raw.githubusercontent.com/emcecs/charts/master/docs'])
		# subprocess.run(['helm', 'repo', 'update'])
		# subprocess.run(['helm', 'repo', 'list'])
		# subprocess.run(['helm', 'search', 'repo', 'deos'])
		# print("Helm repos setup complete.")

	def clean_helm(self):
		print("Removing Helm.")
		subprocess.run(['sudo', 'snap', 'remove', 'helm'])
		subprocess.run(['sudo', 'rm', '-rf', '/usr/local/bin/helm'])

		print("Helm removal complete.")

