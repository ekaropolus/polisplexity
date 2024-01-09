document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');

    loginBtn.addEventListener('click', function() {
        const hardcodedUsername = 'admin'; // Replace with the actual username or user ID

        fetch('/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username: hardcodedUsername})
        })
        .then(response => {
            if (response.status === 200) {
                loginBtn.disabled = true;
                logoutBtn.disabled = false;
                console.log('Login successful');
            } else {
                console.error('Login failed with status: ' + response.status);
            }
            return response.json();
        })
        .then(data => console.log(data.message))
        .catch(error => console.error('Error:', error));
    });

    logoutBtn.addEventListener('click', function() {
        fetch('/users/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.status === 200) {
                loginBtn.disabled = false;
                logoutBtn.disabled = true;
                console.log('Logout successful');
            } else {
                console.error('Logout failed with status: ' + response.status);
            }
            return response.json();
        })
        .then(data => console.log(data.message))
        .catch(error => console.error('Error:', error));
    });
});
