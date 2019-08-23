"""Project automation routines."""

import tempfile
from contextlib import suppress
from pathlib import Path

from invoke import task, UnexpectedExit

APP = "recipe_api"

ROOT = Path(__file__).parent
OPENAPI_GENERATOR_VERSION = "4.0.0-beta"
CONTAINER_PORT = 8000
_default = object()


def is_docker() -> bool:
    """Check if project ran in docker."""
    with suppress(FileNotFoundError), open("/proc/self/cgroup") as file:
        for line in file:
            if "/docker/" in line:
                return True
    return False


@task
def update(ctx):
    """Install all dependencies to the virtual environment."""
    ctx.run("pip install -r dev-requirements.txt ")


@task
def pin(ctx):
    """Compile dependencies and store to requirements.txt."""
    ctx.run("CUSTOM_COMPILE_COMMAND='inv pin' pip-compile --no-index")


@task
def black(ctx):
    """Reformat the code."""
    ctx.run("black ./")


@task(
    help={
        "jar": "When set, download and invoke 'openapi-generator-cli.jar'.  "
        "Otherwise use 'openapitools/openapi-generator-cli' Docker image "
        "to validate the OpenAPI schema"
    }
)
def lint(ctx):
    """Run code linter."""

    # noinspection PyListCreation
    results = []

    results.append(ctx.run("safety check", warn=True))

    print("\n\nTypes Check:")
    results.append(ctx.run("mypy . && echo Ok", warn=True))

    print("\n\nFormatting Check:")
    results.append(ctx.run("black --check ./", warn=True))

    print("\n\nStyle Check:")
    results.append(ctx.run("flake8 --ignore=D && echo Ok", warn=True))

    print("\n\nOpenAPI Schema Check:")
    validate_schema(ctx)

    for result in results:
        if result.exited:
            raise UnexpectedExit(result)

    print("\nAll checks passed")


@task
def test(ctx):
    """Run tests for CI."""
    ctx.run(f"coverage run --source='.' manage.py test --no-input", warn=True)
    ctx.run(f"coverage report")


@task(
    pre=[pin],
    help={
        "tag": 'Docker image tag, default is "latest"',
        "yes": "Do not ask for confirmation",
        "no-cache": "Build the docker image from scratch",
    },
)
def build_docker(ctx, tag="latest", no_cache=False):
    """Build the docker image."""

    ctx.run(f"docker build -t '{APP}:{tag}' {'--no-cache' if no_cache else ''} .")
    print("Done")


@task(help={"cmd": "Command to run instead of the default one"})
def run_docker(ctx, cmd=""):
    """Run the dockerized app in production mode.

    This task requires the `.env` file to be populated.
    """
    ctx.run(f'./scripts/docker-run.sh "{cmd}"', pty=True)


@task(help={"port": f"Port number, default is {CONTAINER_PORT}"})
def run_dev(ctx, port=CONTAINER_PORT):
    """Run the app in development mode."""
    ctx.run(f"./manage.py migrate")
    ctx.run(f"./manage.py runserver 0.0.0.0:{port}")


@task
def validate_schema(ctx):
    """Check if generated OpenAPI schema meets the specification."""
    cmd = (
        f"docker run --rm -v '{ ROOT }':'{ ROOT }' "
        f"openapitools/openapi-generator-cli:v{ OPENAPI_GENERATOR_VERSION }"
    )

    with tempfile.TemporaryDirectory(dir=ROOT, prefix="client-tmp") as tempdir:
        tempdir_path = Path(tempdir)
        _generate_schema(ctx, tempdir_path / "swagger.yaml")

        ctx.run(f" { cmd } validate -i { tempdir_path / 'swagger.yaml' } --recommend")


def _generate_schema(ctx, where):
    ctx.run(
        f"./manage.py generate_swagger { where } "
        f"--format=yaml --overwrite --url http://localhost:{CONTAINER_PORT} "
        f"--settings recipe_api.settings"
    )
