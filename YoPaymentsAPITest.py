import yopayments

YoPay = yopayments.YoPay("90001454216", "sMUw-dshF-fOku-r0Y7-oCsz-d4Xc-YM5n-RVGH")
YoPay.set_instant_payment_notification_url("http://192.168.1.30/myWork/hello.php")
YoPay.set_external_reference("TestWithPython"+YoPay.generate_random())
YoPay.set_public_key_file("keys/Yo_Uganda_Public_Certificate.crt")
YoPay.set_private_key_file("C:/Users/DELL/Desktop/learning materials/private_key.pem")

##Uncomment function call to test deposits
def test_deposit():
	response = YoPay.ac_deposit_funds("256789092671", 5000, "Testing the python library")
	if response.get("Status") == "OK":
		print("Status: " + response.get("Status")+"\n"+
		"Status Code: "+response.get("StatusCode")+"\n"+
		"Transaction Status: " + response.get("TransactionStatus")+
		"\n"+"Transaction Reference: " + response.get("TransactionReference")+
		"\n"+"Network ID: " + response.get("MNOTransactionReferenceId"))
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))
#test_deposit()

##Uncomment function call to test withdraw funds
def test_withdraw_funds():
	username="90001454216"
	account="256789092671"
	amount="7000"
	narrative="New year4"
	external_ref=YoPay.external_reference
	nonce="xGLl39KNTN3467T-"+YoPay.generate_random()
	#Concatenate data to be signed
	data=username+amount+account+narrative+external_ref+nonce
	# print(external_ref)
	# print (nonce)
	base64_signature=YoPay.generate_public_key_signature(data)
	response = YoPay.ac_withdraw_funds(
		account, amount, narrative,
		nonce,base64_signature)
	if response.get("Status") == "OK":
		print("Status: " + response.get("Status")+"\n"+
		"Status Code: "+response.get("StatusCode")+"\n"+
		"Transaction Status: " + response.get("TransactionStatus")+
		"\n"+"Transaction Reference: " + response.get("TransactionReference"))
		if response.get("MNOTransactionReferenceId") is not None:
			print("Network ID: " + response.get("MNOTransactionReferenceId"))
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))
#test_withdraw_funds()

#Uncomment function call to test checktransactionstatus
def test_check_transaction_status():
	transactionReference="JYWLiUwLP3L3ofsTntEjeJkEoheHKyjrhcQYgM5bFSSK7wIVASQsWpoYnahFvoeicc79b5687fe67c97cf3996c0e860aa3e"
	private_transaction="TestWithPython"
	response=YoPay.ac_transaction_check_status(transactionReference,
	private_transaction)
	if response.get("Status") == "OK":
	    print("Status: " + response.get("Status")+"\n"+
		"Status Code: "+response.get("StatusCode")+"\n"+
		"Transaction Status: " + response.get("TransactionStatus")+
		"\n"+"Transaction Reference: " + response.get("TransactionReference")+
		"\n"+"Network ID: " + response.get("MNOTransactionReferenceId")+
		"\n"+"Amount: " + response.get("Amount")+"\n"+
		"Amount Formatted: " + response.get("AmountFormatted")+
		"\n"+"Currency Code: " + response.get("CurrencyCode")+
		"\n"+"Transaction Initiation Date: " + response.get("TransactionInitiationDate")+
		"\n"+"Transaction Completion Date: " + response.get("TransactionCompletionDate")+
		"\n"+"IssuedReceiptNumber: " + response.get("IssuedReceiptNumber"))
	else:
	    print("There was an error processing the payment..." + response.get("StatusMessage"))	
#test_check_transaction_status()

#Uncomment function call to test check balance
def test_balance():
	response=YoPay.ac_acct_balance()
	if response.get("Status") == 'OK':
		bal=response.get("Balance")['Currency']
		print("Balances\n...")
		for b in bal:
			print(b['Code']+"\t"+b['Balance']+"\n...")
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))
#test_balance()

#Uncomment function call to test send mobile airtime
def test_send_mobile_airtime():
	msisdn="256703772798"
	amount="500"
	narrative="TestPython"
	response=YoPay.ac_send_airtime_mobile(
		msisdn,
		amount,
		narrative
	)
	if response.get("Status") == "OK":
		print("Transaction Status: " + response.get("TransactionStatus")+
		"\n"+"Transaction Reference: " + response.get("TransactionReference"))
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))
#test_send_mobile_airtime()


