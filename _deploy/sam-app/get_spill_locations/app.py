import json
import sqlite3


def get_spill_locations(long_min, long_max, lat_min, lat_max, date_min, date_max, 
                        volume_min, volume_max, injury_min, injury_max, 
                        fatality_min, fatality_max, licensee, substance, source, 
                        failure):
    # Database name in URI form, readonly
    database_name = "file:spills.db?mode=ro"

    # Create a database connection
    conn = sqlite3.connect(database_name, uri=True)
    
    with conn:
        cur = conn.cursor()

        # Start building the statement with the base of the query
        statement = "SELECT DISTINCT `Location`, `Latitude`, `Longitude` \
                     FROM Spills \
                     WHERE (((`Longitude` BETWEEN ? AND ?) \
                     AND (`Latitude` BETWEEN ? AND ?) \
                     AND (`IncidentDate` BETWEEN ? AND ?) \
                     AND (`Volume Released` BETWEEN ? AND ?) \
                     AND (`InjuryCount` BETWEEN ? AND ?) \
                     AND (`FatalityCount` BETWEEN ? AND ?))"

        statement_params = [long_min, long_max, lat_min, lat_max, \
                            date_min, date_max, volume_min, volume_max, \
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
        statement = statement + ") ORDER BY `Volume Released` DESC LIMIT 100"

        cur.execute(statement, tuple(statement_params))
        rows = cur.fetchall()

        def objectify(row):
            row_obj = {
                "Location":row[0],
                "Latitude":row[1],
                "Longitude":row[2]
            }
            return row_obj

        rows = [objectify(row) for row in rows]

        return rows
    

def lambda_handler(event, context):
    # Get all of the POST data
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
    lat_min = event['latMin']
    lat_max = event['latMax']
    long_min = event['lngMin']
    long_max = event['lngMax']

    # Fix the years to go from start of first year to end of the last.
    date_min = str(year_min) + "-01-01"
    date_max = str(year_max) + "-12-31"

    result = get_spill_locations(long_min, long_max, lat_min, lat_max, date_min, \
        date_max, volume_min, volume_max, injury_min, injury_max, fatality_min, \
        fatality_max, licensee, substance, source, failure)
    
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