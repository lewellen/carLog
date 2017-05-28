create table drivers (
	id integer primary key asc not null,
	name varchar(256) not null
);

create table vehicles (
	id integer primary key asc not null,
	driverId integer not null,
	vin varchar(256) not null,
	make varchar(256) not null,
	model varchar(256) not null,
	year integer not null,
	stillOwn boolean not null,
	foreign key(driverId) references drivers(id)
);

create table providerTypes (
	id integer primary key asc not null,
	name varchar(256) not null
);

create table providers(
	id integer primary key asc not null,
	providerTypeId integer not null,
	name varchar(256) not null,
	address varchar(256) null,
	foreign key(providerTypeId) references providers(id)
);

create table destinations (
	id integer primary key asc not null,
	name varchar(256) not null
);

create table maintenanceEntries(
	id integer primary key asc not null,
	vehicleId integer not null,
	providerId integer not null,
	at date not null,
	primaryContact varchar(256) null,
	phoneNumber varchar(256) null,
	description varchar(256) not null,
	cost float not null default(0),
	foreign key(vehicleId) references vehicles(id),
	foreign key(providerId) references providers(id)
);

create table mileageEntries(
	id integer primary key asc not null,
	vehicleId integer not null,
	providerId integer not null,
	destinationId integer not null,
	fromDate date not null,
	toDate date not null,
	tripMileage float not null,
	odometer float not null,
	gallons float not null,
	pricePerGallon float not null,
	foreign key(vehicleId) references vehicles(id),
	foreign key(providerId) references providers(id),
	foreign key(destinationId) references destination(id)
);

create table eventEntries(
	id integer primary key asc not null,
	vehicleId integer not null,
	at date not null,
	odometer float null,
	description varchar(256) not null,
	foreign key(vehicleId) references vehicles(id)
);

insert into drivers (name) values ("Default");
insert into providerTypes (name) values ("Unknown");
insert into providers (providerTypeId, name) values (1, "Unknown");
insert into destinations (name) values ("Unknown");
