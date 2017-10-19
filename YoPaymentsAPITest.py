import yopayments

YoPay = yopayments.YoPay("jnkadfsdf", "djsfhbsjkfslfd")

# response = YoPay.ac_deposit_funds("2567788932323", 500, "hello")
response = YoPay.ac_transaction_check_status("30192910")
if response.get("TransactionReference") == "30192910":
    # Check the transaction status
    # print(response.get("Status"))
    print(response.get("TransactionReference"))
else:
    # print("Python sucks..." + response.get("Status"))
    print("Python sucks..." + response.get("TransactionReference"))
