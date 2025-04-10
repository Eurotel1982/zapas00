
fetch('data.json')
    .then(response => response.json())
    .then(data => {
        const tbody = document.querySelector('#results-table tbody');
        data.forEach(item => {
            const tr = document.createElement('tr');
            if (item.draws_00_current >= item.draws_00_max && item.matches_remaining > 0) {
                tr.classList.add('highlight');
            }
            tr.innerHTML = `
                <td>${item.league}</td>
                <td>${item.round}</td>
                <td>${item.draws_00_current}</td>
                <td>${item.draws_00_max}</td>
                <td>${item.matches_remaining}</td>
            `;
            tbody.appendChild(tr);
        });
    });