#Uncomment function call to test get ministatement
def test_get_ministatement():
	start_date=None
	end_date=None
	transaction_status=None
	currency_code=None
	result_set_limit=None
	transaction_entry_designation="ANY"
	external_reference=None
	response=YoPay.ac_get_ministatement(
		start_date,end_date,transaction_status,
		currency_code,result_set_limit, 
		transaction_entry_designation,external_reference
	)
	if response.get("Status") == "OK":
		print(
		"Total Transactions: " + response.get("TotalTransactions")+"\n"+
		"Returned Transactions: " + response.get("ReturnedTransactions") +"\n"
		+"Transaction Details \n==========")
		transaction=response.get("Transactions")['Transaction']
		for trans in transaction:
			print("=========\nTransaction System Id: " + trans['TransactionSystemId']+"\n"+
			"Transaction Reference: " + trans['TransactionReference']+"\n"+
			"Transaction Status: " + trans['TransactionStatus']+
			"\n"+"Initiation Date: " + trans['InitiationDate']+
			"\n"+"Completion Date: " + trans['CompletionDate']+
			"\n"+"Narrative Base64: " + trans['NarrativeBase64']+"\n"+
			"Currency : " + trans['Currency']+
			"\n"+"Amount: " + trans['Amount']+
			"\n"+"Balance: " + trans['Balance']+
			"\n"+"General Type: " + trans['GeneralType']+
			"\n"+"Detailed Type: " + trans['DetailedType'])
			if'BeneficiaryMsisdn' in trans.keys():
			    print("Beneficiary Msisdn: "+ trans['BeneficiaryMsisdn']+"\n")
			print("Beneficiary Base64: "+ str(trans['BeneficiaryBase64']))
			if 'SenderMsisdn' in trans.keys():
			    print("Sender Msisdn: " + trans['SenderMsisdn'])
			print("Sender Base64: "+ trans['SenderBase64'])
			if trans['Base64TransactionExternalReference'] is not None:
			    print("Base64 Transaction ExternalReference: "+ trans['Base64TransactionExternalReference'])
			else:
				print("Base64 Transaction ExternalReference: None")
			print("Transaction Entry Designation "+ trans['TransactionEntryDesignation'])

	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))
#test_get_ministatement()

#Uncomment function call to test verify payment notification Signature for a successful request
def test_verify_ipn_signature():
	datetime = "2014-02-07 14:48:07"
	amount = "1000"
	narrative = "SpinApp Userid:7 Number:256783086794"
	network_ref = "1327659406"
	external_ref = ""
	msisdn = "256783086794"
	signature_base64 = "05b4cTk+IDhI8aqRhsFR2zXbbl9xfWJPHO+WAn/sSWCCB0zQeePvqjUTONk6w8wcaue0YbCO2cd1ER3l0K8aJUj8Ob7Ixl7o5cNsYwCHu8cDenBFxUL8UBnlSxZAkOXf/vi47rwT3Eon9KpPJxJISLnp1vyVJgkWAH9GFsX1zLY33314sekJ1KFzPxY55vkTaUic9BfpIKsj+L4XFcgHpnJHqA20byAEE8uYmdrrSbwlCnEdqJx3ROE3gxMS/M0gAwPcjZFziawAfFaUARogFmrkRA9KKjA9XLPMvN8tN8vNwVbg8xV5p/K4pmBA3Z4DtnJAaYAeUXvgW8Dij+UDdw=="
	data = datetime+amount+narrative+network_ref+external_ref+msisdn
	response=YoPay.verify_payment_notification(data,signature_base64)
	print(response)
#test_verify_ipn_signature()


#Uncomment function call to test verify payment notification Signature for a failure request
def test_verify_failure_signature():
	transaction_init_date = "2014-02-07 14:48:07"
	failed_transaction_reference = "1000"
	verification = "05b4cTk+IDhI8aqRhsFR2zXbbl9xfWJPHO+WAn/sSWCCB0zQeePvqjUTONk6w8wcaue0YbCO2cd1ER3l0K8aJUj8Ob7Ixl7o5cNsYwCHu8cDenBFxUL8UBnlSxZAkOXf/vi47rwT3Eon9KpPJxJISLnp1vyVJgkWAH9GFsX1zLY33314sekJ1KFzPxY55vkTaUic9BfpIKsj+L4XFcgHpnJHqA20byAEE8uYmdrrSbwlCnEdqJx3ROE3gxMS/M0gAwPcjZFziawAfFaUARogFmrkRA9KKjA9XLPMvN8tN8vNwVbg8xV5p/K4pmBA3Z4DtnJAaYAeUXvgW8Dij+UDdw=="
	data = transaction_init_date+failed_transaction_reference
	response=YoPay.verify_payment_notification(data,verification)
	print(response)
#test_verify_failure_signature()

#Uncomment function call to test createBulk payment
def test_create_bulk_payment():
	username="90001454216"
	name="July salaries"
	description="For only Yo Uganda Employees"
	notification_text="Done"
	schedule_payment=None
	private_bulk_payment_request_id="20230803"+YoPay.generate_random()
	nonce="2023-"+YoPay.generate_random()
	beneficiaries=[
		{'Amount':'1000', 'AccountNumber':'256789092672','Name':'Alia', 
		'AccountType':'MOBILE MONEY'},
		{'Amount':'5000', 'AccountNumber':'256789092630','Name':'Alice', 
		'AccountType':'MOBILE MONEY'},
		{'Amount':'7000', 'AccountNumber':'256789094429','Name':'Eric', 
		'AccountType':'MOBILE MONEY'}
		]
	data=username+name+description+notification_text+private_bulk_payment_request_id+nonce
	for b in beneficiaries:
		#To be concatenated in the order the beneficiaries appear
	    data +=b['Amount']+b['AccountNumber']+b['AccountType']
	#generate signature
	base64_signature=YoPay.generate_public_key_signature(data)
	response = YoPay.create_bulky_payments(name,description,
			notification_text,private_bulk_payment_request_id,
			beneficiaries,schedule_payment,nonce,base64_signature,
			)
	print(response)
	if response.get("Status") == 'OK':
		print("Bulk Payment RequestIdentifier: " + response.get("BulkPaymentRequestIdentifier"))
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))
#test_create_bulk_payment()

