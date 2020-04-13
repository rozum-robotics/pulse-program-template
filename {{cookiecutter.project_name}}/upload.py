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
SANDBOX_PORT = 22

SCRIPT = os.path.realpath(__file__)
SCRIPT_ROOT = os.path.dirname(SCRIPT)


def wait_cmd(stds):
    for s in stds:
        s.channel.recv_exit_status()
    return stds


def make_sdist():
    proc = subprocess.run(
        ["python3", "setup.py", "sdist", "--formats=zip"], cwd=SCRIPT_ROOT
    )
    if proc.returncode:
        raise RuntimeError("Failed to make source distribution")
    with open("version") as v:
        version = v.read().strip()
        return "dist/{{cookiecutter.project_name}}-{}.zip".format(version)


def upload(host, port, venv_init=True):
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
        wait_cmd(ssh.exec_command("python3 -m venv {}".format(venv_path)))
        print("done {}".format(venv_path))

    print("Uploading distribution ...", end="")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(os.path.join(SCRIPT_ROOT, dist_path), project_path)
    print("done")

    print("Installing distribution...", end="")
    install_cmd = " ".join(
        [
            "cd {} &&".format(project_path),
            "venv/bin/python",
            "-m pip install",
            os.path.basename(dist_path),
            "pulse-executor==0.0.1.dev0",
            "-i https://pip.rozum.com/simple",
        ]
    )
    wait_cmd(ssh.exec_command(install_cmd))
    print("done")

    print("Closing SSH connection...", end="")
    ssh.close()
    print("done")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument(
        "--port", type=int, default=SANDBOX_PORT, required=False
    )
    args = parser.parse_args()
    robot_host, robot_port = args.host, args.port
    upload(robot_host, robot_port)


if __name__ == "__main__":
    main()
