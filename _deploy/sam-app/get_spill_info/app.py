import json
import sqlite3


def get_spill_info(location, date_min, date_max, volume_min, volume_max, 
                   injury_min, injury_max, fatality_min, fatality_max,
                   licensee, substance, source, failure):
    # Database name in URI form, readonly
    database_name = "file:spills.db?mode=ro"

    # Create a database connection
    conn = sqlite3.connect(database_name, uri=True)
    
    with conn:
        cur = conn.cursor()

        # Start building the statement with the base of the query
        statement = "SELECT * \
                     FROM Spills \
                     WHERE ((`Location` = ? \
                     AND (`IncidentDate` BETWEEN ? AND ?) \
                     AND (`Volume Released` BETWEEN ? AND ?) \
                     AND (`InjuryCount` BETWEEN ? AND ?) \
                     AND (`FatalityCount` BETWEEN ? AND ?))"

        statement_params = [location, date_min, date_max, volume_min, volume_max,\
                            injury_min, injury_max, fatality_min, fatality_max]

        # Add in the filters if they're set
        if (licensee != "All"):
            statement = statement + " AND `LicenseeName` = ?"
            statement_params = statement_params + [licensee]
        
        if (substance != "All"):
            statement = statement + " AND `Substance Released` = ?"
            statement_params = statement_params + [substance]
        
        if (source != "All"):
            statement = statement + " AND `Source` = ?"
            statement_params = statement_params + [source]
        
        if (failure != "All"):
            statement = statement + " AND `FailureType` = ?"
            statement_params = statement_params + [failure]
        

        # Finish the statement with the sorting and limit parts
        statement = statement + ") ORDER BY `IncidentDate` DESC"

        cur.execute(statement, tuple(statement_params))
        rows = cur.fetchall()
        col_names = ['IncidentNumber', 'IncidentType', 'Latitude', 'Longitude',
        	'Location', 'IncidentLSD', 'IncidentSection', 'IncidentTownship',
            'IncidentRange', 'IncidentMeridian', 'LicenceNumber', 'LicenceType',
            'IncidentDate', 'IncidentNotificationDate', 'IncidentCompleteDate',
            'Source', 'CauseCategory', 'CauseType', 'FailureType', 'StrikeArea',
            'FieldCentre', 'LicenseeID', 'LicenseeName', 'InjuryCount', 
            'FatalityCount', 'Jurisdiction', 'ReleaseOffsite', 'SensitiveArea',
            'PublicAffected', 'EnvironmentAffected', 'WildlifeLivestockAffected',
            'AreaAffected', 'PublicEvacuatedCount', 'ReleaseCleanupDate',
            'PipelineLicenceSegmentID', 'PipelineLicenceLineNo', 'PipeDamageType',
            'PipeTestFailure', 'PipelineOutsideDiameter(mm)', 'PipeGrade', 
            'PipeWallThickness(mm)', 'Substance Released', 'Volume Released',
            'Volume Recovered', 'Substance Released 2', 'Volume Released 2',
            'Volume Recovered 2', 'Substance Released 3', 'Volume Released 3',
            'Volume Recovered 3', 'Substance Released 4', 'Volume Released 4',
            'Volume Recovered 4']

        def objectify(row):
            row_obj = dict(zip(col_names, row))
            return row_obj

        rows = [objectify(row) for row in rows]

        return rows
    

def lambda_handler(event, context):
    # Get all of the POST data
    location= event['Location']
    licensee = event['currentLicensee']
    substance = event['currentSubstance']
    source = event['currentSource']
    failure = event['currentFailure']
    year_min = event['yearMin']
    year_max = event['yearMax']
    volume_min = event['volumeMin']
    volume_max = event['volumeMax']
    injury_min = event['injuryMin']
    injury_max = event['injuryMax']
    fatality_min = event['fatalityMin']
    fatality_max = event['fatalityMax']

    # Fix the years to go from start of first year to end of the last.
    date_min = str(year_min) + "-01-01"
    date_max = str(year_max) + "-12-31"

    result = get_spill_info(location, date_min, date_max, volume_min, \
        volume_max, injury_min, injury_max, fatality_min, fatality_max, \
        licensee, substance, source, failure)
    
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True 
        },
        "body": result
    }

    # Spit out the results in json form
    return json.dumps(response)
    