import yopayments

YoPay = yopayments.YoPay("jnkadfsdf", "djsfhbsjkfslfd")

response = YoPay.ac_deposit_funds("2567788932323",500,"hello")
if response.get("Status") == "OK":
    # Check the transaction status
    print(response.get("Status"))
else:
    print("Python sucks..."+response)