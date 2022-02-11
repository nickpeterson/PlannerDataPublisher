import logging
from urllib import request

import azure.functions as func
import requests
import os
import datetime
from pytz import timezone
import json
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings


# Adding some code here


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    groupId = req.params.get('groupId')
    if not groupId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            groupId = req_body.get('groupId')

    tokenHeaders = {'Content-Type': 'application/x-www-form-urlencoded'}
    tokenBody = f"grant_type=password&resource=https://graph.microsoft.com&client_id={os.getenv('ClientId')}&username={os.getenv('FunctionalAccountEmail')}&password={os.getenv('FunctionalAccountPw')}&client_secret={os.getenv('ClientSecret')}"
    accessTokenRequest = requests.get(
        f"https://login.microsoftonline.com/{os.getenv('TenantId')}/oauth2/token", headers=tokenHeaders, data=tokenBody)
    accessTokenResponse = accessTokenRequest.json()
    token = accessTokenResponse['access_token']
    graphHeader = {'Authorization': f"Bearer {token}"}
    groupNameRequest = requests.get(
        f"https://graph.microsoft.com/v1.0/groups/{groupId}", headers=graphHeader)
    groupNameResponse = groupNameRequest.json()
    groupDisplayName = groupNameResponse['displayName']

    groupPlansRequest = requests.get(
        f"https://graph.microsoft.com/v1.0/groups/{groupId}/planner/plans", headers=graphHeader)
    groupPlansResponse = groupPlansRequest.json()
    for plan in groupPlansResponse['value']:

        planDisplayName = plan['title']
        plansTasksRequest = requests.get(
            f"https://graph.microsoft.com/v1.0/planner/plans/{plan['id']}/tasks", headers=graphHeader)
        fileText = json.loads(plansTasksRequest.text)
        writeFiletoADLS(fileText, groupDisplayName, planDisplayName)

    return func.HttpResponse(f"Hello, The Group {groupDisplayName}'s planner data has been added to ADLS ")


def writeFiletoADLS(jsonText, groupName, planName):
    storage_account_name = "luckdatalakedev"
    storage_account_key = "5TGE0TcKHT486KYamBXLRVEttwW6+S8RCtsYJWjTRsqEHLixy9T/AlMgcTmS5LauDf5DcTceDhUUZZZGORXfBQ=="

    try:
        global service_client

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)

    except Exception as e:
        print(e)

    file_system_client = service_client.get_file_system_client(
        file_system="planner-data")

    tz = timezone('EST')
    now = datetime.datetime.now(tz)
    dateOnly = now.strftime("%Y-%m-%d")
    directory = f"{groupName}/{dateOnly}/{planName}"
    filePath = f"{dateOnly}-{planName}.json"

    file_system_client.create_directory(directory)
    directory_client = file_system_client.get_directory_client(directory)
    file_client = directory_client.create_file(filePath)
    file_to_load = json.dumps(jsonText)
    file_client.append_data(data=file_to_load, offset=0, length=len(file_to_load))
    file_client.flush_data(len(file_to_load))

    


