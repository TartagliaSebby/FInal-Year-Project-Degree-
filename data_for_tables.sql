#customer table
insert into customer values(921941, "jeff goldman", "Klang", "Jalan Batu", "24121");
insert into customer values(901483, "Beau Davenport", "BBK", "Jalan ja", "291033");
insert into customer values(906719, "Odessa Vincent", "bukit tinggi", "jalan jalan", "291042");
insert into customer values(993664, "Odessa Crusa", "Bukit jalan", "jalan Bukit", "201834");
insert into customer values(971433, "Marne King", "taman merah", "red street","212041");
insert into customer values(901857, "Henning Hemminway", "tanah batu", "Green street", "21103");
insert into customer values(982114, "Hailey Snow", "Taman Fanir", "jalan kasawari", "23941");
insert into customer values(901284, "Harvey White", "taman Jaur", "jalan Hari", "281292");
insert into customer values(983210, "Tan Chin Long", "Taman Tinggi","Jalan putih","281421");

#seller table
insert into seller values(223531, 'Golden Gate');
insert into seller values(236324, "Baals Electronics");
insert into seller values(202317, 'Dell');
insert into seller values(219421, 'franik');
insert into seller values(200012, 'Mornarchy of Gamers');
insert into seller values(212232, 'Stores of stores');
insert into seller values(209123, "Ash's store");
insert into seller values(201742, "Desmonds Arts Supply");


#item table
insert into item values(104921, 223531, 'model train', 'large train model with bridge', 300);
insert into item values(102312, 223531, 'train painters set', 'brushes and paint for painting models', 100);
insert into item values(107832, 236324, 'edmodo toy kit', 'electronic kit to teach children about electronics', 250);
insert into item values(102352, 202317, 'dell latitude 256GB i5', '2020 dell latitude', 750);
insert into item values(192472, 219421, 'hair pin small', '',3);
insert into item values(128420, 219421, 'hair band large', '', 5);
insert into item values(102943, 236324, 'led multicoloured', '', 5);
insert into item values(183913, 200012, 'MOG zephyr 256GB','2022 MOG zehpyr gaming laptop', 700);
insert into item values(112321, 201742, 'Red pastel paint', 'red coloured pastel paint', 10);
insert into item values(123432, 201742, 'faber paint brush', 'big paint brush', 5);
insert into item values(128492, 201742, '40x40 cm canvas white', "medium sized white canvas", 50);

#order table
insert into orders values(712312, 921941, "pending", '2022-08-12');
insert into orders values(789210, 921941, "delivered",'2021-12-12');
insert into orders values(700120, 901483,"pending", '2021-12-12');
insert into orders values(701293, 906719, "delivered", '2021-12-19');
insert into orders values(792132,906719, "pending", '2022-3-10');
insert into orders values(766621, 993664, "pending", '2022-3-8');
insert into orders values(766666, 971433, "delivered", '2021-12-25');
INSERT INTO orders VALUES( 768169,901284,"pending", '2022-11-1');
INSERT INTO orders VALUES( 756810,982114,"pending", '2022-11-1');
INSERT INTO orders VALUES( 777564,901857,"pending", '2022-10-31');
INSERT INTO orders VALUES( 788699,921941,"pending", '2022-10-27');
INSERT INTO orders VALUES( 741786,921941,"pending", '2022-9-18');
INSERT INTO orders VALUES( 751985,901284,"pending", '2022-10-21');
INSERT INTO orders VALUES( 774337,971433,"pending", '2022-11-5');
INSERT INTO orders VALUES( 710553,901284,"pending", '2022-11-1');
INSERT INTO orders VALUES( 776634, 901857,"pending", '2022-10-19');


#order_item table
insert into order_item values(712312, 104921, 1);
insert into order_item values(789210, 104921, 1);
insert into order_item values(700120, 107832, 2);
insert into order_item values(700120, 102943, 5);
insert into order_item values(701293, 107832, 2);
insert into order_item values(792132, 102352, 2);
insert into order_item values(766621, 183913, 1);
insert into order_item values(766666,192472, 1);
insert into order_item values(766666, 128420, 5);
insert into order_item values( 741786,192472,1);
insert into order_item values( 756810,102943,3);
insert into order_item values( 756810,102943,2);
insert into order_item values( 774337,107832,5);
insert into order_item values( 741786,112321,1);
insert into order_item values( 768169,183913,2);
insert into order_item values( 751985,128420,1);
insert into order_item values( 776634,192472,1);
insert into order_item values( 756810,112321,3);
insert into order_item values(710553,192472,2);
insert into order_item values(777564,107832,1);
insert into order_item values(788699,123432,1);



#delivery table 
insert into delivery values(300213,712312,'2022-08-13','10:00','VPP3642');
insert into delivery values(332012,789210,'2021-12-13','10:00','USQ2039');
insert into delivery values(340231,700120,'2021-12-14','10:00','VPP3642');
insert into delivery values(301953,701293,'2021-12-20','10:00','VWQ3332');
insert into delivery values(366812,792132,'2022-3-12','10:00','PWO3401');
insert into delivery values(309172,766621,'2022-3-10','10:00','VPP3642');
insert into delivery values(301292,766666, '2021,12-30','10:00','VPP3642');


