import subprocess
import getpass

class docker_utility:
	is_valid_install: bool

	def __init__(self):
		self.is_valid_install = False

	def install_docker(self):
		exist = subprocess.call('command -v docker', shell=True)
		if exist == 0:
			print ("Docker is installed. Skipping Docker installation.")
		else:
			print ("Docker is not installed. Starting Docker installation.")

			# Install Docker required packages
			subprocess.run(['sudo', 'apt-get', 'clean'])
			subprocess.run(['sudo', 'apt-get', 'update'])
			subprocess.run(['sudo', 'apt-get', 'install', '-y', 'apt-transport-https', 'ca-certificates', 'curl', 'gnupg-agent', 'software-properties-common'])

			# Add Docker's GPG Key
			curl = subprocess.Popen(["curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg"], stdout=subprocess.PIPE)
			aptkey = subprocess.Popen(["sudo", "apt-key", "add"], stdin=curl.stdout, stdout=subprocess.PIPE)
			curl = aptkey.communicate()[0]

			# Remove docker files
			subprocess.run(['sudo', 'apt-get', 'remove', 'docker', 'docker-engine', 'docker.io', 'containerd', 'runc'])

			# Set Docker Stable Repository
			subprocess.run(['sudo', 'add-apt-repository', "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"])

			# Install Docker CE
			subprocess.run(['sudo', 'apt-get', 'update'])
			subprocess.run(['sudo', 'apt-get', 'install', '-y', 'docker-ce'])

			# Add current user to Docker Group
			# change $user to the actual user
			user = getpass.getuser()
			subprocess.run(['sudo', 'usermod', '-aG', 'docker', user])

			# Enable Docker Service
			subprocess.run(['sudo', 'systemctl', 'enable', 'docker'])

			# Start Docker Service
			subprocess.run(['sudo', 'systemctl', 'start', 'docker'])

			print ("Docker installation complete.")