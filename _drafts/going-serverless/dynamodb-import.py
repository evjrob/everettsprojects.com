# Derived from:
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.02.html

#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
# 
#  http://aws.amazon.com/apache2.0/
# 
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import tqdm


type_conversions = {
    'IncidentNumber': int,
    'IncidentType': str,
    'Latitude': decimal.Decimal,
    'Longitude': decimal.Decimal,
    'Location': str,
    'IncidentLSD': int,
    'IncidentSection': int,
    'IncidentTownship': int,
    'IncidentRange': int,
    'IncidentMeridian': int,
    'LicenceNumber': str,
    'LicenceType': str,
    'IncidentDate': str,
    'IncidentNotificationDate': str,
    'IncidentCompleteDate': str,
    'Source': str,
    'CauseCategory': str,
    'CauseType': str,
    'FailureType': str,
    'StrikeArea': str,
    'FieldCentre': str,
    'LicenseeID': int,
    'LicenseeName': str,
    'InjuryCount': int,
    'FatalityCount': int,
    'Jurisdiction': str,
    'ReleaseOffsite': str,
    'SensitiveArea': str,
    'PublicAffected': str,
    'EnvironmentAffected': str,
    'WildlifeLivestockAffected': str,
    'AreaAffected': str,
    'PublicEvacuatedCount': int,
    'ReleaseCleanupDate': str,
    'PipelineLicenceSegmentID': int,
    'PipelineLicenceLineNo': int,
    'PipeDamageType': str,
    'PipeTestFailure': str,
    'PipelineOutsideDiameter(mm)': decimal.Decimal,
    'PipeGrade': str,
    'PipeWallThickness(mm)': decimal.Decimal,
    'Substance Released': str,
    'Volume Released': decimal.Decimal,
    'Volume Recovered': decimal.Decimal,
    'Volume Units': str,
    'Substance Released 2': str,
    'Volume Released 2': decimal.Decimal,
    'Volume Recovered 2': decimal.Decimal,
    'Volume Units 2': str,
    'Substance Released 3': str,
    'Volume Released 3': decimal.Decimal,
    'Volume Recovered 3': decimal.Decimal,
    'Volume Units 3': str,
    'Substance Released 4': str,
    'Volume Released 4': decimal.Decimal,
    'Volume Recovered 4': decimal.Decimal,
    'Volume Units 4': str
}

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('Spills')

with open("everettx_spills.json") as json_file:
    db_obj = json.load(json_file, parse_float = decimal.Decimal)
    spills = db_obj[2]['data']
    for spill in tqdm.tqdm(spills):
        db_spill = spill.copy()
        for key, value in spill.items():
            if value == '' or value is None:
                del db_spill[key]
            elif key in type_conversions:
                db_spill[key] = type_conversions[key](value)

        table.put_item(
           Item=db_spill
        )