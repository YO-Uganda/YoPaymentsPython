import requests
import xmltodict


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

    # The Yo Payments API URL
    # Required:
    # Default: "https://paymentsapi1.yo.co.ug/ybs/task.php"
    # Options:
    # * "https://paymentsapi1.yo.co.ug/ybs/task.php",
    # * "https://paymentsapi2.yo.co.ug/ybs/task.php",
    # * "https://41.220.12.206/services/yopaymentsdev/task.php" For Sandbox tests

    url = "https://paymentsapi1.yo.co.ug/ybs/task.php"

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
            xml += '<InstantNotificationUrl>' + self.instant_payment_notification_url + '</InstantNotificationUrl>'
        if self.instant_failure_notification_url is not None:
            xml += '<FailureNotificationUrl>' + self.instant_failure_notification_url + '</FailureNotificationUrl>'
        if self.authentication_signature_base64:
            xml += '<AuthenticationSignatureBase64>' + self.authentication_signature_base64 + '</AuthenticationSignatureBase64>'
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

    def ac_withdraw_funds(self, msisdn, amount, narrative):
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
        """
        xml = '<?xml version="1.0" encoding="UTF-8" ?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>" + self.username + "</APIUsername>"
        xml += "<APIPassword>" + self.password + "</APIPassword>"
        xml += "<Method>acwithdrawfunds</Method>"
        xml += "<NonBlocking>" + self.nonBlocking + "</NonBlocking>"
        xml += "<Account>" + msisdn + "</Account>"
        xml += "<Amount>" + amount + "</Amount>"
        xml += "<Narrative>" + narrative + "</Narrative>"

        if self.internal_reference is not None:
            xml += "<InternalReference>" + self.internal_reference + "</InternalReference>"

        if self.external_reference is not None:
            xml += "<ExternalReference>" + self.external_reference + "</ExternalReference>"

        if self.provider_reference_text is not None:
            xml += '<ProviderReferenceText>' + self.provider_reference_text + '</ProviderReferenceText>'
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
