CREATE TABLE `users` (
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
