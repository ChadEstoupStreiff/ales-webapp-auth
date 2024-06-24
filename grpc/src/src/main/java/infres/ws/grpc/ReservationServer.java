package infres.ws.grpc;


import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import reservation.FlightReservationGrpc;
import reservation.HotelReservationGrpc;
import reservation.Main;


/**
 * Hello world!
 *
 */

public class ReservationServer {
    public static void main(String[] args) throws Exception {
        Server server = ServerBuilder.forPort(8080)
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
    public void reserveHotel(Main.HotelRequest req, StreamObserver<Main.HotelResponse> responseObserver) {
        Main.HotelResponse response = Main.HotelResponse.newBuilder()
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
    public void reserveFlight(Main.FlightRequest req, StreamObserver<Main.FlightResponse> responseObserver) {
        Main.FlightResponse response = Main.FlightResponse.newBuilder()
                .setReservationId("54321")
                .setSuccess(true)
                .setMessage("Reservation successful")
                .build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}

