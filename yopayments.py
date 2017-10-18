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

    def set_nonblocking(self, nonBlocking):
        self.nonBlocking = nonBlocking

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

        Status = self.__get_text(result.getElementsByTagName("Status")[0].childNodes)
        StatusCode = self.__get_text(result.getElementsByTagName("StatusCode")[0].childNodes)

        StatusMessage = None
        if len(result.getElementsByTagName("StatusMessage")) > 0:
            StatusMessage = self.__get_text(result.getElementsByTagName("StatusMessage")[0].childNodes)

        TransactionStatus = None
        if len(result.getElementsByTagName("TransactionStatus")) > 0:
            TransactionStatus = self.__get_text(result.getElementsByTagName("TransactionStatus")[0].childNodes)

        ErrorMessageCode = None
        if len(result.getElementsByTagName("ErrorMessageCode")) > 0:
            ErrorMessageCode = self.__get_text(result.getElementsByTagName("ErrorMessageCode")[0].childNodes)

        ErrorMessage = None
        if len(result.getElementsByTagName("ErrorMessage")) > 0:
            ErrorMessage = self.__get_text(result.getElementsByTagName("ErrorMessage")[0].childNodes)

        TransactionReference = None
        if len(result.getElementsByTagName("TransactionReference")) > 0:
            TransactionReference = self.__get_text(result.getElementsByTagName("TransactionReference")[0].childNodes)

        MNOTransactionReferenceId = None
        if len(result.getElementsByTagName("MNOTransactionReferenceId")) > 0:
            MNOTransactionReferenceId = self.__get_text(result.getElementsByTagName("MNOTransactionReferenceId")[0].childNodes)

        IssuedReceiptNumber = None
        if len(result.getElementsByTagName("IssuedReceiptNumber")) > 0:
            IssuedReceiptNumber = self.__get_text(result.getElementsByTagName("IssuedReceiptNumber")[0].childNodes)

        response_object = {
            "Status": Status,
            "StatusCode": StatusCode,
            "StatusMessage": StatusMessage,
            "ErrorMessage": ErrorMessage,
            "ErrorMessageCode": ErrorMessageCode,
            "TransactionReference": TransactionReference,
            "TransactionStatus": TransactionStatus,
            "MNOTransactionReferenceId": MNOTransactionReferenceId,
            "IssuedReceiptNumber": IssuedReceiptNumber
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

        Status = self.__get_text(result.getElementsByTagName("Status")[0].childNodes)
        StatusCode = self.__get_text(result.getElementsByTagName("StatusCode")[0].childNodes)

        StatusMessage = None
        if len(result.getElementsByTagName("StatusMessage")) > 0:
            StatusMessage = self.__get_text(result.getElementsByTagName("StatusMessage")[0].childNodes)

        TransactionStatus = None
        if len(result.getElementsByTagName("TransactionStatus")) > 0:
            TransactionStatus = self.__get_text(result.getElementsByTagName("TransactionStatus")[0].childNodes)

        ErrorMessageCode = None
        if len(result.getElementsByTagName("ErrorMessageCode")) > 0:
            ErrorMessageCode = self.__get_text(result.getElementsByTagName("ErrorMessageCode")[0].childNodes)

        ErrorMessage = None
        if len(result.getElementsByTagName("ErrorMessage")) > 0:
            ErrorMessage = self.__get_text(result.getElementsByTagName("ErrorMessage")[0].childNodes)

        TransactionReference = None
        if len(result.getElementsByTagName("TransactionReference")) > 0:
            TransactionReference = self.__get_text(result.getElementsByTagName("TransactionReference")[0].childNodes)

        MNOTransactionReferenceId = None
        if len(result.getElementsByTagName("MNOTransactionReferenceId")) > 0:
            MNOTransactionReferenceId = self.__get_text(
                result.getElementsByTagName("MNOTransactionReferenceId")[0].childNodes)

        IssuedReceiptNumber = None
        if len(result.getElementsByTagName("IssuedReceiptNumber")) > 0:
            IssuedReceiptNumber = self.__get_text(result.getElementsByTagName("IssuedReceiptNumber")[0].childNodes)

        response_object = {
            "Status": Status,
            "StatusCode": StatusCode,
            "StatusMessage": StatusMessage,
            "ErrorMessage": ErrorMessage,
            "ErrorMessageCode": ErrorMessageCode,
            "TransactionReference": TransactionReference,
            "TransactionStatus": TransactionStatus,
            "MNOTransactionReferenceId": MNOTransactionReferenceId,
            "IssuedReceiptNumber": IssuedReceiptNumber
        }

        return response_object


    def __get_xml_response(self, xml):
        headers = {"Content-type": "text/xml","Content-transfer-encoding": "text"}
        conn = requests.post(self.url, data=xml, headers=headers)
        return conn.text

    def __get_text(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)