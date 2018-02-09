import yopayments

YoPay = yopayments.YoPay("100017341111", "zxfV-COuR-lZJs-li2v-xreU-gNDS-A7Jk-D0Ea")
# YoPay.set_instant_payment_notification_url("http://165.227.133.30/yo/YoPaymentsIPN_PHP/index.php")
# YoPay.set_external_reference("AzizPythonTest2")
# response = YoPay.ac_deposit_funds("256779664901", 500, "Testing the python library 1")
response = YoPay.ac_acct_balance()
print(response)

if response.get("Status") == "OK":
    print(response.get("Status"))
else:
    print("Python sucks..." + response.get("Status"))
