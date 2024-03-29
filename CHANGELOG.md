# Change Log

All notable changes to this project will be documented in this file.

## [2.0.0b] - 2023-07-23

Rewrites the front-end to a single page HTML instead of React.
This is an incredibly small and simple application, so maintaining
the various dependencies that come with a React site is a bit overkill.

The backend API is also refactored to move away from using AWS Lambda functions.
The usage and popularity of this site is absolutely fantastic, but also quite unexpected.
There have been numerous overage fees within the AWS free-tier limits,
which is not sustainable without donations from users.

I see discussions related to portchecker.io, and some users have asked about self hosting.
The changes made here also means that this project is more portable/not vendor locked
in and only requires Docker to run.

As always, feedback and recommendations are more than welcomed!

Please consider the rewritten front-end and API as a beta release.

## [1.0.11] - 2021-12-27

- Improve various UI elements for better experience
- Update production docker-compose file to use GitHub container registry instead of Docker Hub

## [1.0.10] - 2021-12-13

- Add GitHub action to build images when new releases are tagged
- Add GitHub action to perform CodeQL Analysis and add badge to README
- Bump @emotion/babel-plugin from 11.3.0 to 11.7.1
- Bump @svgr/webpack from 6.1.1 to 6.1.2
- Bump postcss from 8.4.4 to 8.4.5
- Bump @emotion/react from 11.7.0 to 11.7.1
- Bump react-router-dom from 6.0.2 to 6.1.1

## [1.0.9] - 2021-12-10

- Resolve console warning about undefined DEFAULT_PORT var in production

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

