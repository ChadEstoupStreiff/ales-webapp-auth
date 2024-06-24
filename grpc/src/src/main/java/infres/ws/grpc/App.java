package infres.ws.grpc;


import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;


/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );
    }
}

public class ReservationServer {
    public static void main(String[] args) throws Exception {
        Server server = ServerBuilder.forPort(50051)
                .addService(new HotelReservationServiceImpl())
                .addService(new FlightReservationServiceImpl())
                .build()
                .start();

        System.out.println("Server started, listening on " + server.getPort());
        server.awaitTermination();
    }
}

class HotelReservationServiceImpl extends HotelReservationGrpc.HotelReservationImplBase {
    @Override
    public void reserveHotel(HotelRequest req, StreamObserver<HotelResponse> responseObserver) {
        HotelResponse response = HotelResponse.newBuilder()
                .setReservationId("12345")
                .setSuccess(true)
                .setMessage("Reservation successful")
                .build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}

class FlightReservationServiceImpl extends FlightReservationGrpc.FlightReservationImplBase {
    @Override
    public void reserveFlight(FlightRequest req, StreamObserver<FlightResponse> responseObserver) {
        FlightResponse response = FlightResponse.newBuilder()
                .setReservationId("54321")
                .setSuccess(true)
                .setMessage("Reservation successful")
                .build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}

public class ReservationClient {
    public static void main(String[] args) {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 50051)
                .usePlaintext()
                .build();

        HotelReservationGrpc.HotelReservationBlockingStub hotelStub = HotelReservationGrpc.newBlockingStub(channel);
        FlightReservationGrpc.FlightReservationBlockingStub flightStub = FlightReservationGrpc.newBlockingStub(channel);

        HotelRequest hotelRequest = HotelRequest.newBuilder()
                .setHotelId("hotel123")
                .setUserId("user456")
                .setCheckInDate("2024-07-01")
                .setCheckOutDate("2024-07-10")
                .setNumberOfRooms(1)
                .build();

        HotelResponse hotelResponse = hotelStub.reserveHotel(hotelRequest);
        System.out.println("Hotel reservation: " + hotelResponse);

        FlightRequest flightRequest = FlightRequest.newBuilder()
                .setFlightId("flight789")
                .setUserId("user456")
                .setDepartureDate("2024-07-01")
                .setReturnDate("2024-07-10")
                .setNumberOfTickets(1)
                .build();

        FlightResponse flightResponse = flightStub.reserveFlight(flightRequest);
        System.out.println("Flight reservation: " + flightResponse);

        channel.shutdown();
    }
}
