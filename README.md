# Intro
This is a sample repository for integration tests between different services
using docker and docker-compose.

It tests a sample integration between a simple REST API app and vault, the
secret managing tool from Hashicorp. Vault was chosen for this sample because
it has a very simple integration, and is good for an example.

# Folder setup
`tests`: this is where the test code resides. It's just testing against an API,
so the tests can be written in any language, but I chose python. Docker compose
files are in `tests/compose`.

`repos`: This is where the source code is. If services to test reside in
different git repos they can submodule them here.

`docker`: This is for the dockerfiles and auxilary files necessary for each
repo.

# Running tests
To run the tests, you'll need a working docker environment with docker-compose
and a python environment with `nose` and `requests`.

With everything setup, running the tests just involves invoking `make test`.
