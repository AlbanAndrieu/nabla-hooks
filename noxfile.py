import nox

nox.options.sessions = "lint", "black", "test"
locations = "hooks", "tests", "noxfile.py"


@nox.session(python=False)
def test(session):
    # session.install("pytest", "pytest-cov", "pytest-asyncio")
    session.run("python", "-m", "pytest", "--cov=hooks")


@nox.session(python=False)
def lint(session):
    args = session.posargs or locations
    # session.install(
    #    "flake8",
    #    "flake8-black",
    #    "flake8-isort",
    #    "flake8-bugbear",
    #    "flake8-bandit",
    #    "flake8-annotations",
    #    "flake8-docstrings",
    # )
    session.run(
        "flake8",
        "--config=.flake8",
        "--max-line-length=88",
        "--max-complexity=12",
        *args,
    )


# TODO add safety to CI rather
# @nox.session(python=False)
# def safety(session):
#     session.install("safety")
#     session.run("safety", "check", "--file=requirements.txt", "--full-report")


@nox.session(python=False)
def black(session):
    args = session.posargs or locations
    # session.install("black")
    session.run("black", *args)
