package infres.ws.grpc;


import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import reservation.FlightReservationGrpc;
import reservation.HotelReservationGrpc;
import reservation.Main;

import java.util.List;
import java.util.UUID;

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
        responseObserver.onNext(Main.HotelResponse.newBuilder()
                .setReservationId(UUID.randomUUID().toString())
                .setSuccess(Manager.getInstance().reserverHotel(req.getUserId(), req.getHotelId()))
                .build());
        responseObserver.onCompleted();
    }

    @Override
    public void listReservedHotels(Main.ListHotelsRequest req, StreamObserver<Main.ListHotelsResponse> responseObserver) {
        responseObserver.onNext(Main.ListHotelsResponse.newBuilder().addAllHotels(Manager.getInstance().getHotels(req.getUserId())).build());
        responseObserver.onCompleted();
    }
}

class FlightReservationServiceImpl extends FlightReservationGrpc.FlightReservationImplBase {
    @Override
    public void reserveFlight(Main.FlightRequest req, StreamObserver<Main.FlightResponse> responseObserver) {
        responseObserver.onNext(Main.FlightResponse.newBuilder()
                .setReservationId(UUID.randomUUID().toString())
                .setSuccess(Manager.getInstance().reserverFlight(req.getUserId(), req.getFlightId()))
                .build());
        responseObserver.onCompleted();
    }

    @Override
    public void listReservedFlights(Main.ListFlightsRequest req, StreamObserver<Main.ListFlightsResponse> responseObserver) {
        responseObserver.onNext(Main.ListFlightsResponse.newBuilder().addAllFlights(Manager.getInstance().getFlights(req.getUserId())).build());
        responseObserver.onCompleted();
    }
}

class company {
    public int id;
    public String name;
}

