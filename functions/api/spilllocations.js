export const onRequestPost = async (context) => {
  try {
    const event = await context.request.json();
    
    // Fix the years to go from start of first year to end of the last
    const dateMin = `${event.yearMin}-01-01`;
    const dateMax = `${event.yearMax}-12-31`;

    // Start building the SQL query
    let sql = `
      SELECT DISTINCT Location, Latitude, Longitude 
      FROM Spills 
      WHERE (
        (Longitude BETWEEN ? AND ?)
        AND (Latitude BETWEEN ? AND ?)
        AND (IncidentDate BETWEEN ? AND ?)
        AND ("Volume Released" BETWEEN ? AND ?)
        AND (InjuryCount BETWEEN ? AND ?)
        AND (FatalityCount BETWEEN ? AND ?)
    `;

    const params = [
      event.lngMin, event.lngMax,
      event.latMin, event.latMax,
      dateMin, dateMax,
      event.volumeMin, event.volumeMax,
      event.injuryMin, event.injuryMax,
      event.fatalityMin, event.fatalityMax
    ];

    // Add filters if they're set
    if (event.currentLicensee !== 'All') {
      sql += ' AND LicenseeName = ?';
      params.push(event.currentLicensee);
    }
    
    if (event.currentSubstance !== 'All') {
      sql += ' AND "Substance Released" = ?';
      params.push(event.currentSubstance);
    }
    
    if (event.currentSource !== 'All') {
      sql += ' AND Source = ?';
      params.push(event.currentSource);
    }
    
    if (event.currentFailure !== 'All') {
      sql += ' AND FailureType = ?';
      params.push(event.currentFailure);
    }

    // Finish the statement
    sql += ') ORDER BY "Volume Released" DESC LIMIT 100';

    // Execute the query
    const results = await context.env.DB.prepare(sql)
      .bind(...params)
      .all();

    return new Response(JSON.stringify(results.results), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true',
      },
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
};