import getopt
import os
import sys
import argparse
import getpass

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from zipfile import ZipFile

SANDBOX_USERNAME = "sandbox"
SANDBOX_PASSWORD = "sandbox2"
SANDBOX_PORT = 22

SCRIPT = os.path.realpath(__file__)
SCRIPT_ROOT = os.path.dirname(SCRIPT)


def zip_all():
    file_exclusions = [
        "{{cookiecutter.project_name}}.zip",
        ".gitignore",
        "development.txt",
    ]
    dir_exclusions = ["venv", "test"]

    with ZipFile("{{cookiecutter.project_name}}.zip", "w") as zip_file:
        for root, dirs, files in os.walk(SCRIPT_ROOT, topdown=True):
            dirs[:] = [d for d in dirs if d not in dir_exclusions]
            
            rel_root = os.path.relpath(root, SCRIPT_ROOT)

            for f in files:
                if f not in file_exclusions:
                    zip_file.write(os.path.join(rel_root, f))


def upload(host, zip_path):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    pwd = getpass.getpass("Enter password: ")
    ssh.connect(
        hostname=host,
        username=SANDBOX_USERNAME,
        password=pwd,
        port=SANDBOX_PORT,
    )
    ssh.exec_command("mkdir -p /home/sandbox/player")

    scp = SCPClient(ssh.get_transport())
    scp.put(os.path.join(SCRIPT_ROOT, zip_path), "/home/sandbox/player")

    ssh.exec_command(
        f"unzip /home/sandbox/player/{zip_path} -d /home/sandbox/player/{{cookiecutter.project_name}}"
    )
    ssh.exec_command(
        "/home/sandbox/player/{{cookiecutter.project_name}}/init.sh"
    )

    scp.close()
    ssh.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    args = parser.parse_args()
    robot_host = args.host
    print(f"Uploading project to {robot_host}")
    zip_all()

    upload(robot_host, "{{cookiecutter.project_name}}.zip")


if __name__ == "__main__":
    main()
