
fetch('data.json')
  .then(response => response.json())
  .then(data => {
    const table = document.querySelector("tbody");
    data.forEach(item => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.league}</td>
        <td>${item.round}</td>
        <td>${item.draws_0_0}</td>
        <td>${item.max_draws}</td>
      `;
      // Zvýraznění řádku, pokud už je dosažen maximální počet 0:0
      if (item.draws_0_0 === item.max_draws) {
        row.style.backgroundColor = '#ffcccc'; // červená = dosaženo maxima  
      } else if (item.draws_0_0 === item.max_draws - 1) {
        row.style.backgroundColor = '#ccffcc'; // zelená = o 1 méně než maximum
      }
      table.appendChild(row);
    });
  })
  .catch(error => {
    console.error("Chyba při načítání dat:", error);
  });