#Uncomment function call to test check bulk payment status
def test_check_bulk_payment_status():
	bulk_payment_request_identifier="2023080312BULKPAY3703"
	private_bulk_payment_request_id=None
	response=YoPay.check_bulk_payment_status(
		bulk_payment_request_identifier,
	    private_bulk_payment_request_id
	)
	if response.get("Status") == 'OK':
		print("Activity Status: "+response.get("ActivityStatus"))
		if "PauseReason" in response.keys():
			print("Pause Reason: "+response.get("PauseReason"))
		print("AuthorizationStatus: " + response.get("AuthorizationStatus"))
		if "TimeLeftToRun" in response.keys():
			print("Time Left ToRun: "+ response.get("TimeLeftToRun"))
		print("Number Of Beneficiaries: " + response.get("NumberOfBeneficiaries")+
		"\n"+"Number Of Beneficiaries Paid: " + response.get("NumberOfBeneficiariesPaid")+
		"\n"+"Number Of Beneficiaries Unpaid: " + response.get("NumberOfBeneficiariesUnpaid")+"\n"+
		"Percent Progress: " + response.get("PercentProgress")+"\n"+
		"Beneficiaries========")
		beneficiary=response.get("Beneficiaries")['Beneficiary']
		for b in beneficiary :
			print("=========\nAmount: " + b['Amount']+"\n"+
			"Account Number: " + b['AccountNumber'])
			if "Name" in b.keys():
				print("Name:"+ b['Name'])
			print("Account Type: " + b['AccountType']+
			"\n"+"Status: " + b['Status'])
			print("Low Level Status: " + b['LowLevelStatus'])
			if "LowLevelErrorMessage" in b.keys():
				print("Low Level ErrorMessage : " + b['LowLevelErrorMessage'])
			if "LowLevelErrorMessageNegative" in b.keys():
				print("Low Level ErrorMessage Negative: " + str(b['LowLevelErrorMessageNegative']))
			if "ProviderReference" in b.keys():
				print("Provider Reference: " + b['ProviderReference'])
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))
#test_check_bulk_payment_status()

#Uncomment function call to test pause of bulk payment
def test_pause_bulk_payment():
	bulk_payment_request_identifier="2023080312BULKPAY3703"
	pause_reason="Mistake"
	response=YoPay.pause_bulk_payment(bulk_payment_request_identifier,pause_reason)
	if response.get("Status") == 'OK':
		print("Status: "+ response.get("Status"))
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))
#test_pause_bulk_payment()

#Uncomment function call to test resume of bulk payment
def test_resume_bulk_payment():
	bulk_payment_request_identifier="2023080312BULKPAY3703"
	response=YoPay.resume_bulk_payment(bulk_payment_request_identifier)
	if response.get("Status") == 'OK':
		print("Status: "+ response.get("Status"))
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))
#test_resume_bulk_payment()

#Uncomment function call to test cancel of bulk payment
def test_cancel_bulk_payment():
	bulk_payment_request_identifier="2023080312BULKPAY3703"
	response=YoPay.cancel_bulk_payment(bulk_payment_request_identifier)
	if response.get("Status") == 'OK':
		print("Status: "+ response.get("Status"))
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))

#test_cancel_bulk_payment()

#Test withdraw to bank
def test_withdraw_funds_to_bank():
	username="90001454216"
	amount="70000"
	currency_code="UGX"
	bank_account_name="ALIYINZA MERCY"
	bank_account_number="3202369445"
	bank_account_identifier="d1fe173d08e959397adf34b1d77e88d7"
	transfer_type="RTGS"
	transaction_reference="TestBankTransfer"+YoPay.generate_random()
	nonce="BankTransfer-"+YoPay.generate_random()
	#Concatenate data to be signed
	data=username+amount+currency_code+bank_account_name+bank_account_number+bank_account_identifier+transfer_type+transaction_reference+nonce
	base64_signature=YoPay.generate_public_key_signature(data)
	response = YoPay.ac_withdraw_funds_to_bank(
		amount, currency_code,bank_account_name,bank_account_number,
		bank_account_identifier,transfer_type,transaction_reference,
		nonce,base64_signature)
	if response.get("Status") == "OK":
		print("Status: " + response.get("Status")+"\n"+
		"Status Code: "+response.get("StatusCode")+"\n"+
		"Settlement Identifier: " + response.get("SettlementTransactionIdentifier"))
	else:
		print("There was an error processing the payment..." + response.get("StatusMessage"))

#test_withdraw_funds_to_bank()





		
		
	

