fetch('data.json')
  .then(response => response.json())
  .then(data => {
    const table = document.querySelector("tbody");

    // Seřadíme data podle počtu 0:0 v tomto kole (sestupně)
    data.sort((a, b) => b.draws_0_0 - a.draws_0_0);

    data.forEach(item => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.league}</td>
        <td>${item.round}</td>
        <td>${item.draws_0_0}</td>
        <td>${item.max_draws}</td>
      `;

      // Barevné zvýraznění podle počtu remíz
      if (item.draws_0_0 === item.max_draws) {
        row.style.backgroundColor = '#ffcccc'; // červená
      } else if (item.draws_0_0 === item.max_draws - 1) {
        row.style.backgroundColor = '#ccffcc'; // zelená
      }

      table.appendChild(row);
    });
  })
  .catch(error => {
    console.error("Chyba při načítání dat:", error);
  });
