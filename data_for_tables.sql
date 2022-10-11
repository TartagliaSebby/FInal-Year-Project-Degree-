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
insert into seller values(212232, 'Stores of stores');
insert into seller values(209123, "Ash's store");


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
insert into delivery values(300213,712312,'2022-08-13','10:00','VPP3642');
insert into delivery values(332012,789210,'2021-12-13','10:00','USQ2039');
insert into delivery values(340231,700120,'2021-12-14','10:00','VPP3642');
insert into delivery values(301953,701293,'2021-12-20','10:00','VWQ3332');
insert into delivery values(366812,792132,'2022-3-12','10:00','PWO3401');
insert into delivery values(309172,766621,'2022-3-10','10:00','VPP3642');
insert into delivery values(301292,766666, '2021,12-30','10:00','VPP3642');


--ASN table 
insert into asn values(400210, 236324,'2021-12-30','06:15:00','courier','Received', "VVV1023");
insert into asn values(458123, 219421,'2022-1-30','17:00','self', "Received", "VJP8821");
insert into asn values(499921, 202317,'2022-2-12','10:30','self','Received',"JQY2363");
insert into asn values(444212,200012,'2022-1-21', '12:00', 'courier', "Received", "JTE7218");
insert into asn values(450512, 223531,'2022-10-14', "13:00",'self', "pending", "PQT2945");

--ASN_item table
insert into asn_items values(400210,107832,5);
insert into asn_items values(458123,192472,20);
insert into asn_items values(458123,128420,20);
insert into asn_items values(499921,102352,5);
insert into asn_items values(444212,183913,3);
insert into asn_items values(450512,104921,3);

--item_location table 
insert into item_location values('03-C-2-L2-2', 104921, 4);
insert into item_location values('04-C-7-L1-1', 104921, 2);
insert into item_location values('04-C-7-L1-2', 102312, 2);
insert into item_location values('01-A-4-L3-3', 107832, 6);
insert into item_location values('04-D-6-L1-3', 102352, 3);
--receive_discrepancy table 
insert into receive_discrepancies values(458123, 192472,"missing 2 units", 20, 18,0);
insert into receive_discrepancies values(444212,183913, "torn up box and scratches on laptop", 3, 2, 1);
insert into receive_discrepancies values(450512,104921, "missing 1 set", 3, 2, 0);
--employee table

--instruction table

--assigned_orders table 

--picklist table


--shift table 

