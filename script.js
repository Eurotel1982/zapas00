fetch("data.json")
  .then(response => response.json())
  .then(data => {
    const halftimeData = data["halftime_draws_series"];

    const halftimeTableBody = document.querySelector("#halftime-table tbody");

    halftimeData.sort((a, b) => b.series_count - a.series_count);

    halftimeData.forEach(item => {
      const row = document.createElement("tr");

      const leagueCell = document.createElement("td");
      leagueCell.textContent = item.league;
      row.appendChild(leagueCell);

      const roundCell = document.createElement("td");
      roundCell.textContent = item.round;
      row.appendChild(roundCell);

      const seriesCell = document.createElement("td");
      seriesCell.textContent = item.series_count;
      row.appendChild(seriesCell);

      halftimeTableBody.appendChild(row);
    });
  });
