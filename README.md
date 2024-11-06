<h1 align="center">portchecker.io</h1>

[portchecker.io](https://portchecker.io) is an open-source API for checking port availability on specified hostnames or IP addresses. Ideal for developers and network admins, it helps troubleshoot network setups, validate firewall rules, and assess potential access points.


## Table of contents:

- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Development](#development)
  - [Standalone](#standalone)
  - [Docker](#docker)
- [Production](#production)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)

## Getting Started
The project consists of two containers. The front-end is a static HTML file sat behind Nginx. The back-end is a simple API built using [Litestar](https://litestar.dev/).

The project aims to be super simple, with low overhead and also the least amount of dependencies as possible.

The project contains both production and development stacks. The production stack utilises `gunicorn` as the API's process manager with `uvicorn` workers. Development utilises `uvicorn` with the `--reload` parameter.

## Documentation
API routes and specification can be found at [portchecker.io/docs](https://portchecker.io/docs)


## Development

### Standalone

#### Web
> [!NOTE]  
> Uses [Node](https://nodejs.org/) version 23 and newer. Requires [Yarn](https://classic.yarnpkg.com/en/)

Bringing up the UI outside of Docker;
~~~
$ cd frontend/web
$ yarn install
$ yarn dev
~~~

portchecker.io front-end be running at [http://0.0.0.0:8080](http://0.0.0.0:8080).

#### API
> [!NOTE]  
> Uses Python 3.12. The Python environment uses [Poetry](https://pypi.org/project/poetry/) for package management. This must be installed.

~~~
$ cd backend/api
$ poetry install
$ uvicorn main:app --host 0.0.0.0 --port 8000 --reload
~~~

portchecker.io API be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).


### Docker
~~~
$ docker-compose -f docker-compose-dev.yml up --build
~~~

portchecker.io front-end will be running at [http://0.0.0.0:8080](http://0.0.0.0:8080) and the API will be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Production
### Docker
> [!NOTE]  
> Uses [ghcr.io/dsgnr/portcheckerio-web:latest](https://github.com/dsgnr/portchecker.io/pkgs/container/portcheckerio-web) and [ghcr.io/dsgnr/portcheckerio-api:latest](https://github.com/dsgnr/portchecker.io/pkgs/container/portcheckerio-api).

~~~
$ docker-compose up
~~~

portchecker.io front-end will be running at [http://0.0.0.0:8080](http://0.0.0.0:8080) and the API will be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Environment Variables
The following configuration options are available. These would be set within the Docker compose files, or in your environment if you're using portchecker standalone.

### Web
| Name             | Required? | Default | Notes                                                      |
|------------------|-----------|---------|------------------------------------------------------------|
| DEFAULT_PORT     | No        |         | Allows a default port number to be prefilled in the UI     |
| GOOGLE_ANALYTICS | No        |         | Allows for a Google Analytics tracking code to be provided |

### API
| Name          | Required? | Default | Notes                                                                                                                                                                              |
|---------------|-----------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ALLOW_PRIVATE | No        | 443     | Allows private IP addresses in [ IANA IPv4 Special Registry ]( https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml ) ranges to be checked |

## Contributing

I'm thrilled that you’re interested in contributing to this project! Here’s how you can get involved:

### How to Contribute

1. **Submit Issues**:
   - If you encounter any bugs or have suggestions for improvements, please submit an issue on our [GitHub Issues](https://github.com/dsgnr/portchecker.io/issues) page.
   - Provide as much detail as possible, including steps to reproduce and screenshots if applicable.

2. **Propose Features**:
   - Have a great idea for a new feature? Open a feature request issue in the same [GitHub Issues](https://github.com/dsgnr/portchecker.io/issues) page.
   - Describe the feature in detail and explain how it will benefit the project.

3. **Submit Pull Requests**:
   - Fork the repository and create a new branch for your changes.
   - Make your modifications and test thoroughly.
   - Open a pull request against the `devel` branch of the original repository. Include a clear description of your changes and any relevant context.

## Author

* Website: https://danielhand.io
* Github: [@dsgnr](https://github.com/dsgnr)

## Show your support

Give a ⭐️ if this project helped you!

Running websites such as this comes with associated costs. Any donations to help the running of the site is hugely appreciated!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U7U3FUX17)

The site is located on Digital Ocean. You can use the following referral link to get some credit when joining:

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=b54817e033c8&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

## License

See the [LICENSE](LICENSE) file for more details on terms and conditions.



