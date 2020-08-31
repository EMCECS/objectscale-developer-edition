import subprocess

class misc_utility:
	is_valid_install: bool
	
	def __init__(self):
		self.is_valid_install = False

	def install_misc(self):
		print ("Starting Misc utilities installations")

		subprocess.run(['sudo', 'apt', 'update'])
		subprocess.run(['sudo', 'apt', 'install', 'conntrack'])
		subprocess.run(['sudo', 'apt', 'install', 'ethtool'])
		subprocess.run(['sudo', 'apt', 'install', 'ebtables'])
		subprocess.run(['sudo', 'systemctl', 'enable', 'kubelet.service'])

		print ("Misc utilities installation complete.")
		return
