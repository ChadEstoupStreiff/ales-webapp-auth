package infres.ws.grpc;

import com.google.type.DateTime;
import reservation.Main;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

public class Manager {

    private static Manager instance;

    public static Manager getInstance() {
        if (instance == null) {
            instance = new Manager();
        }
        return instance;
    }

    private ArrayList<Main.FlightReservationInfo> flights = new ArrayList<>();
    private ArrayList<Main.HotelReservationInfo> hotels = new ArrayList<>();

    private HashMap<String, ArrayList<String>> reservationsFlights = new HashMap<>();
    private HashMap<String, ArrayList<String>> reservationsHotels = new HashMap<>();


    public boolean reserverFlight(String user, String flight) {
        if (flights.stream().noneMatch(f -> f.getFlightId().equals(flight))) {
            flights.add(Main.FlightReservationInfo.newBuilder()
                            .setFlightId(flight)
                            .setDepartureDate(LocalDate.now().toString())
                            .setNumberOfTickets(3)
                    .build());
        }

        ArrayList<String> flights = reservationsFlights.getOrDefault(user, new ArrayList<>());
        flights.add(flight);
        reservationsFlights.put(user, flights);
        return true;
    }

    public List<Main.FlightReservationInfo> getFlights(String user) {
        return flights.stream().filter(f -> reservationsFlights.get(user).contains(f.getFlightId())).toList();
    }

    public boolean reserverHotel(String user, String hotel) {
        if (hotels.stream().noneMatch(f -> f.getHotelId().equals(hotel))) {
            hotels.add(Main.HotelReservationInfo.newBuilder()
                    .setHotelId(hotel)
                    .setCheckInDate(LocalDate.now().toString())
                    .setCheckOutDate(LocalDate.now().toString())
                    .setNumberOfRooms(3)
                    .build());
        }

        ArrayList<String> hotels = reservationsHotels.getOrDefault(user, new ArrayList<>());
        hotels.add(hotel);
        reservationsHotels.put(user, hotels);
        return true;
    }

    public List<Main.HotelReservationInfo> getHotels(String user) {
        return hotels.stream().filter(f -> reservationsHotels.get(user).contains(f.getHotelId())).toList();
    }
}
