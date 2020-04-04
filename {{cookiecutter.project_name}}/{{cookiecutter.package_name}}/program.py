from pulseapi import RobotPulse


robot = RobotPulse("localhost:8081")


def before_all():
    print("Before all")


def before_each():
    print("Before each")


def execute():
    print("Execution")


def after_each():
    print("After each")


def after_all():
    print("After all")


def on_error(exc):
    print("On error")
