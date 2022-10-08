---customer table
insert into customer values(921941, "jeff goldman", "Klang", "Jalan Batu", "24121");
insert into customer values(901483, "Beau Davenport", "BBK", "Jalan ja", "291033");
insert into customer values(906719, "Odessa Vincent", "bukit tinggi", "jalan jalan", "291042");
insert into customer values(993664, "Odessa Crusa", "Bukit jalan", "jalan Bukit", "201834");
insert into customer values(971433, "Marne King", "taman merah", "red street","212041");
insert into customer values(901857, "Henning Hemminway", "tanah batu", "Green street", "21103");

--seller table
insert into seller values(223531, 'Golden Gate');
insert into seller values(236324, "Baals Electronics");
insert into seller values(202317, 'Dell');
insert into seller values(219421, 'franik');
insert into seller values(200012, 'Mornarchy of Gamers');


--item table
insert into item values(104921, 223531, 'model train', 'large train model with bridge', 300);
insert into item values(102312, 223531, 'train painters set', 'brushes and paint for painting models', 100);
insert into item values(107832, 236324, 'edmodo toy kit', 'electronic kit to teach children about electronics', 250);
insert into item values(102352, 202317, 'dell latitude 256GB i5', '2020 dell latitude', 750);
insert into item values(192472, 219421, 'hair pin small', '',3);
insert into item values(128420, 219421, 'hair band large', '', 5);
insert into item values(102943, 236324, 'led multicoloured', '', 5);
insert into item values(183913, 200012, 'MOG zephyr 256GB','2022 MOG zehpyr gaming laptop', 700);

--order table
insert into orders values(712312, 921941, "pending", '2022-08-12');
insert into orders values(789210, 921941, "delivered",'2021-12-12');
insert into orders values(700120, 901483,"pending", '2021-12-12');
insert into orders values(701293, 906719, "delivered", '2021-12-19');
insert into orders values(792132,906719, "pending", '2022-3-10');
insert into orders values(766621, 993664, "pending", '2022-3-8');
insert into orders values(766666, 971433, "delivered", '2021,12-25');


--order_item table
insert into order_item values(712312, 104921, 1);
insert into order_item values(789210, 104921, 1);
insert into order_item values(700120, 107832, 2);
insert into order_item values(700120, 102943, 5);
insert into order_item values(701293, 107832, 2);
insert into order_item values(792132, 102352, 2);
insert into order_item values(766621, 183913, 1);
insert into order_item values(766666,192472, 1);
insert into order_item values(766666, 128420, 5);



--delivery table 

--ASN table 

--ASN_item table

--item_location table 

--receive_discrepancy table 

--employee table

--instruction table

--assigned_orders table 

--picklist table


--shift table 

