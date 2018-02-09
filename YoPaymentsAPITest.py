import yopayments

YoPay = yopayments.YoPay("XXXXXX", "XXXXXXXX")
YoPay.set_instant_payment_notification_url("http://XXXXXXXXXXXX.com/yo/receiveIPN")
YoPay.set_external_reference("YoPaymentsAPIPythonTest")
response = YoPay.ac_deposit_funds("256700000000", 500, "Testing the python library")

if response.get("Status") == "OK":
    print(response.get("Status"))
else:
    print("There was an error processing the payment..." + response.get("StatusCode"))
