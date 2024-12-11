import requests
import xmltodict
import hashlib
import OpenSSL
from OpenSSL import crypto
import base64
import random
import string


class YoPay:
    # The External Reference variable
    # Optional:
    # An External Reference is something which yourself and the beneficiary agree upon
    # e.g. an invoice number
    # Default: None

    external_reference = None

    # The Internal Reference variable
    # Optional:
    # An Internal Reference is a reference code related to another Yo! Payments system transaction
    # If you are unsure about the meaning of this field, leave it as None
    # Default: None

    internal_reference = None

    # The Provider Reference Text variable
    # A text you wish to be presented in any confirmation message which the mobile money provider
    # network sends to the subscriber upon successful completion of the transaction.
    # Some mobile money providers automatically send a confirmatory text message to the subscriber
    # upon completion of transactions. This parameter allows you to provide some text which will
    # be appended to any such confirmatory message sent to the subscriber.
    # Default: None

    provider_reference_text = None

    # The Instant Payment Notification URL variable
    # Optional:
    # A valid URL which is notified as soon as funds are successfully deposited into your account.
    # A payment notification will be sent to this URL.
    # It must be properly URL encoded.
    # e.g. http://ipnurl?key1=This+value+has+encoded+white+spaces&key2=value
    # Any special XML Characters must be escaped or your request will fail
    # e.g. http://ipnurl?key1=This+value+has+encoded+white+spaces&amp;key2=value
    # Default: None

    instant_payment_notification_url = None

    # The Instant Failure Notification URL variable
    # Optional:
    # A valid URL which is notified as soon as your deposit request fails
    # A failure notification will be sent to this URL.
    # It must be properly URL encoded.
    # e.g. http://failureurl?key1=This+value+has+encoded+white+spaces&key2=value
    # Any special XML Characters must be escaped or your request will fail
    # e.g. http://failureurl?key1=This+value+has+encoded+white+spaces&amp;key2=value
    # Default: None

    instant_failure_notification_url = None

    # The Non Blocking Request variable
    # Optional:
    # Whether the connection to the Yo! Payments Gateway is maintained until your request is
    # fulfilled. "FALSE" maintains the connection till the request is complete.
    # Default: "FALSE"
    # Options: "FALSE", "TRUE".

    nonBlocking = False

    # The Authentication Signature Base64 variable
    # Optional.
    # It may be required to authenticate certain deposit requests.

    authentication_signature_base64 = None
    
    #Public key file for signature verification
    public_key_file=None

    # The private key file  variable
    # Optional
    # May be required for to generate RSA signature

    private_key_file = None

    # The Yo Payments API URL
    # Required:
    # Default: "https://paymentsapi1.yo.co.ug/ybs/task.php"
    # Options:
    # * "https://paymentsapi1.yo.co.ug/ybs/task.php",
    # * "https://paymentsapi2.yo.co.ug/ybs/task.php",
    # * "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php" For Sandbox tests

    url = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"

    def __init__(self, username, password):
        """
        YoAPI constructor.

        :param username: username
        :type username:
        :param password: password
        :type password:
        """
        self.username = username
        self.password = password

    def get_username(self):
        """

        :return: returns the username
        :rtype: str
        """
        return self.username

    def get_password(self):
        """

        :return: returns the password
        :rtype: str
        """
        return self.password

    def set_non_blocking(self, non_blocking):
        """
        Set the NonBlocking Variable

        :param non_blocking:
        :type non_blocking:
        """
        self.nonBlocking = non_blocking

    def set_url(self, url):
        """
        Set the YO URL

        :param url: yoURL, The URL to submit API requests to
        :type url: str
        """
        self.url = url

    def set_external_reference(self, external_reference):
        """
        Set the External Reference

        :param external_reference: external_reference Used when submitting payment requests
        :type external_reference:
        """
        self.external_reference = external_reference

    def set_internal_reference(self, internal_reference):
        """
        Set the Internal Reference

        :param internal_reference: internal_reference Used when submitting payment requests
        :type internal_reference:
        """
        self.internal_reference = internal_reference

    def set_instant_payment_notification_url(self, instant_payment_notification_url):
        """
        Set the Instant Payment Notification URL

        :param instant_payment_notification_url: instant_notification_url Useful for nonblocking requests
        :type instant_payment_notification_url:
        """
        self.instant_payment_notification_url = instant_payment_notification_url

    def set_instant_failure_notification_url(self, instant_failure_notification_url):
        """
        Set the Instant Failure Notification URL

        :param instant_failure_notification_url: failure_notification_url Useful for nonblocking requests
        :type instant_failure_notification_url:
        """
        self.instant_failure_notification_url = instant_failure_notification_url

    def set_authentication_signature_base64(self, authentication_signature_base64):
        """
        Set the Authentication Signature Base64

        :param authentication_signature_base64 : failure_notification_url Useful for nonblocking requests
        :type
        """
        self.authentication_signature_base64 = authentication_signature_base64

    def get_authentication_signature_base64(self):
        """

        :return: Returns the Authentication Signature Base64 Variable
        :rtype: str
        """
        return self.authentication_signature_base64

    def set_public_key_file(self, public_key_file):
        """
        Set the public key file location

        :param public_key_file : Useful in signature verification for both successful and Failure IPNS
        :type
        """
        self.public_key_file = public_key_file

    def get_public_key_file(self):
        """

        :return: Returns the public key file location variable
        :rtype: str
        """
        return self.public_key_file
    
    def set_private_key_file(self, private_key_file):
        """
        Set the private key file location

        :param private_key_file : Useful in signature generation for both withdraws and bulk payments
        """
        self.private_key_file = private_key_file

    def get_private_key_file(self):
        """

        :return: Returns the private key file location variable
        :rtype: str
        """
        return self.private_key_file


    def ac_deposit_funds(self, msisdn, amount, narrative):
        """
        Request Mobile Money User to deposit funds into your account
        Shortly after you submit this request, the mobile money user receives an on-screen
        notification on their mobile phone. The notification informs the mobile money user about
        your request to transfer funds out of their account and requests them to authorize the
        request to complete the transaction.
        This request is not supported by all mobile money operator networks

        :param msisdn: The mobile money phone number in the format 256772123456
        :type msisdn:
        :param amount: The amount of money to deposit into your account (floats are supported)
        :type amount:
        :param narrative: The reason for the mobile money user to deposit funds
        :type narrative:
        :return:
        :rtype:
        """
        xml = '<?xml version="1.0" encoding="UTF-8" ?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>" + self.username + "</APIUsername>"
        xml += "<APIPassword>" + self.password + "</APIPassword>"
        xml += "<Method>acdepositfunds</Method>"
        xml += "<NonBlocking>TRUE</NonBlocking>" if self.nonBlocking else "<NonBlocking>FALSE</NonBlocking>"
        xml += "<Amount>" + str(amount) + "</Amount>"
        xml += "<Account>" + msisdn + "</Account>"
        xml += "<Narrative>" + narrative + "</Narrative>"
        if self.external_reference is not None:
            xml += "<ExternalReference>" + self.external_reference + "</ExternalReference>"
        if self.internal_reference is not None:
            xml += "<InternalReference>" + self.internal_reference + "</InternalReference>"
        if self.instant_payment_notification_url is not None:
            xml += "<InstantNotificationUrl>" + self.instant_payment_notification_url + "</InstantNotificationUrl>"
        if self.instant_failure_notification_url is not None:
            xml += "<FailureNotificationUrl>" + self.instant_failure_notification_url + "</FailureNotificationUrl>"
        if self.authentication_signature_base64:
            xml += "<AuthenticationSignatureBase64>" + self.authentication_signature_base64 + "</AuthenticationSignatureBase64>"
        xml += "</Request>"
        xml += "</AutoCreate>"

        response = self.__get_xml_response(xml)
        return self.__parse_response(response)

    def ac_transaction_check_status(self, transaction_reference, private_transaction=None):
        """
        Check the status of a transaction that was earlier submitted for processing.
        Its particularly useful where the NonBlocking is set to TRUE.
        It can also be used to check on any other transaction on the system.

        :param transaction_reference: The response from the Yo! Payments
        Gateway that uniquely identifies the transaction whose status you are checking
        :type transaction_reference: str
        :param private_transaction: private_transaction_reference, The External Reference
        that was used to carry out a transaction
        :type private_transaction:
        :return:
        :rtype:
        """
        xml = '<?xml version="1.0" encoding="UTF-8" ?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>" + self.username + "</APIUsername>"
        xml += "<APIPassword>" + self.password + "</APIPassword>"
        xml += "<Method>actransactioncheckstatus</Method>"
        if transaction_reference is not None:
            xml += "<TransactionReference>" + transaction_reference + "</TransactionReference>"
        if private_transaction is not None:
            xml += "<PrivateTransactionReference>" + private_transaction + "</PrivateTransactionReference>"
        xml += "</Request>"
        xml += "</AutoCreate>"
        

        response = self.__get_xml_response(xml)
        return self.__parse_response(response)

    def ac_internal_transfer(self, currency_code, amount, beneficiary_account, beneficiary_email, narrative):
        """
        Transfer funds from your Payment Account to another Yo! Payments Account

        :param currency_code: MTN Mobile Money, MTN Airtime, Warid Airtime, Orange Airtime, Airtel Airtime
        :type currency_code: Uganda Shillings
        :param amount: The amount to be transferred
        :type amount: str
        :param beneficiary_account: Account number of Yo! Payments User
        :type beneficiary_account:
        :param beneficiary_email: Email Address of the recipient of funds
        :type beneficiary_email:
        :param narrative: Textual narrative about the transaction
        :type narrative:
        """
        xml = '<?xml version="1.0" encoding="UTF-8" ?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>" + self.username + "</APIUsername>"
        xml += "<APIPassword>" + self.password + "</APIPassword>"
        xml += "<Method>acinternaltransfer</Method>"
        xml += "<CurrencyCode>" + currency_code + "</CurrencyCode>"
        xml += "<Amount>" + amount + "</Amount>"
        xml += "<BeneficiaryAccount>" + beneficiary_account + "</BeneficiaryAccount>"
        xml += "<BeneficiaryEmail>" + beneficiary_email + "</BeneficiaryEmail>"
        xml += "<Narrative>" + narrative + "</Narrative>"

        if self.internal_reference is not None:
            xml += "<InternalReference>" + self.internal_reference + "</InternalReference>"

        if self.external_reference is not None:
            xml += "<ExternalReference>" + self.external_reference + "</ExternalReference>"
        xml += "</Request>"
        xml += "</AutoCreate>"

        response = self.__get_xml_response(xml)
        return self.__parse_response(response)

    def ac_withdraw_funds(self, msisdn, amount, narrative,
    nonce=None,signature=None):
        """
        Withdraw funds from your YO! Payments Account to a mobile money user
        This transaction transfers funds from your YO! Payments Account to a mobile money user.
        Please handle this request with care because if compromised, it can lead to
        withdrawal of funds from your account.
        This request is not supported by all mobile money operator networks
        This request requires permission that is granted by the issuance of an API Access Letter

        :param msisdn: The mobile money phone number in the format 256772123456
        :type msisdn: str
        :param amount: The amount of money to withdraw from your account (floats are supported)
        :type amount: str
        :param narrative: The reason for withdrawal of funds from your account
        :type narrative: str
        :param nonce: This is the public key authentication nonce which is only
        specified if public key authentication is turned on your account.
        :type nonce:str
        :param signature : This is the public key authentication signature in Base64 and also
	    mandatory only if public key authentication is turned on your account.
        :type signature: str
        """
        xml = '<?xml version="1.0" encoding="UTF-8" ?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>" + self.username + "</APIUsername>"
        xml += "<APIPassword>" + self.password + "</APIPassword>"
        xml += "<Method>acwithdrawfunds</Method>"
        xml += "<NonBlocking>TRUE</NonBlocking>"
        xml += "<Account>" + msisdn + "</Account>"
        xml += "<Amount>" + amount + "</Amount>"
        xml += "<Narrative>" + narrative + "</Narrative>"

        if self.internal_reference is not None:
            xml += "<InternalReference>" + self.internal_reference + "</InternalReference>"

        if self.external_reference is not None:
            xml += "<ExternalReference>" + self.external_reference + "</ExternalReference>"

        if self.provider_reference_text is not None:
            xml += "<ProviderReferenceText>" + self.provider_reference_text + "</ProviderReferenceText>"
        if nonce is not None:
            xml += "<PublicKeyAuthenticationNonce>"+nonce+"</PublicKeyAuthenticationNonce>"
        if signature is not None:
            xml += "<PublicKeyAuthenticationSignatureBase64>"+signature+"</PublicKeyAuthenticationSignatureBase64>"
        xml += "</Request>"
        xml += "</AutoCreate>"

        response = self.__get_xml_response(xml)
        return self.__parse_response(response)

    def ac_acct_balance(self):
        """
        Get the current balance of your Yo! Payments Account
        Returned array contains an array of balances (including airtime)
        """
        xml = '<?xml version="1.0" encoding="UTF-8" ?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>" + self.username + "</APIUsername>"
        xml += "<APIPassword>" + self.password + "</APIPassword>"
        xml += "<Method>acacctbalance</Method>"
        xml += "</Request>"
        xml += "</AutoCreate>"

        response = self.__get_xml_response(xml)
        return self.__parse_response(response)

    def __get_xml_response(self, xml):
        """

        :param xml:
        :type xml:
        :return:
        :rtype:
        """
        headers = {"Content-type": "text/xml", "Content-transfer-encoding": "text"}
        conn = requests.post(self.url, data=xml, headers=headers)
        return conn.text

    def __get_text(self, nodelist):
        """

        :param nodelist:
        :type nodelist:
        :return:
        :rtype:
        """
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def __parse_response(self, response):
        try:
            return xmltodict.parse(response)["AutoCreate"]["Response"]
        except KeyError:
            return xmltodict.parse(response)

    
    #Generate RSA Signature
    def generate_public_key_signature(self,data):
        with open(self.private_key_file, 'rb') as p:
            file_content=p.read()
            p.close()
            private_key=crypto.load_privatekey(crypto.FILETYPE_PEM, file_content)
            if not private_key:
                raise ValueError("You must specify the private key file")
            message=data.encode('UTF-8')
            signature=crypto.sign(private_key,hashlib.sha1(message).hexdigest(),'sha1WithRSAEncryption')
            """
            * Decoding to UTF-8 removes the prepend and appended b'...' string
            * from base64 encoded signature.
            """
            base64_signature=base64.b64encode(signature).decode("UTF-8")
        return str(base64_signature)

    #Send Mobile Airtime
    def ac_send_airtime_mobile(self,msisdn, amount, narrative):
        xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>"+ self.username +"</APIUsername>"
        xml += "<APIPassword>"+ self.password +"</APIPassword>"
        xml += "<Method>acsendairtimemobile</Method>"
        xml += "<NonBlocking>TRUE</NonBlocking>"
        xml += "<Account>"+ msisdn +"</Account>"
        xml += "<Amount>"+ amount +"</Amount>"
        xml += "<Narrative>"+narrative+"</Narrative>"
        if self.external_reference is not None:
           xml += "<ExternalReference>"+ self.external_reference +"</ExternalReference>" 
        if self.internal_reference is not None:
           xml += "<InternalReference>"+ self.internal_reference +"</InternalReference>" 
        if self.provider_reference_text is not None:
           xml += "<ProviderReferenceText>"+ self.provider_reference_text +"</ProviderReferenceText>"
        xml += '</Request>'
        xml += '</AutoCreate>'
        response = self.__get_xml_response(xml)
        return self.__parse_response(response)
    
    #get ministatement 
    def ac_get_ministatement(
        self,
        start_date=None,
        end_date=None, 
        transaction_status=None,
        currency_code=None, 
        result_set_limit=None, 
        transaction_entry_designation=None,
        external_reference=None):
        """
        getMiniStatement gets a list of transactions which were carried out on 
        your account during a certain period of time .
        :param string startDate: This is the date and time for which
        the transaction should be queried. If specified, format: YYYY-MM-DD HM:MM:SS.
        :param string endDate: This is the date and time for which
        the transaction should be queried. If specified, format: YYYY-MM-DD HM:MM:SS.
        :param string transactionStatus: . If specified, the only valid values are: 
        FAILED, PENDING, SUCCEEDED and INDETERMINATE.
        :param string currencyCode: Currency code for the transaction.
        :param string resultSetLimit:Specifies the maximum number of results that
        should be allowed. By default, the maximum is 15.
        :param transactionEntryDesignation:This parameter can take any of three possible 
        values; TRANSACTION, CHARGES,ANY.
        :param externalReference:ExternalReference parameter that you provided with 
        your withdraw or deposit request.
        :Return the statement
        """
        xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>" + self.username + "</APIUsername>"
        xml += "<APIPassword>" + self.password + "</APIPassword>"
        xml += "<Method>acgetministatement</Method>"
        if start_date is not None:
            xml += "<StartDate>"+ start_date + "</StartDate>"
        if end_date is not None:
            xml += "<EndDate>"+ end_date + "</EndDate>"
        if transaction_status is not None:
            xml += "<TransactionStatus>"+ transaction_status + "</TransactionStatus>"
        if currency_code is not None:
            xml += "<CurrencyCode>"+ currency_code + "</CurrencyCode>"
        if result_set_limit is not None:
            xml += "<ResultSetLimit>"+ result_set_limit + "</ResultSetLimit>"
        if transaction_entry_designation is not None:
            xml += "<TransactionEntryDesignation>"+ transaction_entry_designation + "</TransactionEntryDesignation>"
        if external_reference is not None:
            xml += "<ExternalReference>"+ external_reference + "</ExternalReference>"
        xml += "</Request>"
        xml += "</AutoCreate>"
        response = self.__get_xml_response(xml)
        return self.__parse_response(response)

    #Receive payment Notification
    # def receive_payment_notification(self):
    #     verification_status=False
    #     if self.verify_payment_notification():
    #         verification_status=True 
    #     return {    "is_verified" :verification_status,
    #                 "date_time" : request.POST['date_time'],
    #                 "amount" : request.POST['amount'],
    #                 "narrative" : request.POST['narrative'],
    #                 "network_ref" : request.POST['network_ref'],
    #                 "external_ref" : request.POST['external_ref'],
    #                 "msisdn" : request.POST['msisdn']
    #             }
    #verify IPN signature
    def verify_payment_notification(self,data, base64_signature):
        #print(base64_signature)
        with open(self.public_key_file,'rb') as pub:
            file_content=pub.read()
            pub.close()
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, file_content)
            if not cert:
                raise ValueError("You must specify the public key file")
            decoded_signature = base64.b64decode(base64_signature)
            try:
                crypto.verify(cert, decoded_signature, data, "sha1")
                return "Signature Verification passed"
            except Exception as ex:
                raise crypto.Error(
                    f"Error occurred during signature validation: {ex}"
                )
                return "Signature Verification Failed" 
            #try:
            
            #verified = crypto.verify(pubKeyObject, decoded_signature, sha1_str, 'sha1')
            #return True
            # except crypto.Error:
            #     return False
                
            # if(verify) is None:
            #     print("Sucessful")
            # else:
            #     print("failed")
            #print(verified)
        #return verified

    def create_bulky_payments(self,name,description,notification_text,
        private_bulk_payment_request_id,beneficiaries,
        schedule_payment=None,nonce=None,signature=None):
        #print(beneficiaries['Amount'])
        """
        create_bulky_payments takes transaction input fields to enable 
        making multiple payments at a time.
        :param name: This is a short name that describes the bulk payment,
        E.g Salary payments
        :type name: str
        :param string description: This is a detailed description of a bulk payment.
        :param string notification_text: This is a brief description of a bulk payment.
        :param datetime schedule_payment: This is used suppose there is a period in which
        the bulk payment should run. If specified, format: YYYY-MM-DD HM:MM:SS.
        :param string private_bulk_payment_request_id: textual string that uniquely
        dentifies the bulk payment.
        :param String nonce: This is the public key authentication nonce which is only
        specified if public key authentication is turned on your account.
        It must be unique for all transactions whether succeeded or not.
        :param string signature: This is the public key authentication signatuture in Base64 and also
        mandatory only if public key authentication is turned on your account.
        :param beneficiaries:This is an array that takes in various beneficiaries.
        The array key names used should be the same as defined below. It consists
        of;
        :Amount: This is the amount to be sent to the beneficiary.
        :AccountNumber: This is a numerical value representing the account number of the 
        mobile money account where you wish to transfer the funds to.
        :Name: This is the name of the beneficiary. You may provide all names, some of the names or none.
        :AccountType: Set this to the type of account the funds are going to be transferred to.
        If it you are transferring to a mobile money subscriber, then it should MOBILE MONEY.
        If you are transferring funds to an internal YBS account, set this to "YO PAYMENTS"
        :EmailAddress: This is the email address of the beneficiary and its optional.
        :PaymentNotificationText: Provide a very brief text to describe this payment.
        Note that you only need to set this if you want to override the 
        :GroupwidePaymentNotificationText only for this beneficiary so that their payment 
        notification text is different. Inotherwords, this field is optional.

        Returns : YoPaymentsResponse object of a created bulk payments. 
        """
        xml='<?xml version="1.0" encoding="UTF-8"?>'
        xml +="<AutoCreate>"
        xml +="<Request>"
        xml +="<APIUsername>" + self.username + "</APIUsername>"
        xml +="<APIPassword>" + self.password + "</APIPassword>"
        xml +="<Method>accreatebulkpayment</Method>"
        xml +="<Name>" + name + "</Name>"
        xml +="<Description>" + description + "</Description>"
        xml +="<GroupwidePaymentNotificationText>" + notification_text+"</GroupwidePaymentNotificationText>"

        if schedule_payment is not None:
            xml +="<SchedulePayment>" + schedule_payment + "</SchedulePayment>"
        xml +="<PrivateBulkPaymentRequestId>" + private_bulk_payment_request_id+"</PrivateBulkPaymentRequestId>"
        if nonce is not None:
            xml +="<PublicKeyAuthenticationNonce>" + nonce+ "</PublicKeyAuthenticationNonce>"

        if signature is not None:
            xml +="<PublicKeyAuthenticationSignatureBase64>" + signature + "</PublicKeyAuthenticationSignatureBase64>"

        xml +="<Beneficiaries>"
        for  values in beneficiaries:
            xml +="<Beneficiary>"
            if "Amount" in values.keys():
                xml +="<Amount>" + values['Amount'] + "</Amount>"

            if "AccountNumber" in values.keys():
                xml +="<AccountNumber>" + values['AccountNumber'] + "</AccountNumber>"

            if "Name" in values.keys():
                xml +="<Name>" + values['Name'] + "</Name>"

            if "AccountType" in values.keys():
                xml +="<AccountType>" + values['AccountType'] + "</AccountType>"

            if "EmailAddress" in values.keys():
                xml +="<EmailAddress>" + values['EmailAddress'] + "</EmailAddress>"

            if "PaymentNotificationText" in values.keys():
                xml +="<PaymentNotificationText>" + values['PaymentNotificationText'] + "</PaymentNotificationText>"

            xml +="</Beneficiary>"
        xml +="</Beneficiaries>"
        xml +="</Request>"
        xml +="</AutoCreate>"
        response = self.__get_xml_response(xml)
        return self.__parse_response(response)

    def check_bulk_payment_status(self,
		bulk_payment_request_identifier=None,
		private_bulk_payment_request_id=None):
        """
        The check_bulk_payment_status request enables you to get the status of a bulk payment
        that was previously created.
        :param bulk_payment_request_identifier :This uniquely identifies the bulk payment 
        that was created and returned from the gateway.Only option if private_bulk_payment_request_id is set
        :type bulk_payment_request_identifier:str
        :param private_bulk_payment_request_id: textual string generated from your 
        application when creating the bulk payment. Only optional if bulk_payment_request_identifier
        is set.
        type private_bulk_payment_request_id: str
        Returns : YoPaymentsResponse object. 
        """

        xml ='<?xml version="1.0" encoding="UTF-8"?>'
        xml +="<AutoCreate>"
        xml +="<Request>"
        xml +="<APIUsername>"+ self.username +"</APIUsername>"
        xml +="<APIPassword>"+ self.password +"</APIPassword>"
        xml +="<Method>accheckbulkpaymentstatus</Method>"
        if bulk_payment_request_identifier is not None:
            xml +="<BulkPaymentRequestIdentifier>"+ bulk_payment_request_identifier +"</BulkPaymentRequestIdentifier>"
        
        if private_bulk_payment_request_id is not None:
            xml +="<PrivateBulkPaymentRequestId>"+ private_bulk_payment_request_id +"</PrivateBulkPaymentRequestId>"
        
        xml +="</Request>"
        xml +="</AutoCreate>"

        response = self.__get_xml_response(xml)
        return self.__parse_response(response)

    def pause_bulk_payment(self,bulk_payment_request_identifier,
	    pause_reason):

        """
        pause_bulk_payment takes in parameters used to pause a running bulk payment.
        :param bulk_payment_request_identifier: This uniquely identifies
        the bulk payment that was created and returned from the gateway
        :type bulk_payment_equest_identifier :str
        :param string pause_reason: This the reason why the bulk payment is being paused.
        :type pause_reason: str
        :Returns : YoPaymentsReseponse object. 
        """
        xml ='<?xml version="1.0" encoding="UTF-8"?>'
        xml +="<AutoCreate>"
        xml +="<Request>"
        xml +="<APIUsername>" + self.username + "</APIUsername>"
        xml +="<APIPassword>" + self.password + "</APIPassword>"
        xml +="<Method>acpausebulkpayment</Method>"
        xml +="<BulkPaymentRequestIdentifier>"+ bulk_payment_request_identifier +"</BulkPaymentRequestIdentifier>"
        xml +="<PauseReason>" + pause_reason +"</PauseReason>"
        xml +="</Request>"
        xml +="</AutoCreate>"
        
        response = self.__get_xml_response(xml)
        return self.__parse_response(response)
    
    def resume_bulk_payment(self,bulk_payment_request_identifier):
        """
        resume_bulk_payment takes in one parameter used to resume a previously 
        paused bulk payment.
        :param bulk_payment_request_identifier: This uniquely identifies
        the bulk payment that was created and returned from the gateway
        type bulk_payment_request_identifier :str
        :Returns : YoPaymentsReseponse object. 
        """
        xml='<?xml version="1.0" encoding="UTF-8"?>'
        xml +="<AutoCreate>"
        xml +="<Request>"
        xml +="<APIUsername>"+ self.username +"</APIUsername>"
        xml +="<APIPassword>"+ self.password +"</APIPassword>"
        xml +="<Method>acresumebulkpayment</Method>"
        xml +="<BulkPaymentRequestIdentifier>"+ bulk_payment_request_identifier +"</BulkPaymentRequestIdentifier>"
        xml +="</Request>"
        xml +="</AutoCreate>"

        response = self.__get_xml_response(xml)
        return self.__parse_response(response)


	
    def cancel_bulk_payment(self,bulk_payment_request_identifier):
        """
        cancel_bulk_payment takes in one parameter used to cancel a running 
        bulk payment.
        :param bulk_payment_request_identifier: This uniquely identifies
        the bulk payment that was created and returned from the gateway
        type b: strulk_payment_request_identifier: str
        :Returns : YoPaymentsReseponse object. 
        """
        xml='<?xml version="1.0" encoding="UTF-8"?>'
        xml +="<AutoCreate>"
        xml +="<Request>"
        xml +="<APIUsername>"+ self.username +"</APIUsername>"
        xml +="<APIPassword>"+ self.password +"</APIPassword>"
        xml +="<Method>accancelbulkpayment</Method>"
        xml +="<BulkPaymentRequestIdentifier>"+ bulk_payment_request_identifier +"</BulkPaymentRequestIdentifier>"
        xml +="</Request>"
        xml +="</AutoCreate>"

        response = self.__get_xml_response(xml)
        return self.__parse_response(response)

    def generate_random(self):
        # initializing size of string
        N = 4
        
        # using random.choices()
        # generating random strings
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        return res
    
    def ac_withdraw_funds_to_bank(self, amount,currency_code, bank_account_name,bank_account_number,
                          bank_account_identifier,transfer_type=None,transaction_reference=None,
                          nonce=None,signature=None):
        """
        Withdraw funds from your YO! Payments Account to a bank account

        :param amount: The amount of money to withdraw from your account (floats are supported)
        :type amount: str
        :param currency_code: UGX
        :type currency_code: str
        :param bank_account_name: This is the name of the bank account to which
        funds are being transferred. It should be as it is in the system.
        :type bank_account_name: str
        :param bank_account_number: This is the  account number to which
        funds are being transferred. It should be as it is in the system.
        :type bank_account_number: str
        :param bank_account_identifier: It should be as it is in the system.
        :type bank_account_identifier: str
        :param transfer_type: Can either be RTGS, EFT, TT
        :type transfer_type: str
        :param transaction_reference: This is he transaction reference to
        associate with bank withdraw transaction. Can later on be used to 
        check status of the bank transfer
        :type transaction_reference: str
        :param nonce: This is the public key authentication nonce which is only
        specified if public key authentication is turned on your account.
        :type nonce:str
        :param signature : This is the public key authentication signature in Base64 and also
	    mandatory only if public key authentication is turned on your account.
        :type signature: str
        """
        xml = '<?xml version="1.0" encoding="UTF-8" ?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>" + self.username + "</APIUsername>"
        xml += "<APIPassword>" + self.password + "</APIPassword>"
        xml += "<Method>acwithdrawfundstobank</Method>"
        xml += "<Amount>" + amount + "</Amount>"
        xml +="<CurrencyCode>"+currency_code+"</CurrencyCode>"
        xml +="<BankAccountName>"+bank_account_name+"</BankAccountName>"
        xml +="<BankAccountNumber>"+bank_account_number+"</BankAccountNumber>"
        xml +="<BankAccountIdentifier>"+bank_account_identifier+"</BankAccountIdentifier>"
        if transfer_type is not None:
            xml += "<TransferTransactionType>" + transfer_type + "</TransferTransactionType>"

        
        if transaction_reference is not None:
            xml += "<PrivateTransactionReference>" + transaction_reference + "</PrivateTransactionReference>"
        if nonce is not None:
            xml += "<PublicKeyAuthenticationNonce>"+nonce+"</PublicKeyAuthenticationNonce>"
        if signature is not None:
            xml += "<PublicKeyAuthenticationSignatureBase64>"+signature+"</PublicKeyAuthenticationSignatureBase64>"
        xml += "</Request>"
        xml += "</AutoCreate>"

        response = self.__get_xml_response(xml)
        return self.__parse_response(response)
        
    




		
	
