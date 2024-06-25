

function fetchUserInfo(token) {
    fetch('http://localhost:8902/token', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(userInfo => {
        var date = new Date(userInfo.exp);
        document.getElementById('userInfo').innerHTML = "<h3>ID: " + userInfo.sub + ", Name: " + userInfo.name + ", E-Mail: " + userInfo.email + ", Expiration: " + date.toUTCString() + "</h3>";
    });
}

token = loadToken()
console.log(token)
fetchUserInfo(token)