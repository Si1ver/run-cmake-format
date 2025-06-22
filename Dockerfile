# This Dockerfile provides an environment for running cmake-format and cmake-lint.

# Stage 1
# The build image is used to prepare a python virtual environment with all dependencies installed.
FROM public.ecr.aws/docker/library/python:3.13.4-alpine3.22 AS build

# Make sure python output is not buffered and always printed instantly.
ENV PYTHONUNBUFFERED=1

# Place pipenv virtual environment in the project directory to copy it from build image to runtime image.
ENV PIPENV_VENV_IN_PROJECT=1

# The work directory `/app` is used as a best practice.
WORKDIR /app

# Copy pinned dependencies to provide reproducible builds.
COPY Pipfile Pipfile.lock ./

# Make sure the sh is used as a shell.
SHELL [ "/bin/sh", "-c" ]

# Install system dependencies and create a virtual environment using pipenv.
RUN pip install --no-cache-dir pipenv \
  && pipenv sync --clear

# Stage 2
# The runtime image is used to run the tools.
FROM public.ecr.aws/docker/library/python:3.13.4-alpine3.22

# Make sure python output is not buffered and always printed instantly.
ENV PYTHONUNBUFFERED=1

# The work directory `/app` is used as a best practice.
WORKDIR /app

# Copy python virtual environment with installed tools from build image.
COPY --from=build /app/.venv ./.venv

# Copy utility scripts.
COPY run_cmake_tool.py github_action_entrypoint.py ./

# Add virtual environment runtime directory to PATH.
ENV VIRTUAL_ENV=/app/.venv
ENV PATH=/app/.venv/bin:$PATH

# Set the cmake tools launcher script as entrypoint.
ENTRYPOINT [ "python", "run_cmake_tool.py" ]
