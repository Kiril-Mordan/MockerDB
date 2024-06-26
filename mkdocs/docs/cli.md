
``` bash
mockerdb --help
```

```
Usage: mockerdb [OPTIONS] COMMAND [ARGS]...

  Mocker-db CLI tool

Options:
  --help  Show this message and exit.

Commands:
  runserver  Run the FastAPI server for MockerDB.
```

Mocker-db exists as API that can be pulled from [`dockerhub`](https://hub.docker.com/r/kyriosskia/mocker-db) as docker image. This pulls the code that functions within that docker image into some cached directory and runs uvicorn fastapi app from there, also saving mocker state there is persist path is not provided.

``` bash
mockerdb runserver  --help
```

```
Usage: mockerdb runserver [OPTIONS]

  Run the FastAPI server for MockerDB.

Options:
  --persist-path TEXT  Path where cache data will be saved. Path will be
                       cached.
  --repo-url TEXT      The URL of the GitHub repository to clone.
  --host TEXT          The host to bind to.
  --port INTEGER       The port to bind to.
  --reload             Enable auto-reload.
  --dump-cache         Overwrites existing cache.
  --help               Show this message and exit.
```