#ASN table 
insert into asn values(400210, 236324,'2021-12-30','06:15:00','courier','Received', "VVV1023");
insert into asn values(458123, 219421,'2022-1-30','17:00','self', "Received", "VJP8821");
insert into asn values(499921, 202317,'2022-2-12','10:30','self','Received',"JQY2363");
insert into asn values(444212,200012,'2022-1-21', '12:00', 'courier', "Received", "JTE7218");
insert into asn values(450512, 223531,'2022-10-14', "13:00",'self', "pending", "PQT2945");
insert into asn values(427492, 200012,'2022-11-1', "13:00",'self', "pending", "JTE7218");
insert into asn values(491732, 202317,'2022-11-2', "13:00",'self', "pending", "JQY2363");

#ASN_item table
insert into asn_items values(400210,107832,5);
insert into asn_items values(458123,192472,20);
insert into asn_items values(458123,128420,20);
insert into asn_items values(499921,102352,5);
insert into asn_items values(444212,183913,3);
insert into asn_items values(450512,104921,3);
insert into asn_items values(491732,104921,3);

#item_location table 
insert into item_location values('03-C-2-L2-2', 104921, 4);
insert into item_location values('04-C-7-L1-1', 104921, 2);
insert into item_location values('04-C-7-L1-2', 102312, 2);
insert into item_location values('01-A-4-L3-3', 107832, 6);
insert into item_location values('04-D-6-L1-3', 102352, 3);
insert into item_location values("01-A-1-L2-1",123432,5);
insert into item_location values("04-C-5-L3-2",107832,8);
insert into item_location values("01-A-5-L3-3",183913,6);
insert into item_location values("03-B-6-L3-1",183913,14);
insert into item_location values("03-B-5-L2-3",102352,13);
insert into item_location values("04-D-2-L2-1",104921,17);
insert into item_location values("01-A-3-L2-1",102943,11);
insert into item_location values("04-C-3-L2-1",192472,14);
insert into item_location values("02-D-6-L1-3",104921,19);
insert into item_location values("03-C-5-L1-1",102352,7);
insert into item_location values("01-A-6-L1-2",183913,5);
insert into item_location values("03-C-2-L1-1",192472,13);
insert into item_location values("03-C-2-L3-2",104921,13);
insert into item_location values("03-B-1-L2-2",107832,14);
insert into item_location values("04-D-3-L1-3",102352,19);
insert into item_location values("01-A-3-L1-1",102943,19);
insert into item_location values("04-D-7-L3-1",107832,17);
insert into item_location values("02-A-4-L3-2",128420,17);
insert into item_location values("04-C-1-L2-1",102312,12);
insert into item_location values("04-C-8-L1-2",107832,17);
insert into item_location values("03-B-4-L2-2",104921,15);
insert into item_location values("04-C-1-L3-3",102312,17);
insert into item_location values("02-A-5-L1-1",123432,18);
insert into item_location values("01-A-5-L3-2",107832,7);
insert into item_location values("02-A-8-L2-2",102943,15);
insert into item_location values("03-C-1-L3-1",107832,11);
insert into item_location values("02-A-3-L2-2",104921,14);
insert into item_location values("01-A-8-L1-3",102943,19);
insert into item_location values("01-A-5-L1-1",112321,19);
insert into item_location values("03-B-2-L2-1",112321,9);
insert into item_location values("02-A-3-L2-1",112321,6);
insert into item_location values("03-D-2-L2-1",128420,18);
insert into item_location values("02-B-3-L2-1",128420,10);

#receive_discrepancy table 
insert into receive_discrepancies values(458123, 192472,"missing 2 units", 20, 18,0);
insert into receive_discrepancies values(444212,183913, "torn up box and scratches on laptop", 3, 2, 1);
insert into receive_discrepancies values(450512,104921, "missing 1 set", 3, 2, 0);
#employee table
insert into employee values(8888, "Nathan Drake", "Nathan@gmail.com", "012-2837492","manager","1234",0);
insert into employee values(8001,"Jeffery Beverly", "Jeff@gmail.com", "017-2931253","worker","1234",0);
insert into employee values(8002,"Mark Rick", "Mark@gmail.com", "019-0219423","worker","asdf",1);
insert into employee values(8003,"Ellen Harvey", "eeH@@gmail.com", "012-1230944","worker","asd",1);
insert into employee values(8004, "Lee Chai Yen", "ChaiYuan@gmail.com", "016-9843275","worker","asdf",1);
insert into employee values(8005,"Tan Hong Kai", "Hong@gmail.com", "018-9832940","worker","asdf",1);
insert into employee values(8006,"Kumar radesh", "Kumar@gmail.com","014-5741923","worker","asdf",1);
insert into employee values(8007, "Kevin Space","Kevin@gmail.com","018,8829021","worker","asdf",1);
insert into employee values(8008,"Shawn Kevin","shawn@gmail.com", "015-2430187","worker","asdf",1);
insert into employee values(8009,"John Nathan","John@gmail.com", '012-2345587',"worker","asdf",1);


#instruction table
insert into instructions values(8001, "", "receiving", "Dock 1");
#assigned_orders table 

#picklist table


#shift table 

select distinct e.item_id, SUM(e.quantity) from item_location e right outer join item i on e.item_id = i.item_id group by item_id;


INSERT INTO pick_list VALUES(8008,"{'0': "{'item_id': 107832, 'location': '01-A-5-L3-2', 'quantity': 2}"}")