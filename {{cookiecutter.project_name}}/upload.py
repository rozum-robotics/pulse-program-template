import getopt
import os
import sys
import argparse
import getpass
import subprocess
import logging

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from zipfile import ZipFile

SANDBOX_USERNAME = "sandbox"
SANDBOX_PORT = 22

SCRIPT = os.path.realpath(__file__)
SCRIPT_ROOT = os.path.dirname(SCRIPT)


def make_logger(verbose_enabled: bool, file_enabled: bool):
    logger = logging.getLogger(__name__)
    if verbose_enabled:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if file_enabled:
        fh = logging.FileHandler("upload.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def wait_cmd(stds):
    for s in stds:
        s.channel.recv_exit_status()
    return stds


def make_sdist():
    proc = subprocess.run(
        ["python", "setup.py", "sdist", "--formats=zip"], cwd=SCRIPT_ROOT
    )
    if proc.returncode:
        raise RuntimeError("Failed to make source distribution")
    with open("version") as v:
        version = v.read().strip()
        return "dist/{{cookiecutter.project_name}}-{}.zip".format(version)


def upload(host, port, log, venv_init=True):
    log.debug("Making distribution...")
    dist_path = make_sdist()
    log.debug("Distribution done {}".format(dist_path))
    log.debug("Establishing SSH connection to {}:{}...".format(host, port))
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    pwd = getpass.getpass("Enter password: ")
    ssh.connect(
        hostname=host,
        username=SANDBOX_USERNAME,
        password=pwd,
        port=port,
        allow_agent=False,
        look_for_keys=False,
    )
    log.debug("Connection established")

    log.debug("Preparing directory for the project...")
    project_path = "/home/sandbox/player/{{cookiecutter.project_name}}"
    venv_path = "{}/venv".format(project_path)
    ssh.exec_command("mkdir -p {}".format(project_path))
    log.debug("Directory done")

    if venv_init:
        # intialize venv for project
        log.debug("Intializing virtual environment...")
        wait_cmd(ssh.exec_command("python3 -m venv {}".format(venv_path)))
        log.debug("Virtual environment initialized {}".format(venv_path))

    log.debug("Uploading distribution ...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(os.path.join(SCRIPT_ROOT, dist_path), project_path)
    log.debug("Distribution uploaded")

    log.debug("Installing distribution...")
    install_cmd = " ".join(
        [
            "cd {} &&".format(project_path),
            "venv/bin/python",
            "-m pip install",
            os.path.basename(dist_path),
            "pulse-executor -U",
        ]
    )
    wait_cmd(ssh.exec_command(install_cmd))
    log.debug("Distribution installed")

    chown_cmd = " ".join(
        ["cd {} &&".format(project_path), "chown", "-R", ":sandbox", "."]
    )
    wait_cmd(ssh.exec_command(chown_cmd))
    log.debug("Changed ownership for project files")

    log.debug("Closing SSH connection...")
    ssh.close()
    log.debug("SSH connection closed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument(
        "--port", type=int, default=SANDBOX_PORT, required=False
    )
    parser.add_argument("--verbose", action="store_true", required=False)
    parser.add_argument("--dump-log", action="store_true", required=False)
    args = parser.parse_args()
    robot_host, robot_port = args.host, args.port
    verbose_logging, file_logging = args.verbose, args.dump_log
    log = make_logger(verbose_logging, file_logging)
    try:
        log.info("Upload started")
        upload(robot_host, robot_port, log)
    except Exception as e:
        log.error("Upload failed")
        log.error(e)
    else:
        log.info("Upload finished successfully")


if __name__ == "__main__":
    main()
