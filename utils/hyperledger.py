import requests
import json
import os
import concurrent.futures
import logging

logger = logging.getLogger(__name__)

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
  req = {
      "id": data.id,
      "patient_first_name": data.patient_first_name,
      "patient_last_name": data.patient_last_name,
      "patient_email": data.patient_email,
      "patient_visible": data.patient_visible,
      "policy_name": data.policy_name,
      "policy_discount": str(data.policy_discount),
      "approved": data.approved,
      "requested": data.requested,
      "date": str(data.date),
  }
  response = requests.request("POST", "{0}/createClaimRequest".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(req)))
  response = response.json()
  if response["result"]:
    logger.info("Insurance Claim {} has been pushed to hyperledger".format(req["id"]))
  elif response["error"]:
    logger.info("Error pushing Insurance Claim to hyperledger - {}".format(response["error"]))

def GetAllInsuranceClaimsFromHyperledger():
  response = requests.request("GET", "{0}/queryAllClaimRequest".format(baseUrl), headers=headers, data=json.dumps(payload))
  response = response.json()
  if response["result"]:
    logger.info("Insurance Claims fetched from hyperledger")
  elif response["error"]:
    logger.info("Error fetching Insurance Claims from hyperledger - {}".format(response["error"]))
  return response

def GetInsuranceClaimFromHyperledger(id):
  data={ "id": id}
  response = requests.request("GET", "{0}/queryClaimRequest".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(data)))
  return response.json()

def PushTransactionToHyperledger(data):
  req = {
    "id": data.id,
    "patient_first_name": data.patient_first_name,
    "patient_last_name": data.patient_last_name,
    "patient_email": data.patient_email,
    "case_number": data.case_number,
    "amount": str(data.amount),
    "status": data.status
  }
  response = requests.request("POST", "{0}/createTransacton".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(req)))
  response = response.json()
  if response["result"]:
    logger.info("Transaction {} has been pushed to hyperledger".format(req["id"]))
  elif response["error"]:
    logger.info("Error pushing transaction to hyperledger - {}".format(response["error"]))

def GetAllTransactionsFromHyperledger():
  response = requests.request("GET", "{0}/queryAllTransactions".format(baseUrl), headers=headers, data=json.dumps(payload))
  response = response.json()
  if response["result"]:
    logger.info("Transactions fetched from hyperledger")
  elif response["error"]:
    logger.info("Error fetching Transactions from hyperledger - {}".format(response["error"]))
  return response

def GetTransactionFromHyperledger(id):
  data={ "id": id}
  response = requests.request("GET", "{0}/queryTransaction".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(data)))
  return response.json()

def PushDiagnosisReportToHyperledger(data):
  req = {
      "id": data.id,
      "patient_first_name": data.patient_first_name,
      "patient_last_name": data.patient_last_name,
      "birthdate": data.birthdate,
      "age": data.age,
      "gender": data.gender,
      "doctor_first_name": data.doctor_first_name,
      "doctor_last_name": data.doctor_last_name,
      "doctor_email_id": data.doctor_email_id,
      "patient_email_id": data.patient_email_id,
      "doctor_phone_number": data.doctor_phone_number,
      "diagnosis_comments": data.diagnosis_comments,
      "recommended_tests": data.recommended_tests,
      "approved": data.approved
  }
  response = requests.request("POST", "{0}/createDiagnosisReport".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(req)))
  response = response.json()
  if response["result"]:
    logger.info("Dianosis {} has been pushed to hyperledger".format(req["id"]))
  elif response["error"]:
    logger.info("Error pushing diagnosis to hyperledger - {}".format(response["error"]))

def GetAllDiagnosisReportsFromHyperledger():
  response = requests.request("GET", "{0}/queryAllDiagnosisReports".format(baseUrl), headers=headers, data=json.dumps(payload))
  response = response.json()
  if response["result"]:
    logger.info("Diagnosis Reports fetched from hyperledger")
  elif response["error"]:
    logger.info("Error fetching Diagnosis Reports from hyperledger - {}".format(response["error"]))
  return response

def GetDiagnosisReportFromHyperledger(id):
  data={ "id": id}
  response = requests.request("GET", "{0}/queryDiagnosisReport".format(baseUrl), headers=headers, data=json.dumps(addUserToRequest(data)))
  return response.json()

def GetAllHyperledgerTransactions():
  with concurrent.futures.ThreadPoolExecutor() as executor:
    reqs = [GetAllDiagnosisReportsFromHyperledger,GetAllInsuranceClaimsFromHyperledger,GetAllTransactionsFromHyperledger]
    res = [executor.submit(req) for req in reqs]
    concurrent.futures.wait(res)

    response = {}
    responseKeys = ["diagnosis","insurance_claim", "transactions"]

    for i in range(3):
      arr=[]
      for a in (res[i].result()["result"]):
        arr.append(a["Record"])
      response[responseKeys[i]] = arr

    return response
