# Yo! Payments API Python Module

Yo! Payments is a revolutionary mobile payments gateway service. Yo! Payments enables businesses to receive payments from their customers via mobile money, as well as make mobile money payments to any mobile money account holder. Yo! Payments also has the capability to send mobile calling credit ("airtime") directly to users.

Yo! Payments Python Module is a Python module that can be included in your Python project to enable seamless integration with your Python application.

## Getting Started

### Prerequisites

To use the API, you must, first of all, have a Yo! Payments Business Account. The API is not available for Personal Accounts

* Yo! Payments api_username
* Yo! Payments api_password

Import the module

```
import yopayments
```

Use the module as shown below

```
YoPay = yopayments.YoPay("yo_api_username", "yo_api_password")

YoPay.set_nonblocking(True)

response = YoPay.ac_deposit_funds("256712345678",500,"reason for payment")

if response.get("TransactionStatus") == "SUCCEEDED":
	# Payment was successful
else:
	# Payment failed
```


## Built With

 * [Python](https://www.python.org/) - Python Programming Language

## Authors

* **Aziz Kirumira** - *Initial work* - [Yo (U) Ltd](https://github.com/YO-Uganda)
* **Arnold Kunihira** - *Initial work* - [Yo (U) Ltd](https://github.com/YO-Uganda)


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

* Gerald Begumisa
* Grace Kyeyune
* Joseph Tabajjwa
