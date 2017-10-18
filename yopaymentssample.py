import requests
import uuid
import random
import string
from xml.dom.minidom import parse, parseString

api_url = "https://paymentsapi1.yo.co.ug/ybs/task.php"
api_username = "yo_api_username"
api_password = "yo_api_password"


# Function subm_request makes an HTTP request to Yo! Payments
def submit_request(xml):
    global api_url
    headers = {"Content-type": "text/xml"}
    conn = requests.post(api_url, xml, headers)
    return conn.text


# Function generate_deposit_Xml generates required XML for acdepositfunds request
def generate_deposit_xml(amount, msisdn, narrative, external_ref):
    global api_username, api_password
    xml = "<?xml version='1.0' encoding='UTF-8' ?>"
    xml += "<AutoCreate>"
    xml += "<Request>"
    xml += "<APIUsername>" + api_username + "</APIUsername>"
    xml += "<APIPassword>" + api_password + "</APIPassword>"
    xml += "<Method>acdepositfunds</Method>"
    xml += "<NonBlocking>TRUE</NonBlocking>"
    xml += "<Amount>" + amount + "</Amount>"
    xml += "<Account>" + msisdn + "</Account>"
    xml += "<Narrative>" + narrative + "</Narrative>"
    xml += "<ExternalReference>" + external_ref + "</ExternalReference>"
    xml += "</Request>"
    xml += "</AutoCreate>"
    return xml


# randomword generates random string
def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_text(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


# Calling generate_deposit_xml to generate XML
xml = generate_deposit_xml("1000", "256783086794", "Testing...", randomword(8))
response = submit_request(xml)
result = parseString(response)

# Now extract fields
statusCode = get_text(result.getElementsByTagName("StatusCode")[0].childNodes)
status = get_text(result.getElementsByTagName("Status")[0].childNodes)

statusMessage = ""
if len(result.getElementsByTagName("StatusMessage")) > 0:
    statusMessage = get_text(result.getElementsByTagName("StatusMessage")[0].childNodes)

errorMessage = ""
if len(result.getElementsByTagName("ErrorMessage")) > 0:
    errorMessage = get_text(result.getElementsByTagName("ErrorMessage")[0].childNodes)

transaction_ref = ""
if len(result.getElementsByTagName("TransactionReference")) > 0:
    transaction_ref = get_text(result.getElementsByTagName("TransactionReference")[0].childNodes)

transaction_status = ""
if len(result.getElementsByTagName("TransactionStatus")) > 0:
    transaction_status = get_text(result.getElementsByTagName("TransactionStatus")[0].childNodes)

# You can do something with these variables
print("Status: " + status)
print("Status Code: " + statusCode)
print("Status Message: " + statusMessage)
print("Error Message: " + errorMessage)
print("Transaction Reference: " + transaction_ref)
print("Transaction Status: " + transaction_status)

# Use the above example to implement for other API operations such as Check balance, Withdraws, Check status etc.
