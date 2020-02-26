# Pulse program template

Template to create Python programs for Pulse Program Player.

## Configuration
```json
{
    "project_name": "helloworld", // name of the folder
    "package_name": "pulse_program", // name of the package. MUST be a valid python module/package name
    //help: https://docs.python-guide.org/writing/structure/#modules
    "email": "dev@rozum.com", // optional email
    "author": "Rozum Robotics", // optional author
    "url": "https://rozum.com", // optional url
    "version": "0.0.1", // initial version of the project
    "pulse_api_version": "1.6.0" //pulse-api version to use in the project
}
```

## Usage

Install cookiecutter:

`python3 -m pip install cookiecutter --user`

Go to directory where you want to start your project and initiate it:

```bash
cd workdir
cookiecutter git@dev.rozum.com:rozum-soft/utils/pulse-program-template.git
```

Fill in the fields and start developing at project_name/project_name folder.

To test that project initiated properly, run:

`pip install -e . -i https://pip.rozum.com/simple`

**Note:** It is recommended to create and activate python virtual environment
prior to execution of the command given above.

