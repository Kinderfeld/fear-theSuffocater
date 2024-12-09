#!/usr/bin/python3

"""
---------------------------------------
Setups tor functionality on your machine.

- Installs tor on your machine
- Setups tor nodes.
- Setups Snowflake Proxy on FreeBSD and Debian based GNU/Linux distros
- Setups obfs4 bridges on GNU/Linux and BSD
- Adds Tor repositories for Devuan and Debian GNU/Linux.

Author: iva
Date: 02.12.2024
---------------------------------------
"""

try:
    import usr
    import subprocess
    from os import system
    from time import sleep
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")


def install_tor() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    print("We are going to install Tor on your machine.")
    answer: str = input("\n[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        try:
            usr.package_handling(distro, package_list=["tor", "torsocks"], command="install")
            
            print("Now you need to install Tor Browser from the web.")
            answer: str = input("[?] Proceed? (y/N): ")
            if answer in ["y", "yes"]:
                subprocess.run(["xdg-open", "https://www.torproject.org/download/"], check=True)
            
            print("Looks like you're locked and loaded.")
            print("Tor can't help you if you use it wrong! Learn how to be safe at https://support.torproject.org/faq/staying-anonymous/")
            answer: str = input("[?] Proceed? (y/N): ")
            if answer in ["y", "yes"]:
                subprocess.run(["xdg-open", "https://support.torproject.org/faq/staying-anonymous/"], check=True)
            
            print(f"{GREEN}[*] Success! {RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def snowflake_setup_debian() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    if distro not in usr.DEBIAN_BASED_DISTROS:
        print(f"{RED}[!] Error: your OS {distro} in not Debian based.{RESET}")
    
    print(f"{RED}[!] Warning:")
    print("     On Debian Stable based distributions packages might be outdated and so this setup might not work.")
    print(f"     It is recommended to use another setup method, e.g. Docker.{RESET}")

    answer: str = input("[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        print("Snowflake is a pluggable transport available in Tor Browser to defeat internet censorship.") 
        print("Like a Tor bridge, a user can access the open internet when even regular Tor connections are censored.")
        print("To use Snowflake is as easy as to switch to a new bridge configuration in Tor Browser.")
        print("And we are going to setup a docker snowflake proxy for you.")

        answer: str = input("[?] Proceed? (y/N): ").lower()
        if answer in ["y", "yes"]:
            try:
                usr.package_handling(distro, package_list=["snowflake-proxy"], command="install")

                answer: str = input("[?] Start Snowflake service now? (y/N): ")
                if answer in ["y", "yes"]:
                    usr.init_system_handling(init_system, "start", "snowflake-proxy")
                
                print("Looks like you are locked and loaded.\nNow, check snowflake-proxy logs and type")
                print("'systemctl stop snowlake-proxy' or 'service snowflake-proxy stop' if you want to disable it.")
                print(f"{GREEN}[*] Success!{RESET}")
            except (subprocess.CalledProcessError, FileNotFoundError) as error:
                print(f"{RED}[!] Error: {error}{RESET}")


def snowflake_setup_freebsd() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    if distro not in usr.FREEBSD_BASED_DISTROS:
        print(f"{RED}[!] Error: your OS {distro} is not FreeBSD based.{RESET}")
    
    print("Snowflake is a pluggable transport available in Tor Browser to defeat internet censorship.")
    print("Like a Tor bridge, a user can access the open internet when even regular Tor connections are censored.")
    print("To use Snowflake is as easy as to switch to a new bridge configuration in Tor Browser.")
    
    answer: str = input("[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        try:
            usr.package_handling(distro, package_list=["showflake-tor"], command="install")
            
            answer: str = input("[?] Enable Snowflake Proxy daemon on boot and start Snowflake Proxy service now? (y/N): ")
            if answer in ["y", "yes"]:
                subprocess.run(["sysrc", "snowlake_enable=YES"], check=True)
                usr.init_system_handling(init_system, "start", "snowflake")
            
            print("Looks like you are locked and loaded.\nNow, check snowflake-proxy logs and type")
            print("'service snowflake stop' if you want to disable it.")
        except (subprocess.CalledProcessError, FileNotFoundError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def snowflake_setup_docker() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    answer: str = input("[?] Proceed (y/N): ").lower()
    if answer in ["y", "yes"]:
        try:
            usr.package_handling(distro, package_list=[], command="update")

            print("[<==] Installing get-docker.sh...")
            sleep(1)
            subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o get-docker.sh"], check=True)

            print("[<==] Installing docker compose file...")
            sleep(1)
            subprocess.run(["wget", "https://gitlab.torproject.org/tpo/anti-censorship/docker-snowflake-proxy/raw/main/docker-compose.yml"], check=True)

            print("[?] Deploy Snowflake now? (y/N): ")
            if answer in ["y", "yes"]:
                print("[<==] Deploying proxy...")
                sleep(1)
                subprocess.run(["docker", "compose", "up", "-d", "snowflake-proxy"], check=True)
            
            print("Looks like you are locked and loaded. Now, dont forget to check your docker logs:")
            print("- 'docker logs -f snowflake-proxy'")
            print("And update the container with Watchtower:")
            print("- 'docker compose up -d'")
            print(f"{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def torify_apt_devuan() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    if distro != "devuan":
        print(f"{RED}[!] Error: your OS {distro} is not Devuan based.{RESET}")

    print("Tor is a free overlay network for enabling anonymous communication.")
    print("Built on free and open-source software and more than seven thousand volunteer-operated relays worldwide,") 
    print("users can have their Internet traffic routed via a random path through the network.")
    print("And if you wish, you can use apt over tor (Devuan based GNU/Linux distribution required).")

    answer: str = input("\n[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        try:
            usr.package_handling(distro, package_list=["tor", "apt-transport-tor", "apt-transport-https"], command="install")
            
            answer: str = input("[?] Start tor service now? (y/N): ").lower()
            if answer in ["y", "yes"]:
                usr.init_system_handling(init_system, "start", "tor")
            
            with open("config_files/apt_tor_devuan_repos.txt", "r") as config_file:
                apt_tor_repos: str = config_file.read()

            with open("/etc/apt/sources.list", "a") as true_config_file:
                true_config_file.write(apt_tor_repos)
            
            answer: str = input("[?] View 'sources.list' (y/N): ")
            if answer in ["y", "yes"]:
                subprocess.run(["nano", "/etc/apt/sources.list"], check=True)
            
            print(f"{GREEN}[*] Success!{RESET}")
        except (subprocess.CalledProcessError, FileNotFoundError, IOError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def torify_apt_debian() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    if distro != "debian":
        print(f"{RED}[!] Error: your OS {distro} is not devuan based.{RESET}")

    print("Tor is a free overlay network for enabling anonymous communication.")
    print("Built on free and open-source software and more than seven thousand volunteer-operated relays worldwide,")
    print("users can have their Internet traffic routed via a random path through the network.")
    print("And if you wish, you can use apt over tor (Devuan based GNU/Linux distribution required).")

    answer: str = input("\n[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        try:
            usr.package_handling(distro, package_list=["tor", "apt-transport-tor", "apt-transport-https"], command="install")
            print("[?] Start tor service now? (y/N): ")
            if answer in ["y", "yes"]:
                usr.init_system_handling(init_system, "start", "tor")
                ...

            print(f"{GREEN}[*] Success!{RESET}")
        except (subprocess.CalledProcessError, FileNotFoundError, IOError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_debian() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")

    answer: str = input("[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            ...
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_arch() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")

    answer: str = input("[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            ...
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_void() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")

    answer: str = input("[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            ...
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_dragonflybsd() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")

    answer: str = input("[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            ...
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_freebsd() -> None:
    system("clear")
    
    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")
    
    answer: str = input("[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            ...
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_openbsd() -> None:
    system("clear")
    
    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")
    
    answer: str = input("[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            ...
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_netbsd() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")

    answer: str = input("[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            ...
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_docker() -> None:
    system("clear")
    
    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")
    
    answer: str = input("[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            usr.package_handling(distro, package_list=[], command="update")

            print("[<==] Installing get-docker.sh...")
            sleep(1)
            subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o get-docker.sh"], check=True)

            print("[<==] Installing docker compose file...")
            sleep(1)
            subprocess.run(["wget", "https://gitlab.torproject.org/tpo/anti-censorship/docker-obfs4-bridge/-/raw/main/docker-compose.yml"], check=True)

            subrpocess.run(["touch", ".env"], check=True)
            tor_port: str = input("[==>] Your bridge's Tor port: ")
            obfs4_port: str = input("[==>] Your bridge's obfs4 port: ")
            email: str = input("[==>] Your Email: ")

            dotenv_template: str = f"""
# Your bridge's Tor port.
OR_PORT={tor_port}
# Your bridge's obfs4 port.
PT_PORT={obfs4_port}
# Your email address.
EMAIL={email}"""
            
            with open(".env", "w") as config_file:
                config_file.write(dotenv_template)

            answer: str = input("[?] Deploy container now? (y/N): ").lower()
            if answer in ["y", "yes"]:
                print("[<==] Deploying bridge...")
                sleep(1)
                subprocess.run(["docker-compose", "up", "-d", "obfs4-bridge"], check=True)

                print("Looks like you are locked and loaded. Now, dont forget to check your docker logs:")
                print("- 'docker logs CONTAINER_ID'")
                print("And update the container:")
                print("- 'docker-compose pull obfs4-bridge'")
                print(f"{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def tor_node_setup() -> None:
    system("clear")
    ...


def tor_management() -> None:
    system("clear")

    functions: dict = {
            "install_tor": install_tor,
            "torify_apt_debian": torify_apt_debian,
            "torify_apt_devuan": torify_apt_devuan,
            "obfs4_bridge_debian": obfs4_bridge_debian,
            "obfs4_bridge_arch": obfs4_bridge_arch,
            "obfs4_bridge_void": obfs4_bridge_void,
            "obfs4_bridge_drafonflybsd": obfs4_bridge_dragonflybsd,
            "obfs4_bridge_freebsd": obfs4_bridge_freebsd,
            "obfs4_bridge_openbsd": obfs4_bridge_openbsd,
            "obfs4_bridge_netbsd": obfs4_bridge_netbsd,
            "obfs4_bridge_docker": obfs4_bridge_docker,
            "snowflake_setup_debian": snowflake_setup_debian,
            "snowflake_setup_freebsd": snowflake_setup_freebsd,
            "tor_node_setup": tor_node_setup
            }

    print("+---- Tor Management  ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function name: ").lower()
    if your_function in functions:
        functions[your_function]()


if __name__ == "__main__": 
    tor_management()
