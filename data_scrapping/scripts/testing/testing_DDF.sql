-- 2020-07-21
CREATE TABLE mebourne_housing(
    id serial,
    suburb character(100),
    rooms smallint,
    type character(2),
    price int,
    method character(2),
    sellerg character(100),
    date date,
    distance decimal(4,2),
    postcode character(4),
    bedrooms smallint,
    badrooms smallint,
    car smallint,
    landsize int,
    buildingarea int,
    yearbuild int,
    councilarea character(150),
    lattitude decimal(7,4),
    longtitude decimal(7,4),
    regionname character(150),
    propertycount int
);