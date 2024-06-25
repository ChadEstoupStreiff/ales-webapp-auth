

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
        document.getElementById('userInfo').innerHTML = "<h3>ID: " + userInfo.sub + "</h3><h3>Name: " + userInfo.name + "</h3><h3>E-Mail: " + userInfo.email + "</h3><h3>Expiration: " + date.toUTCString() + "</h3>";
    });
}

token = loadToken()
fetchUserInfo(token)
reload()

function reload() {
    document.getElementById("flights_list").innerHTML = "<span class='loader'></span>"
    document.getElementById("hotels_list").innerHTML = "<span class='loader'></span>"

    fetch('http://localhost:8902/flights/reservations', {
        headers: {
            'Authorization': `Bearer ${token}`
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(flights => {   
        html = ""
        flights.forEach(e => {
            html = html + "<hr/><div class='flighinfo'><p>ID: " + e.flight_id + "</p><p>Departure: " + e.departure_date + "</p><p>Return: " + e.return_date + "</p><p>Nbr of tickets: " + e.number_of_tickets + "</p></div>"
        });
        document.getElementById("flights_list").innerHTML = html
    });

    fetch('http://localhost:8902/hotels/reservations', {
        headers: {
            'Authorization': `Bearer ${token}`
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(hotels => {
        html = ""
        hotels.forEach(e => {
            html = html + "<hr/><div class='hotelinfo'><p>ID: " + e.hotel_id + "</p><p>Check in: " + e.check_in_date + "</p><p>Check out: " + e.check_out_date + "</p><p>Nbr of rooms: " + e.number_of_rooms + "</p></div>"
        });
        document.getElementById("hotels_list").innerHTML = html
    });
}

document.getElementById('flight_reserve').addEventListener('click', () => {
    fetch('http://localhost:8902/flights/reserve?flight=' + document.getElementById("flight_id").value, {
        headers: {
            'Authorization': `Bearer ${token}`
        },
        method: "POST",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(_ => {
        reload()  
    });
});


document.getElementById('hotel_reserve').addEventListener('click', () => {
    fetch('http://localhost:8902/hotels/reserve?hotel=' + document.getElementById("hotel_id").value, {
        headers: {
            'Authorization': `Bearer ${token}`
        },
        method: "POST",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(_ => {
        reload()  
    });
});