# This is the main installation script, meant to be run
# by the developer on any OS to install [minikube and ECS, or just ECS on minikube?]
import platform
import sys
from windows.install_windows import install_win
from linux.install_linux import install_tux
from macos.install_macos import install_mac
from arg_parsing.arg_cache import parse_args


def main():
    print('Hello, Developer.')
    parse_args()

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
