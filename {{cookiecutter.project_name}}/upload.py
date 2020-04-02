import getopt
import os
import sys
import argparse
import getpass
import subprocess

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from zipfile import ZipFile

SANDBOX_USERNAME = "sandbox"
SANDBOX_PASSWORD = "sandbox2"
SANDBOX_PORT = 22

SCRIPT = os.path.realpath(__file__)
SCRIPT_ROOT = os.path.dirname(SCRIPT)


def make_sdist():
    proc = subprocess.run(
        ["python3", "setup.py", "sdist", "--formats=zip"],
        cwd=SCRIPT_ROOT
    )
    if proc.returncode:
        raise RuntimeError("Failed to make source distribution")
    with open("version") as v:
        version = v.read().strip()
        return "dist/{{cookiecutter.package_name}}-{}.zip".format(version)


def upload(host, venv_init=True):
    # TODO: replace prints with logging to file and stdout
    print("Making distribution...", end="")
    dist_path = make_sdist()
    print("done {}".format(dist_path))
    
    print("Establishing SSH connection to {}:{}...".format(host, SANDBOX_PORT))
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    pwd = getpass.getpass("Enter password: ")
    ssh.connect(
        hostname=host,
        username=SANDBOX_USERNAME,
        password=pwd,
        port=SANDBOX_PORT,
    )
    print("Connection established")
    
    print("Preparing directory for the project...", end="")
    project_path = "/home/sandbox/player/{{cookiecutter.project_name}}"
    venv_path = "{}/venv".format(project_path)
    ssh.exec_command("mkdir -p {}".format(project_path))
    print("done")
    
    if venv_init:    
        # intialize venv for project
        print("Intializing virtual environment...", end="")
        ssh.exec_command("python3 -m venv {}".format(venv_path))
        print("done {}".format(venv_path))
    
    
    scp = SCPClient(ssh.get_transport())
    
    print("Uploading distribution ...", end="")
    scp.put(os.path.join(SCRIPT_ROOT, dist_path), project_path)
    print("done")
    
    print("Installing distribution...", end="")
    install_cmd = " ".join([
        "{}/bin/python".format(venv_path),
        "-m pip install",
        os.path.basename(dist_path),
        "-i https://pip.rozum.com/simple"
    ])
    ssh.exec_command(install_cmd)
    print("done")
    
    print("Closing SSH connection...", end="")
    scp.close()
    ssh.close()
    print("done")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    args = parser.parse_args()
    robot_host = args.host
    upload(robot_host, "{{cookiecutter.project_name}}.zip")


if __name__ == "__main__":
    main()
