import requests
from xml.dom.minidom import parseString


class YoPay:
    external_reference = None
    internal_reference = None
    instant_payment_notification_url = None
    instant_failure_notification_url = None
    nonBlocking = False
    url = url = "https://paymentsapi1.yo.co.ug/ybs/task.php"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def set_non_blocking(self, non_blocking):
        self.nonBlocking = non_blocking

    def set_url(self, url):
        self.url = url

    def set_external_reference(self, external_reference):
        self.external_reference = external_reference

    def set_internal_reference(self, internal_reference):
        self.internal_reference = internal_reference

    def set_instant_payment_notification_url(self, instant_payment_notification_url):
        self.instant_payment_notification_url = instant_payment_notification_url

    def set_instant_failure_notification_url(self, instant_failure_notification_url):
        self.instant_failure_notification_url = instant_failure_notification_url

    def ac_deposit_funds(self, msisdn, amount, narrative):
        xml = '<?xml version="1.0" encoding="UTF-8" ?>'
        xml += "<AutoCreate>"
        xml += "<Request>"
        xml += "<APIUsername>" + self.username + "</APIUsername>"
        xml += "<APIPassword>" + self.password + "</APIPassword>"
        xml += "<Method>acdepositfunds</Method>"
        if self.nonBlocking:
            xml += "<NonBlocking>TRUE</NonBlocking>"
        else:
            xml += "<NonBlocking>FALSE</NonBlocking>"
        xml += "<Amount>" + str(amount) + "</Amount>"
        xml += "<Account>" + msisdn + "</Account>"
        xml += "<Narrative>" + narrative + "</Narrative>"
        if self.external_reference is not None:
            xml += "<ExternalReference>" + self.external_reference + "</ExternalReference>"
        xml += "</Request>"
        xml += "</AutoCreate>"

        response = self.__get_xml_response(xml)
        result = parseString(response)

        status = self.__get_text(result.getElementsByTagName("Status")[0].childNodes)
        status_code = self.__get_text(result.getElementsByTagName("StatusCode")[0].childNodes)

        status_message = None
        if len(result.getElementsByTagName("StatusMessage")) > 0:
            status_message = self.__get_text(result.getElementsByTagName("StatusMessage")[0].childNodes)

        transaction_status = None
        if len(result.getElementsByTagName("TransactionStatus")) > 0:
            transaction_status = self.__get_text(result.getElementsByTagName("TransactionStatus")[0].childNodes)

        error_message_code = None
        if len(result.getElementsByTagName("ErrorMessageCode")) > 0:
            error_message_code = self.__get_text(result.getElementsByTagName("ErrorMessageCode")[0].childNodes)

        error_message = None
        if len(result.getElementsByTagName("ErrorMessage")) > 0:
            error_message = self.__get_text(result.getElementsByTagName("ErrorMessage")[0].childNodes)

        transaction_reference = None
        if len(result.getElementsByTagName("TransactionReference")) > 0:
            transaction_reference = self.__get_text(result.getElementsByTagName("TransactionReference")[0].childNodes)

        mnotransaction_reference_id = None
        if len(result.getElementsByTagName("MNOTransactionReferenceId")) > 0:
            mnotransaction_reference_id = self.__get_text(
                result.getElementsByTagName("MNOTransactionReferenceId")[0].childNodes)

        issued_receipt_number = None
        if len(result.getElementsByTagName("IssuedReceiptNumber")) > 0:
            issued_receipt_number = self.__get_text(result.getElementsByTagName("IssuedReceiptNumber")[0].childNodes)

        response_object = {
            "Status": status,
            "StatusCode": status_code,
            "StatusMessage": status_message,
            "ErrorMessage": error_message,
            "ErrorMessageCode": error_message_code,
            "TransactionReference": transaction_reference,
            "TransactionStatus": transaction_status,
            "MNOTransactionReferenceId": mnotransaction_reference_id,
            "IssuedReceiptNumber": issued_receipt_number
        }

        return response_object

    def ac_transaction_check_status(self, transaction_reference, private_transaction=None):
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
        result = parseString(response)

        error_message_code = None
        if len(result.getElementsByTagName("ErrorMessageCode")) > 0:
            error_message_code = self.__get_text(
                result.getElementsByTagName("ErrorMessageCode")[0].childNodes)

        error_message = None
        if len(result.getElementsByTagName("ErrorMessage")) > 0:
            error_message = self.__get_text(result.getElementsByTagName("ErrorMessage")[0].childNodes)

        transaction_reference = None
        if len(result.getElementsByTagName("TransactionReference")) > 0:
            transaction_reference = self.__get_text(
                result.getElementsByTagName("TransactionReference")[0].childNodes)

        mnotransaction_reference_id = None
        if len(result.getElementsByTagName("MNOTransactionReferenceId")) > 0:
            mnotransaction_reference_id = self.__get_text(
                result.getElementsByTagName("MNOTransactionReferenceId")[0].childNodes)

        amount = None
        if len(result.getElementsByTagName("Amount")) > 0:
            amount = self.__get_text(result.getElementsByTagName("Amount")[0].childNodes)

        amount_formatted = None
        if len(result.getElementsByTagName("AmountFormatted")) > 0:
            amount_formatted = self.__get_text(result.getElementsByTagName("AmountFormatted")[0].childNodes)

        currency_code = None
        if len(result.getElementsByTagName("CurrencyCode")) > 0:
            currency_code = self.__get_text(result.getElementsByTagName("CurrencyCode")[0].childNodes)

        transaction_init_date = None
        if len(result.getElementsByTagName("TransactionInitialDate")) > 0:
            transaction_init_date = self.__get_text(result.getElementsByTagName("TransactionInitialDate")[0].childNodes)

        transaction_comp_date = None
        if len(result.getElementsByTagName("TransactionCompletionDate")) > 0:
            transaction_comp_date = self.__get_text(
                result.getElementsByTagName("TransactionCompletionDate")[0].childNodes)

        issued_receipt_number = None
        if len(result.getElementsByTagName("IssuedReceiptNumber")) > 0:
            issued_receipt_number = self.__get_text(result.getElementsByTagName("IssuedReceiptNumber")[0].childNodes)

        response_object = {
            "ErrorMessageCode": error_message_code,
            "ErrorMessage": error_message,
            "TransactionReference": transaction_reference,
            "MNOTransactionReferenceId": mnotransaction_reference_id,
            "Amount": amount,
            "AmountFormatted": amount_formatted,
            "CurrencyCode": currency_code,
            "TransactionInitialDate": transaction_init_date,
            "TransactionCompletionDate": transaction_comp_date,
            "IssuedReceiptNumber": issued_receipt_number
        }

        return response_object

    def __get_xml_response(self, xml):
        headers = {"Content-type": "text/xml", "Content-transfer-encoding": "text"}
        conn = requests.post(self.url, data=xml, headers=headers)
        return conn.text

    def __get_text(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
