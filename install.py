# This is the main installation script, meant to be run
# by the developer on any OS to install [minikube and ECS, or just ECS on minikube?]
import platform
from install_windows import install_win
from install_linux import install_tux
from install_macos import install_mac



def main():
    print('Hello, Developer.')
    os = platform.system().casefold()
    if os.find('linux') > -1:
        install_tux()
    elif os.find('windows') > -1:
        install_win()
    elif os.find('darwin') > -1:
        install_mac()
    else:
        print("Unsupported OS: "+os)


if __name__ == "__main__":
    main()
else:
    print('Not run in main context.')
