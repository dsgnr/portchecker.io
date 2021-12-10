# Change Log

All notable changes to this project will be documented in this file.

## [1.0.8] - 2021-12-10

- Add dependabot monitoring to repository
- Allow default port to be defined as an environment variable
- Make Dockerfile serve from Nginx instead of webpack serve to improve performance
- Separate development and production environments and add docker-compose files

## [1.0.7] - 2021-12-08

- Migrate from NPM to Yarn to resolve dependencies
- Upgrade react-router-dom to v6

## [1.0.6] - 2021-11-11

- Update package.json dependencies
- Improve webui styling for when the users browser does not have JavaScript enabled

## [1.0.5] - 2021-11-07

- Move users IP detector (for form auto population) to Cloudflare DNS to avoid some spam filters
- Improve styling for pending/in-progress tasks
- Update UI to use improved Lambda API task

## [1.0.4] - 2021-11-02

- Improve results styling
- Migrate WebUI to AWS Beanstalk

## [1.0.3] - 2021-09-29

- Add Kubernetes probes for RabbitMQ
- Rename Redis manifest file and add Kubernetes probes
- Ensure the form captures errors better
- Make the form submit on return key press
- Increase the check time on front-end and API Kubernetes deployments

## [1.0.2] - 2021-09-28

- Add liveness and startup probe to api and front-end Kubernetes manifest
- Update webpack to version 5.55.0
- Add healthz for API
- Stop scaling on mobile
- Update page title
- Remove websocket for production
- Correct homepage and demo URLs in README

## [1.0.1] - 2021-09-28

- Add better form validation
- Improve CSS styling for mobile

## [1.0.0] - 2021-09-28

- Initial release

