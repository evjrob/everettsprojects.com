export async function onRequestPost(context) {
    try {
      const event = await context.request.json();
      
      // Get all of the POST data
      const {
        Location: location,
        currentLicensee: licensee,
        currentSubstance: substance,
        currentSource: source,
        currentFailure: failure,
        yearMin,
        yearMax,
        volumeMin,
        volumeMax,
        injuryMin,
        injuryMax,
        fatalityMin,
        fatalityMax
      } = event;
  
      // Fix the years to go from start of first year to end of the last
      const dateMin = `${yearMin}-01-01`;
      const dateMax = `${yearMax}-12-31`;
  
      // Start building the SQL query
      let sql = `
        SELECT * 
        FROM Spills 
        WHERE Location = ? 
        AND IncidentDate BETWEEN ? AND ?
        AND "Volume Released" BETWEEN ? AND ?
        AND InjuryCount BETWEEN ? AND ?
        AND FatalityCount BETWEEN ? AND ?
      `;
  
      let params = [
        location,
        dateMin,
        dateMax,
        volumeMin,
        volumeMax,
        injuryMin,
        injuryMax,
        fatalityMin,
        fatalityMax
      ];
  
      // Add optional filters
      if (licensee !== "All") {
        sql += " AND LicenseeName = ?";
        params.push(licensee);
      }
      if (substance !== "All") {
        sql += ' AND "Substance Released" = ?';
        params.push(substance);
      }
      if (source !== "All") {
        sql += " AND Source = ?";
        params.push(source);
      }
      if (failure !== "All") {
        sql += " AND FailureType = ?";
        params.push(failure);
      }
  
      sql += " ORDER BY IncidentDate DESC";
  
      // Execute query using D1
      const results = await context.env.spills.prepare(sql)
        .bind(...params)
        .all();
  
      return new Response(JSON.stringify(results.results), {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": "true"
        }
      });
  
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      });
    }
  }