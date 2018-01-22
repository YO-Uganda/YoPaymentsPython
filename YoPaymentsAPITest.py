import yopayments

YoPay = yopayments.YoPay("qjuysdavuab", "lgcavolbaubvojapkpabnaikaninv")

# response = YoPay.ac_deposit_funds("2567788932323", 500, "hello")
# response = YoPay.ac_withdraw_funds("256772123456", 2000, "Salary Expenses")
# response = YoPay.ac_transaction_check_status("30192910")
response = YoPay.ac_internal_transfer("UGX-MTNMM", "1000", "100048753342", "afollicle@yo.co.ug", "Medical")
# Check the transaction status
# print(response.get("Status"))
# print(response.get("TransactionReference"))

# response = YoPay.ac_acct_balance()

if response.get("Status") == "OK":
    print(response.get("Status"))
else:
    print("Python sucks..." + response.get("Status"))
