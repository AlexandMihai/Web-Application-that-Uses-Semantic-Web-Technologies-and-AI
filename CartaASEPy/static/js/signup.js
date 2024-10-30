function signupUser() {
    const username = document.getElementById("signupUsername").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    fetch('http://127.0.0.1:5000/signupprocess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert("Account created successfully!");
            window.location.href = "/login.html";
        } else {
            alert("Signup error: " + data.message);
        }
    });
}