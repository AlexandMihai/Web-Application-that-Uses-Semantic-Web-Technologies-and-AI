document.getElementById('password-reset-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const messageElement = document.getElementById('message');

    fetch('http://127.0.0.1:5000/forgot_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            messageElement.textContent = 'A reset code has been sent to your email.';
            window.location.href = '/password_change';
        } else {
            messageElement.textContent = data.message;
        }
    })
    .catch(error => {
        messageElement.textContent = 'An error occurred. Please try again later.';
    });
});
