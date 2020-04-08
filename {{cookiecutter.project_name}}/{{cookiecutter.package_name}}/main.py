import argparse

from {{cookiecutter.package_name}} import program


def run(num_iterations: int, robot_ip: str):    
    with program.Instance(robot_ip) as p:
        p.before_all()
        for i in range(num_iterations):
            p.before_each()
            p.execute()
            p.after_each()
        p.after_all()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", 
        "--iterations", 
        type=int, 
        required=True, 
        description="Number of iterations to perform"
    )
    parser.add_argument(
        "--robot-ip", 
        required=True, 
        description="Network address of the target robotic arm"
    )
    args = parser.parse_args()
    run(args.i, args.robot_ip)
