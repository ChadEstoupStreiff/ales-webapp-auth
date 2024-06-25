document.getElementById('loginBtn').addEventListener('click', () => {
    fetch('http://localhost:8902/login/google')
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

// function fetchUserInfo(token) {
//     fetch('http://localhost:8902/token', {
//         headers: {
//             'Authorization': `Bearer ${token}`
//         }
//     })
//     .then(response => response.json())
//     .then(userInfo => {
//         document.getElementById('userInfo').innerText = JSON.stringify(userInfo, null, 2);
//     });
// }