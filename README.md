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
> Uses [Node](https://nodejs.org/) version 25 and newer. Requires [Yarn](https://classic.yarnpkg.com/en/)

Bringing up the UI outside of Docker;

```
$ cd frontend/web
$ yarn install
$ yarn dev
```

portchecker.io front-end be running at [http://0.0.0.0:8080](http://0.0.0.0:8080).

#### API

> [!NOTE]
> Uses Python 3.13. The Python environment uses [Poetry](https://pypi.org/project/poetry/) for package management. This must be installed.

```
$ cd backend/api
$ poetry install
$ uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

portchecker.io API be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).

### Docker

```
$ docker-compose -f docker-compose-dev.yml up --build
```

portchecker.io front-end will be running at [http://0.0.0.0:8080](http://0.0.0.0:8080) and the API will be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Production

### Docker

> [!NOTE]
> Uses [ghcr.io/dsgnr/portcheckerio-web:latest](https://github.com/dsgnr/portchecker.io/pkgs/container/portcheckerio-web) and [ghcr.io/dsgnr/portcheckerio-api:latest](https://github.com/dsgnr/portchecker.io/pkgs/container/portcheckerio-api).

```
$ docker-compose up
```

portchecker.io front-end will be running at [http://0.0.0.0:8080](http://0.0.0.0:8080) and the API will be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Environment Variables

The following configuration options are available. These would be set within the Docker compose files, or in your environment if you're using portchecker standalone.

### Web

| Name             | Required? | Default         | Notes                                                                                    |
| ---------------- | --------- | --------------- | ---------------------------------------------------------------------------------------- |
| API_URL          | No        | http://api:8000 | The URL of the API service if changed from the default. The scheme and port is required. |
| DEFAULT_HOST     | No        |                 | Allows a default host address value to be prefille in the in the UI. Defaults to external/WAN IP if not set                                   |
| DEFAULT_PORT     | No        | 443             | Allows a default port number to be prefilled in the UI                                   |

### API

| Name          | Required? | Default | Notes                                                                                                                                                                            |
| ------------- | --------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ALLOW_PRIVATE | No        | False   | Allows private IP addresses in [ IANA IPv4 Special Registry ](https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml) ranges to be checked |


## Monitoring

A Prometheus `/metrics` endpoint is available for capturing metrics about the API endpoints, their response times and status codes. Since some endpoints have a hostname and variables provided via the path, these are grouped to anonymise them.

An example Grafana dashboard can be seen at [grafana/README.md](grafana/README.md).

Add your instance to your Prometheus config using the following config (be sure to update the scrape target to suit your needs):
~~~ yaml
- job_name: 'portchecker'
  static_configs:
  - targets:
    - 'https://portchecker.io'
~~~

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

## Spotlight

Where this project has been mentioned.

[JC Laforge Tech - Check Open Ports with PortChecker.io](https://www.youtube.com/watch?v=jAfo36A-rfA)

[![JC Laforge Tech - Check Open Ports with PortChecker.io](https://img.youtube.com/vi/jAfo36A-rfA/0.jpg)](https://www.youtube.com/watch?v=jAfo36A-rfA)

[My Server Cloud - Installation of PortChecker on docker | Check for Open Ports EASILY](https://www.youtube.com/watch?v=HTy5_-YiaHg)

[![My Server Cloud - Installation of PortChecker on docker | Check for Open Ports EASILY](https://img.youtube.com/vi/HTy5_-YiaHg/0.jpg)](https://www.youtube.com/watch?v=HTy5_-YiaHg)

[DB Tech - PortChecker - Check for Open Ports EASILY (Docker Tutorial)](https://www.youtube.com/watch?v=0EgbXY0ZaeU)

[![DB Tech - PortChecker - Check for Open Ports EASILY (Docker Tutorial)](https://img.youtube.com/vi/0EgbXY0ZaeU/0.jpg)](https://www.youtube.com/watch?v=0EgbXY0ZaeU)

[SYNACK Time - Portchecker.io Tutorial: Open Source Scanner with API Integration & Self-Hosting](https://www.youtube.com/watch?v=1qgFQtMMT60)
[![SYNACK Time - Portchecker.io Tutorial: Open Source Scanner with API Integration & Self-Hosting](https://img.youtube.com/vi/1qgFQtMMT60/0.jpg)](https://www.youtube.com/watch?v=1qgFQtMMT60)

[selfh.st - This Week in Self-Hosted (8 November 2024)](https://selfh.st/newsletter/2024-11-08/)

## Author

- Website: https://danielhand.io
- Github: [@dsgnr](https://github.com/dsgnr)

## Show your support

Give a ⭐️ if this project helped you!

Running websites such as this comes with associated costs. Any donations to help the running of the site is hugely appreciated!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U7U3FUX17)

The site is located on Digital Ocean. You can use the following referral link to get some credit when joining:

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=b54817e033c8&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

## License

See the [LICENSE](LICENSE) file for more details on terms and conditions.
