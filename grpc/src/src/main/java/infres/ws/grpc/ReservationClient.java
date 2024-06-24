package infres.ws.grpc;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import reservation.FlightReservationGrpc;
import reservation.HotelReservationGrpc;
import reservation.Main;

public class ReservationClient {
    public static void main(String[] args) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 8080)
                .usePlaintext()
                .build();

        HotelReservationGrpc.HotelReservationBlockingStub hotelStub = HotelReservationGrpc.newBlockingStub(channel);
        FlightReservationGrpc.FlightReservationBlockingStub flightStub = FlightReservationGrpc.newBlockingStub(channel);

        Main.HotelRequest hotelRequest = Main.HotelRequest.newBuilder()
                .setHotelId("hotel123")
                .setUserId("user456")
                .setCheckInDate("2024-07-01")
                .setCheckOutDate("2024-07-10")
                .setNumberOfRooms(1)
                .build();

        Main.HotelResponse hotelResponse = hotelStub.reserveHotel(hotelRequest);
        System.out.println("Hotel reservation: " + hotelResponse);

        Main.FlightRequest flightRequest = Main.FlightRequest.newBuilder()
                .setFlightId("flight789")
                .setUserId("user456")
                .setDepartureDate("2024-07-01")
                .setReturnDate("2024-07-10")
                .setNumberOfTickets(1)
                .build();

        Main.FlightResponse flightResponse = flightStub.reserveFlight(flightRequest);
        System.out.println("Flight reservation: " + flightResponse);

        channel.shutdown();
    }
}
