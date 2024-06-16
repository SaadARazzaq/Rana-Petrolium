document.addEventListener('DOMContentLoaded', function() {
    const salesForm = document.getElementById('sales-form');
    const dbContainer = document.getElementById('db-container');
    const diffDbContainer = document.getElementById('diff-db-container');
    const salesBtn = document.getElementById('nozzle-data-btn');
    const viewDbBtn = document.getElementById('nozzle-db-btn');
    const viewDiffDbBtn = document.getElementById('nozzle-difference-db-btn');
    const submitSalesBtn = document.getElementById('submit-sales');
    const nozzlesContainer = document.getElementById('nozzles');

    salesForm.style.display = 'none';
    dbContainer.style.display = 'none';
    diffDbContainer.style.display = 'none';

    salesBtn.addEventListener('click', function() {
        salesForm.style.display = 'block';
        dbContainer.style.display = 'none';
        diffDbContainer.style.display = 'none';
    });

    viewDbBtn.addEventListener('click', function() {
        salesForm.style.display = 'none';
        dbContainer.style.display = 'block';
        diffDbContainer.style.display = 'none';
        fetchDbContent();
    });

    viewDiffDbBtn.addEventListener('click', function() {
        salesForm.style.display = 'none';
        dbContainer.style.display = 'none';
        diffDbContainer.style.display = 'block';
        fetchDifferencesDbContent();
    });

    for (let i = 1; i <= 8; i++) {
        const div = document.createElement('div');
        div.classList.add('form-group');
        const label = document.createElement('label');
        label.innerText = `Nozzle ${i} (liters):`;
        const input = document.createElement('input');
        input.type = 'number';
        input.placeholder = `Enter nozzle ${i} reading in liters`;
        input.classList.add('nozzle-input');
        div.appendChild(label);
        div.appendChild(input);
        nozzlesContainer.appendChild(div);
    }

    submitSalesBtn.addEventListener('click', function() {
        const petrolRateInput = document.getElementById('petrol-rate');
        const petrolRate = parseFloat(petrolRateInput.value);

        if (isNaN(petrolRate) || petrolRate <= 0) {
            alert('Please enter a valid petrol rate.');
            petrolRateInput.focus();
            return;
        }

        const nozzleInputs = document.getElementsByClassName('nozzle-input');
        const nozzles = Array.from(nozzleInputs).map(input => {
            const value = parseFloat(input.value);
            if (isNaN(value) || value < 0) {
                alert(`Please enter a valid reading for ${input.previousElementSibling.innerText}`);
                input.focus();
                throw new Error('Invalid input');
            }
            return value;
        });

        const data = { petrol_rate: petrolRate, nozzles: nozzles };

        fetch('/submit_sales', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Data submitted successfully!');
                petrolRateInput.value = '';
                Array.from(nozzleInputs).forEach(input => input.value = '');
            } else {
                alert('Error submitting data: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function fetchDbContent() {
        fetch('/fetch_db')
        .then(response => response.json())
        .then(data => {
            const dbTable = document.getElementById('db-table');
            const thead = dbTable.querySelector('thead tr');
            const tbody = dbTable.querySelector('tbody');
            
            thead.innerHTML = '';
            tbody.innerHTML = '';

            if (data.length > 0) {
                const headers = ['ID', 'Date', 'Day', 'Petrol Rate', 'Nozzle 1', 'Nozzle 2', 'Nozzle 3', 'Nozzle 4', 'Nozzle 5', 'Nozzle 6', 'Nozzle 7', 'Nozzle 8'];
                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.innerText = header;
                    thead.appendChild(th);
                });

                data.forEach(row => {
                    const tr = document.createElement('tr');
                    headers.forEach(header => {
                        const key = header.toLowerCase().replace(/ /g, '_');
                        const td = document.createElement('td');
                        td.innerText = row[key];
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                });
            }
        });
    }

    // function fetchDifferencesDbContent() {
    //     fetch('/fetch_differences_db')
    //     .then(response => response.json())
    //     .then(data => {
    //         const dbTable = document.getElementById('differences-db-table');
    //         const thead = dbTable.querySelector('thead tr');
    //         const tbody = dbTable.querySelector('tbody');
            
    //         thead.innerHTML = '';
    //         tbody.innerHTML = '';

    //         if (data.length > 0) {
    //             const headers = ['ID', 'Date', 'Day', 'Petrol Rate Diff', 'Nozzle 1 Diff', 'Nozzle 2 Diff', 'Nozzle 3 Diff', 'Nozzle 4 Diff', 'Nozzle 5 Diff', 'Nozzle 6 Diff', 'Nozzle 7 Diff', 'Nozzle 8 Diff'];
    //             headers.forEach(header => {
    //                 const th = document.createElement('th');
    //                 th.innerText = header;
    //                 thead.appendChild(th);
    //             });

    //             data.forEach(row => {
    //                 const tr = document.createElement('tr');
    //                 headers.forEach(header => {
    //                     const key = header.toLowerCase().replace(/ /g, '_');
    //                     const td = document.createElement('td');
    //                     td.innerText = row[key];
    //                     tr.appendChild(td);
    //                 });
    //                 tbody.appendChild(tr);
    //             });
    //         }
    //     });
    // }

    function fetchDifferencesDbContent() {
        fetch('/fetch_differences_db')
        .then(response => response.json())
        .then(data => {
            const dbTable = document.getElementById('differences-db-table');
            const thead = dbTable.querySelector('thead tr');
            const tbody = dbTable.querySelector('tbody');
            
            thead.innerHTML = '';
            tbody.innerHTML = '';
    
            if (data.length > 0) {
                const headers = ['ID', 'Date', 'Day', 'Petrol Rate Diff', 'Nozzle 1 Diff', 'Nozzle 2 Diff', 'Nozzle 3 Diff', 'Nozzle 4 Diff', 'Nozzle 5 Diff', 'Nozzle 6 Diff', 'Nozzle 7 Diff', 'Nozzle 8 Diff'];
                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.innerText = header;
                    thead.appendChild(th);
                });
    
                data.forEach(row => {
                    const tr = document.createElement('tr');
                    headers.forEach(header => {
                        const key = header.toLowerCase().replace(/ /g, '_');
                        const td = document.createElement('td');
                        td.innerText = row[key];
    
                        // Apply color based on value
                        if (key.includes('diff')) {
                            const value = parseFloat(row[key]);
                            if (!isNaN(value)) {
                                if (value > 0) {
                                    td.style.color = 'green';
                                } else if (value < 0) {
                                    td.style.color = 'red';
                                }
                            }
                        }
    
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                });
            }
        });
    }
    
});
