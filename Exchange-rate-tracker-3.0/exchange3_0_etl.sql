create database exchange3_0_data;
use exchange3_0_data;

create table exchange3_rates(
	id int auto_increment primary key,
    base_currency varchar(10),
    target_currency varchar(10),
    rate decimal(10,4),
    percent_change decimal(10,4),
    date_collected datetime
);