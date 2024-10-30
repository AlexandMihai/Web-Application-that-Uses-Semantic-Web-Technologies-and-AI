document.getElementById('password-change-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const userCode = document.getElementById('code').value;
    const newPassword = document.getElementById('new-password').value;
    const confirmNewPassword = document.getElementById('confirm-new-password').value;
    const messageElement = document.getElementById('message');

    if (newPassword !== confirmNewPassword) {
        messageElement.textContent = 'Passwords do not match.';
        return;
    }

    fetch('http://localhost:5000/reset_and_change_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: userCode, password: newPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            messageElement.textContent = 'Password updated successfully.';
            window.location.href = '/login';
        } else {
            messageElement.textContent = data.message;
        }
    })
    .catch(error => {
        messageElement.textContent = 'An error occurred. Please try again later.';
    });
});
