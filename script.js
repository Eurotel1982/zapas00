fetch("data.json")
  .then(response => response.json())
  .then(data => {
    const tableBody = document.querySelector("#results-table tbody");

    // Seřadit sestupně podle počtu 0:0
    data.sort((a, b) => b["draws_0_0"] - a["draws_0_0"]);

    data.forEach(item => {
      const row = document.createElement("tr");

      const leagueCell = document.createElement("td");
      leagueCell.textContent = item.league;
      row.appendChild(leagueCell);

      const roundCell = document.createElement("td");
      roundCell.textContent = item.round;
      row.appendChild(roundCell);

      const drawsCell = document.createElement("td");
      drawsCell.textContent = item["draws_0_0"];
      row.appendChild(drawsCell);

      tableBody.appendChild(row);
    });
  });
