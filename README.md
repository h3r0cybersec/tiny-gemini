# Gemini Server

Thread gemini-protocol server powered by python 3🎉. **This project is at early stages of development**.

Summary:

1. 💣[Features](#features)
2. 📄[Installation instructions](#installation)
    1. 🔒[Self-Signed certificate generation](#self-signied-certificate-generation)
    2. 📁[Server directory structure](#server-directory-structure)
3. ⚙️[Server Configuration](#server-configurations)
    1. [Simple example](#simple-example)
    1. [Testing server](#testing-server)
1. 💻[Development Status](#development-status)
1. 💡[Suggestions](#suggestions)

## Features

- [X] Mini framework for creating gemini server
  - [X] use of TLS encryption
  - [X] basic system to dynamically evaluate given variables in .gmi files
  - [X] simple configurations

other's features will comming soon!

## Installation

Download repo:

```sh
git clone https://github.com/h3r0cybersec/tiny-gemini.git
cd tiny-gemini
```

from inside the project install and activate a virtualenv:

```sh
python3 -m venv .venv
# don't forget this !
source .venv/bin/activate
```

install given *requirements.txt*

```sh
pip install -r requirements.txt
```

and finally install `tgmi` package

```sh
pip install .
# or
python setup.py install .
```

Now let's have a look how to generate a new tls certificate.

### Self Signied Certificate Generation

All the certificates generated during this phase should be placed inside **certs/** folder in server root directory as stated [here](#folders-and-files-meaning).

#### Server Certificate

`openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt`

#### Client Certificate

`openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt`

more informations [here](https://www.electricmonk.nl/log/2018/06/02/ssl-tls-client-certificate-verification-with-python-v3-4-sslcontext/).

That's it, now you can shape your space in this new world 👏🏻😁.

Don't know how to start ? Take a look inside `tgmi/example` folder for a simple example.

## Server Configurations

These are for now allowed server configurations:

| CONFIGURATION | DEFAULT |
| ------------- | ------- |
| HOST | localhost |
| PORT | 1965 |
| PUBLIC_FOLDER | default to current server `public` folder|
| SERVER_CRT | default to `tgmi/certs/server.crt` self-signed dummy certificate |
| SERVER_KEY | default to `tgmi/certs/server.key` dummy server key |
| CLIENT_CRT | default to `tgmi/certs/client.crt` dummy client key |

to configure a server can we do like this way:

```py
from tgmi.core.server import GeminiServer

# main logics
with GeminiServer({"HOST" : "192.168.1.2", "PORT": "1966"}) as server:
                  # ovveride default 'HOST' and 'PORT'
    server.add_route(...)
    # other routes
    ...
    
    # run server
    server.serve_forever()

...
```

### Server Directory Structure

Servers should be structured according to this directory tree:

```txt
example/
├── app.py
├── certs
│   ├── client.crt
│   ├── client.key
│   ├── server.crt
│   └── server.key
├── public
│   └── index.gmi
└── routes
    ├── __init__.py
    └── index.py
```

#### folders and files meaning

| FILES | MEANING |
| ----- | ------- |
| app.py  | main file thats run the server |
| certs/  | folder that contains all needed certificates |
| public/ | folder that contains all public exposed files |
| routes/ | folder with all route's controller |

## Simple Example

Inside `tgmi/example` folder, will be placed examples that will show all the functionalities that will be implemented in the project. Just copy the *example* you want and start server with `python app.py`.

### Testing Server

To see contents that your server expose in the Gemini space, you should use a specifics gemini client.

For personally usage i use [Lagrange](https://gmi.skyjake.fi/lagrange/) a very beautiful GUI client.

For fast tests, in this repo, inside `tgmi/toolbox` folder there's a simplyfied version of a Gemini capable client, the same using for the testing suite.

## Development Status

- [X] basic server implementation
- [X] basic system to dynamically evaluate given variables in .gmi files
- [ ] implement cli tool to handle server configuration:
  - [ ] add `--skeleton` functionality for server directory tree initialization
  - [ ] add `--run` functionality to run a server
  - [ ] add `--routes` functionality to show all configured routes for the server without running it
- [ ] implement security test
- [ ] implement auto-reload for dev mode
- [ ] implement access/error log into a file
- [ ] implement other test cases
- [ ] implement TLS certificate deep checks
- [ ] implement functionality to handle static file server, for staticaly serve root folder files
- [ ] implement functionality to handle *cgi* script, [RFC 3875](https://datatracker.ietf.org/doc/html/rfc3875)
- [ ] implement **Virtual Host Named Based** system
- [ ] codebase improve
  - [ ] better code refactoring
  - [ ] syntactic sugar

## Suggestions

If want you like to contribute to the project or have new features ideas create a new *issue* and let me know, and thanks you for your help.
