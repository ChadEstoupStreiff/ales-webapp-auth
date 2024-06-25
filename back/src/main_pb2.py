# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: main.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nmain.proto\x12\x0breservation\"1\n\x0cHotelRequest\x12\x10\n\x08hotel_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"8\n\rHotelResponse\x12\x16\n\x0ereservation_id\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\"$\n\x11ListHotelsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"G\n\x12ListHotelsResponse\x12\x31\n\x06hotels\x18\x01 \x03(\x0b\x32!.reservation.HotelReservationInfo\"\x81\x01\n\x14HotelReservationInfo\x12\x10\n\x08hotel_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x15\n\rcheck_in_date\x18\x03 \x01(\t\x12\x16\n\x0e\x63heck_out_date\x18\x04 \x01(\t\x12\x17\n\x0fnumber_of_rooms\x18\x05 \x01(\x05\"3\n\rFlightRequest\x12\x11\n\tflight_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"9\n\x0e\x46lightResponse\x12\x16\n\x0ereservation_id\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\"%\n\x12ListFlightsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"J\n\x13ListFlightsResponse\x12\x33\n\x07\x66lights\x18\x01 \x03(\x0b\x32\".reservation.FlightReservationInfo\"r\n\x15\x46lightReservationInfo\x12\x11\n\tflight_id\x18\x01 \x01(\t\x12\x16\n\x0e\x64\x65parture_date\x18\x03 \x01(\t\x12\x13\n\x0breturn_date\x18\x04 \x01(\t\x12\x19\n\x11number_of_tickets\x18\x05 \x01(\x05\x32\xb0\x01\n\x10HotelReservation\x12\x45\n\x0cReserveHotel\x12\x19.reservation.HotelRequest\x1a\x1a.reservation.HotelResponse\x12U\n\x12ListReservedHotels\x12\x1e.reservation.ListHotelsRequest\x1a\x1f.reservation.ListHotelsResponse2\xb7\x01\n\x11\x46lightReservation\x12H\n\rReserveFlight\x12\x1a.reservation.FlightRequest\x1a\x1b.reservation.FlightResponse\x12X\n\x13ListReservedFlights\x12\x1f.reservation.ListFlightsRequest\x1a .reservation.ListFlightsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'main_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_HOTELREQUEST']._serialized_start=27
  _globals['_HOTELREQUEST']._serialized_end=76
  _globals['_HOTELRESPONSE']._serialized_start=78
  _globals['_HOTELRESPONSE']._serialized_end=134
  _globals['_LISTHOTELSREQUEST']._serialized_start=136
  _globals['_LISTHOTELSREQUEST']._serialized_end=172
  _globals['_LISTHOTELSRESPONSE']._serialized_start=174
  _globals['_LISTHOTELSRESPONSE']._serialized_end=245
  _globals['_HOTELRESERVATIONINFO']._serialized_start=248
  _globals['_HOTELRESERVATIONINFO']._serialized_end=377
  _globals['_FLIGHTREQUEST']._serialized_start=379
  _globals['_FLIGHTREQUEST']._serialized_end=430
  _globals['_FLIGHTRESPONSE']._serialized_start=432
  _globals['_FLIGHTRESPONSE']._serialized_end=489
  _globals['_LISTFLIGHTSREQUEST']._serialized_start=491
  _globals['_LISTFLIGHTSREQUEST']._serialized_end=528
  _globals['_LISTFLIGHTSRESPONSE']._serialized_start=530
  _globals['_LISTFLIGHTSRESPONSE']._serialized_end=604
  _globals['_FLIGHTRESERVATIONINFO']._serialized_start=606
  _globals['_FLIGHTRESERVATIONINFO']._serialized_end=720
  _globals['_HOTELRESERVATION']._serialized_start=723
  _globals['_HOTELRESERVATION']._serialized_end=899
  _globals['_FLIGHTRESERVATION']._serialized_start=902
  _globals['_FLIGHTRESERVATION']._serialized_end=1085
# @@protoc_insertion_point(module_scope)
