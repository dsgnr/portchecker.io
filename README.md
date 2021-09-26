<h1 align="center">Welcome to portchecker.io 👋</h1>
<p>
</p>

[![Pylint](https://github.com/dsgnr/portchecker.io/actions/workflows/pylint.yml/badge.svg)](https://github.com/dsgnr/portchecker.io/actions/workflows/pylint.yml)


This project aims to be a simple, go-to place for querying the port status for a provided hostname or IP address.
The system is API-based and making a `POST` request to the API will trigger a task to be queued in the messaging system (RabbitMQ), and executed by Celery. The user will be presented with a task ID they can then poll.

Why do we need a message queue? Simple! If traffic increases, we don't want the user to be met with a hanging API.
Therefore, the task is queued and executed as quickly as possible.

Results for the task are stored in a Redis cache for 15 minutes (to allow for the user to poll the task results at their own pace).

## 📝 To Do

- [ ] Improve Redis resilience using Sentinel
- [ ] More tests
- [ ] Kubernetes liveness/readiness
- [ ] Implement front-end
- [ ] SEO/search engine submissions
- [ ] Bugfix/security 

### 🏠 [Homepage](portchecker.io)

### ✨ [Demo](portchecker.io)

## Author

👤 **Dan Hand**

* Website: https://danielhand.io
* Github: [@dsgnr](https://github.com/dsgnr)

## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](https://github.com/dsgnr/portchecker.io/issues) if you want to contribute.<br />


## Show your support

Give a ⭐️ if this project helped you!

Running websites such as this comes with associated costs. Any donations to help the running of the site is hugely appreciated!

<a href="https://www.patreon.com/dsgnr_">
  <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="100">
</a>
<a href="https://www.paypal.com/donate?business=RNT9HTKVJ2DDJ&no_recurring=0&item_name=portchecker.io+donation&currency_code=GBP" target="_blank"><img src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_SM.gif"></a>


## 📝 License

Copyright © 2019 [Dan Hand](https://github.com/dsgnr).<br />
This project is [MIT](https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE) licensed.

---
***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
