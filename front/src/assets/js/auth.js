document.getElementById('loginBtn').addEventListener('click', () => {
    fetch('http://localhost:8902/login/google')
        .then(response => response.json())
        .then(data => {
            window.location.href = data.url;
        });
});

document.getElementById('loginkBtn').addEventListener('click', () => {
    fetch('http://localhost:8902/login/keycloak')
        .then(response => response.json())
        .then(data => {
            window.location.href = data.url;
        });
});

function loadToken() {
    const match = document.cookie.match(new RegExp('(^| )token=([^;]+)'));
    if (match) {
        return match[2];
    }
    return null;
}
