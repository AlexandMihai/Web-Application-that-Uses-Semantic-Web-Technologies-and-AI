function loginUser() {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    fetch('http://127.0.0.1:5000/loginprocess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            console.log("Login successful!");
            localStorage.setItem('userToken', data.access_token);
            window.location.href = "/";
        } else {
            console.log("Login error!");
            alert("Login failed: " + (data.message || 'Unknown error'));
        }
    });
}
