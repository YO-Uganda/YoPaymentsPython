import yopayments

YoPay = yopayments.YoPay("jxdfugnfjhd", "qkqbvfknejkwkksbkv")

# response = YoPay.ac_deposit_funds("2567788932323", 500, "hello")
# response = YoPay.ac_transaction_check_status("30192910")
# response = YoPay.ac_internal_transfer("Ugx", 1000, "100953496445", "akambugu@gmail.com", "Medical")
# response = YoPay.ac_withdraw_funds("256772123456", 2000, "Salary Expenses")
# if response.get("TransactionReference") == "30192910":
# Check the transaction status
# print(response.get("Status"))
# print(response.get("TransactionReference"))

response = YoPay.ac_acct_balance()

# if response.get("TransactionReference") == "30192910":
#     # if response.get("MNOTransactionReferenceId") == "330192910":
#     print(response.get("TransactionReference"))
# else:
#     # print("Python sucks..." + response.get("Status"))
#     print("Python sucks..." + response.get("TransactionReference"))
