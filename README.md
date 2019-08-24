# recipe_api
REST API for working with recipes using Dhango REST Framework

## Development
The app may be developed both locally or with Docker.  For local
development you need Python 3.7 to be available on your machine.

### Automated tasks
Some steps are automated with [invoke](http://www.pyinvoke.org/).
While it is available with both Docker container and the virtual environment, 
it is recommended to install it to the system environment to be able to
run the tasks without activating the virtual environment.  The tasks are
written for Python 3.6+ (Python 3.7 is preferred), so make sure to install
[invoke](http://www.pyinvoke.org/) for the right Python version, like so:
`python3.7 -m pip install --user invoke`.

Run `inv -l` from the root directory of the repo to see all available tasks.

* `inv pin && inv update` - update `requirements.txt` according to the
  dependencies listed in `requiremensts.in`, then install all dependencies,
  including the dev ones.
* `inv run-dev` - run the app with a development server.  Before starting it
  applies DB migrations, if required.
* `inv lint && inv test` - check if the code is correct.
* `inv black` to re-format the code with the standard configuration usind
   [black](https://black.readthedocs.io/en/stable/index.html).
