document.addEventListener('DOMContentLoaded', () => {
    const userTable = document.getElementById('userTable');
    const userSelect = document.getElementById('userSelect');


    // Fetch users and populate table and dropdown
    function fetchUsers() {
        fetch('/users')
            .then(response => response.json())
            .then(users => {
                userTable.innerHTML = '';
                userSelect.innerHTML = '';
                users.forEach(user => {
                    // Populate table
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${user.name}</td>
                        <td>${user.status}</td>
                        <td><button onclick="downloadEma('${user.name}')">Download</button></td>
                    `;
                    userTable.appendChild(row);

                    // Populate dropdown
                    const option = document.createElement('option');
                    option.value = user.name;
                    option.textContent = user.name;
                    userSelect.appendChild(option);
                });
            });
    }

    // Download EMA
    window.downloadEma = function (username) {
        window.location.href = `/download/${username}`;
    };

    // Replace EMA
    document.getElementById('replaceEmaForm').addEventListener('submit', event => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('user', userSelect.value);
        formData.append('file', document.getElementById('fileReplace').files[0]);
        
        fetch('/replace-ema', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            fetchUsers();
        });
    });

    // Add User
    document.getElementById('addUserForm').addEventListener('submit', event => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('user', document.getElementById('newUserName').value);
        formData.append('file', document.getElementById('fileAdd').files[0]);
        
        fetch('/add-user', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            fetchUsers();
        });
    });

    // Periodic polling to refresh user data
    function startPolling(interval = 5000) { // 5 seconds
        setInterval(fetchUsers, interval);
    }

    // Initial fetch and polling
    fetchUsers();
    startPolling();
});
