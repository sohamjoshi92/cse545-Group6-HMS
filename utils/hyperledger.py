import requests
import json
import os

'''
Insurance_Statement
Transaction
Diagnosis
'''

headers = {
  'Content-Type': 'application/json'
}
baseUrl = os.environ.get('HYPERLEDGER_URL')
payload = { "username": os.environ.get('HYPERLEDGER_USER') }

def addUserToRequest(data):
  data["username"] = payload["username"]
  return data

def PushInsuranceClaimToHyperledger(data):
  response = requests.request("POST", "{0}/createClaimRequest".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(data)))
  return response.json()

def GetAllInsuranceClaimsFromHyperledger():
  response = requests.request("GET", "{0}/queryAllClaimRequest".format(baseUrl), headers=headers, data=json.dumps(payload))
  return response.json()

def GetInsuranceClaimFromHyperledger(id):
  data={ "id": id}
  response = requests.request("GET", "{0}/queryClaimRequest".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(data)))
  return response.json()

def PushTransactionToHyperledger(data):
  response = requests.request("POST", "{0}/createTransacton".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(data)))
  return response.json()

def GetAllTransactionsFromHyperledger():
  response = requests.request("GET", "{0}/queryAllTransactions".format(baseUrl), headers=headers, data=json.dumps(payload))
  return response.json()

def GetTransactionFromHyperledger(id):
  data={ "id": id}
  response = requests.request("GET", "{0}/queryTransaction".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(data)))
  return response.json()

def PushDiagnosisReportToHyperledger(data):
  response = requests.request("POST", "{0}/createDiagnosisReport".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(data)))
  return response.json()

def GetAllDiagnosisReportsFromHyperledger():
  response = requests.request("GET", "{0}/queryAllDiagnosisReports".format(baseUrl), headers=headers, data=json.dumps(payload))
  return response.json()

def GetDiagnosisReportFromHyperledger(id):
  data={ "id": id}
  response = requests.request("GET", "{0}/queryDiagnosisReport".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(data)))
  return response.json()