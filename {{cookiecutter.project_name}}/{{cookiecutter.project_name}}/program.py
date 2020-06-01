from pulseapi import RobotPulse



class Instance:
    def __init__(self, robot_ip: str, *args, **kwargs):
        self._robot_ip = robot_ip
    
    def __enter__(self):
        self.robot = RobotPulse(self._robot_ip)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None and exc_type != SystemExit:
            self.on_error(exc_value)
    
    def before_all(self):
        print("Before all")

    def before_each(self):
        print("Before each")

    def execute(self):
        print("Execution")

    def after_each(self):
        print("After each")

    def after_all(self):
        # do not use stdout in this block in the program
        # that is uploaded to the robot
        pass

    def on_error(self, exc_value):
        print("On error")
