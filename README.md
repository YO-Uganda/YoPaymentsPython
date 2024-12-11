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

# To test the deposit of funds API
```
YoPay = yopayments.YoPay("yo_api_username", "yo_api_password")

response = YoPay.ac_deposit_funds("256712345678", 500, "reason for payment")

if response.get("TransactionStatus") == "SUCCEEDED":
	# Payment was successful
else:
	# Payment failed
```

# To test withdraw funds API without public Key configured
```
YoPay = yopayments.YoPay("yo_api_username", "yo_api_password")
YoPay.set_external_reference("TestWithPython"+YoPay.generate_random())

response = YoPay.ac_withdraw_funds("256712345678", 500, "reason for payment")

if response.get("TransactionStatus") == "SUCCEEDED":
	# Payment was successful
else:
	# Payment failed
```

# To test withdraw funds API with public Key configured
```
YoPay = yopayments.YoPay("yo_api_username", "yo_api_password")
YoPay.set_external_reference("TestWithPython"+YoPay.generate_random())

username="yo_api_username"
account="256789092671"
amount="2000"
narrative="Reason for payments"
external_ref=YoPay.external_reference
nonce="xGLl39KNTN3467T-"+YoPay.generate_random()
data=username+amount+account+narrative+external_ref+nonce
base64_signature=YoPay.generate_public_key_signature(data)

response = YoPay.ac_withdraw_funds(account, amount, narrative,
		nonce,base64_signature)

if response.get("TransactionStatus") == "SUCCEEDED":
	# Payment was successful
else:
	# Payment failed
```

# To Test check balance API
```
YoPay = yopayments.YoPay("yo_api_username", "yo_api_password")

response = YoPay.ac_acct_balance()

if response.get("Status") == "OK":
    bal=response.get("Balance")['Currency']
	print("Balances\n...")
	for b in bal:
		print(b['Code']+"\t"+b['Balance']+"\n...")
else:
	print("There was an error processing the payment..." + response.get("StatusMessage"))
```

# To test check status API
```
YoPay = yopayments.YoPay("yo_api_username", "yo_api_password")
# you can either use the transacion reference from Yo! or private transaction reference
transactionReference="JYWLiUwLP3L3ofsTntEjeJkEoheHKyj"
private_transaction="TestWithPython" # external reference of your deposit or withdraw

response = YoPay.ac_transaction_check_status(transactionReference)

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
* Isaac Obella [wizlif](https://github.com/wizlif) for the xmltodict introduction
