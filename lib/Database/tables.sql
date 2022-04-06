# Database name: mojocms; Database Host: localhost; 
# Server: MySQL or MariaDB; Server Port: 3308;

CREATE TABLE if not exists `users` (
  `id` bigint(32) NOT NULL AUTO_INCREMENT,
  `username` varchar(49),
  `password` varchar(99),
  `email` varchar(99),
  `date_modified` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `date_registered` datetime NOT NULL DEFAULT current_timestamp,
  `firstname` varchar(99) ,
  `lastname` varchar(99),
  `city` varchar(99),
  `state` varchar(99),
  `country` varchar(99),
  primary key(`id`)
);
insert into users (username, password) values ('mojouser', 'mojopass220320');
update users set password=md5('mojopass220320') where password="mojopass220320";
update users set email="pcaccessfree@pcaf.a2z.blue", firstname="PCAF", lastname="PCAF", city="MyCity", state="MyState", country="MyCountry" where id="1";
update users set email="pcaf@pcaf.a2z.blue" where id="1";

create table if not exists profile (
  id bigint(32) auto_increment primary key not null,
  created timestamp default current_timestamp on update current_timestamp,
  username varchar(29) not null,
  firstname varchar(99) not null,
  lastname varchar(99) not null,
  email varchar(255) not null,
  description text not null
);
