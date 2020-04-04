import argparse

from {{cookiecutter.package_name}} import program


def run(num_iterations):
    try:
        program.before_all()
        for i in range(num_iterations):
            program.before_each()
            program.execute()
            program.after_each()
        program.after_all()
    except Exception as exc:
        program.on_error(exc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--iterations", 
        type=int, 
        required=True, 
        description="Number of iterations to perform"
    )
    args = parser.parse_args()
    run(args.i)
