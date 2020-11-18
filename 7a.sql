CREATE OR REPLACE STREAM "data_stream" ("vendor_id" varchar(4), "pickup_datetime" TIMESTAMP, "dropoff_datetime" TIMESTAMP,
        "passenger_count" INTEGER, "trip_distance" REAL, "pickup_longitude" DOUBLE, "pickup_latitude" DOUBLE, 
        "rate_code" INTEGER, "dropoff_longitude" DOUBLE, "dropoff_latitude" DOUBLE, "payment_type" varchar(4), 
        "fare_amount" decimal(1,1), "surcharge" decimal(1,1), "mta_tax" DECIMAL(1,1), "tip_amount" REAL, "tolls_amount" REAL, 
        "total_amount" REAL, "trip_id" INTEGER, "type" varchar(4), "store_and_fwd_flag" INTEGER);
CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO "data_stream"
SELECT STREAM "vendor_id", "pickup_datetime", "dropoff_datetime",
        "passenger_count", "trip_distance", "pickup_longitude", "pickup_latitude", 
        "rate_code", "dropoff_longitude", "dropoff_latitude", "payment_type", 
        "fare_amount", "surcharge", "mta_tax", "tip_amount", "tolls_amount", 
        "total_amount", "trip_id", "type", "store_and_fwd_flag"
FROM "SOURCE_SQL_STREAM_001"
WHERE "total_amount" < 5;