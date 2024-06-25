package infres.ws.grpc;

import com.google.type.DateTime;
import reservation.Main;

import java.time.Instant;
import java.time.LocalDate;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

public class Manager {

    private static Manager instance;

    public static Manager getInstance() {
        if (instance == null) {
            instance = new Manager();
        }
        return instance;
    }

    private static Date generateRandomFutureDate() {
        Instant now = Instant.now();

        long maxDaysInFuture = 365;
        long randomDaysToAdd = ThreadLocalRandom.current().nextLong(1, maxDaysInFuture + 1);

        Instant randomFutureInstant = now.plusSeconds(randomDaysToAdd * 24 * 60 * 60);
        return Date.from(randomFutureInstant);
    }

    private ArrayList<Main.FlightReservationInfo> flights = new ArrayList<>();
    private ArrayList<Main.HotelReservationInfo> hotels = new ArrayList<>();

    private HashMap<String, ArrayList<String>> reservationsFlights = new HashMap<>();
    private HashMap<String, ArrayList<String>> reservationsHotels = new HashMap<>();


    public boolean reserverFlight(String user, String flight) {
        if (flights.stream().noneMatch(f -> f.getFlightId().equals(flight))) {
            flights.add(Main.FlightReservationInfo.newBuilder()
                            .setFlightId(flight)
                            .setDepartureDate(generateRandomFutureDate().toString())
                            .setReturnDate(generateRandomFutureDate().toString())
                            .setNumberOfTickets(new Random().nextInt(1, 6))
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
                    .setCheckInDate(generateRandomFutureDate().toString())
                    .setCheckOutDate(generateRandomFutureDate().toString())
                    .setNumberOfRooms(new Random().nextInt(1, 6))
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
