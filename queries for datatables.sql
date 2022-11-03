-- manager side order page table 1
SELECT o.order_id, c.name as "Customer Name", SUM(oi.quantity) as "num of items", order_status, placed_date 
FROM orders o, customer c, order_item oi 
where o.order_id = oi.order_id 
AND o.customer_id = c.customer_id
AND o.order_status != "delivered"
Group BY order_id;

--manager side order page overlayn table
SELECT item.item_id, item.item_name, seller.seller_id, order_item.quantity
FROM item, seller, order_item
WHERE item.item_id = order_item.item_id
AND item.seller_id = seller.seller_id
AND order_item.order_id = ord_id;

--inventory page main table 
SELECT i.item_id, i.item_name, s.seller_id, sum(il.quantity)
FROM item i, seller s, item_location il
WHERE i.item_id = il.item_id
AND i.seller_id = s.seller_id
GROUP BY i.item_id;

--inventory page overlay data
SELECT i.item_id, s.seller_id, i.weight, i.item_desc
FROM item i , seller s
WHERE i.seller_id = s.seller_id;

--inbound shipment page main table
SELECT a.asn_id,  s.seller_name, a.shipment_type, a.arrival_date, a.arrival_time, a.asn_status
FROM asn a,seller s
WHERE a.seller_id = s.seller_id;

--invbound page overlay table
SELECT ai.item_id, i.item_name, i.item_desc, ai.quantity
FROM asn_items ai, item i
WHERE ai.item_id = i.item_id
AND ai.asn_id =458123 ;

--receive discrepancy page main table
SELECT a.asn_id, s.seller_id, s.seller_name, a.shipment_type, a.arrival_date,a.arrival_time
FROM asn a, seller s,
WHERE a.seller_id = s.seller_id

--delivery page main table
SELECT o.order_id, d.delivery_id, d.vehicle_id
FROM orders o, delivery d
WHERE o.order_id = d.order_id

--delivery page sub table 1

--delivery page sub table 2
SELECT delivery.order_id, customer.name, delivery.vehicle_num
FROM delivery, customer, orders
WHERE delivery.order_id = orders.order_id
AND customer.customer_id = orders.customer_id

--table for job assignment page 
SELECT e.emp_id, e.name, i.task, i.station
FROM employee e, instructions i 
WHERE e.emp_id =i.emp_id
and e.emp_id in (SELECT emp_id FROM employee WHERE present = 1);

--job assignment page table
SELECT e.emp_id, e.name, i.task, i.station
FROM employee e
LEFT OUTER JOIN instructions i ON e.emp_id = i.emp_id
ORDER BY e.emp_id;

--pick pack assignment pending order table
SELECT o.order_id, SUM(oi.quantity) as items, placed_date
FROM orders o, order_item oi
WHERE o.order_id = oi.order_id
AND o.order_status = 'pending'
Group BY o.order_id;

--pick pack assignment available employees
SELECT e.emp_id, e.name, i.task, i.station
FROM employee e, instruction i
WHERE e.emp_id = i.emp_id

SELECT e.emp_id, e.name, i.task, i.station
FROM employee e
LEFT OUTER JOIN instruction i ON e.emp_id = i.emp_id
WHERE e.present = 1;

--data for genetic algorithm
--!for object creator
--order
SELECT order_id, item_id, quantity
FROM order_item
WHERE order_id IN ({})
ORDER BY order_id;

--inventory before becoming a dictionary
SELECT item_id, location, quantity
FROM order_item oi, item_location il
WHERE oi.item_id = il.item_id
AND oi.order_id IN ({})



/*
SELECT oi.order_id, oi.item_id, il.location FROM order_item oi, item_location il WHERE oi.item_id = il.item_id AND oi.item_id in(SELECT DISTINCT il.item_id FROM FROM order_item oi, item_location il WHERE oi.item_id = il.item_id AND oi.order_id in(712312 ,789210)) ORDER BY oi.order_id;
query = "SELECT oi.order_id, oi.item_id, il.location FROM order_item oi, item_location il WHERE oi.item_id = il.item_id AND oi.item_id in(SELECT DISTINCT il.item_id FROM FROM order_item oi, item_location il WHERE oi.item_id = il.item_id AND oi.order_id in({})) ORDER BY oi.order_id;".format(ord_ids)
query = """SELECT oi.order_id, oi.item_id, il.location 
        FROM order_item oi, item_location il 
        WHERE oi.item_id = il.item_id 
        AND oi.item_id in(
            SELECT DISTINCT il.item_id FROM FROM order_item oi, item_location il WHERE oi.item_id = il.item_id AND oi.order_id in({})) ORDER BY oi.order_id;""".format(ord_ids)
*/




-- query to see if there is sufficient quantity of items
--query for the quantity of items available 
SELECT il.item_id, SUM(il.quantity) AS inv_quantity
FROM item_location il
WHERE il.item_id IN(102943,107832 )
GROUP BY il.item_id
ORDER BY il.item_id



--query for the quantity of items needed to fulfil orders


SELECT ord.item_id,  ord_quantity, inv_quantity
FROM (
    SELECT il.item_id, SUM(il.quantity) AS inv_quantity
    FROM item_location il
    WHERE item_id IN(
        SELECT item_id 
        FROM order_item
        WHERE order_id IN (700120)
    )
    GROUP BY il.item_id
    ORDER BY il.item_id
) inv RIGHT OUTER JOIN (
    SELECT oi.item_id, SUM(oi.quantity) AS ord_quantity
    FROM order_item oi, orders o
    WHERE oi.order_id = o.order_id
    AND oi.order_id IN(700120)
    GROUP BY oi.item_id
    ORDER BY oi.item_id
) ord
ON ord.item_id = inv.item_id;
insert into picking_parameters values(1, '{"ids":"1234,4321"}' , '{"emp":"5678,8765"}')

#inventory loction for script
SELECT il.location, il.quantity
FROM item_location il, orders_items oi
WHERE 

SELECT il.item_id, il.quantity , location
FROM item_location il
WHERE item_id IN(
    SELECT item_id 
    FROM order_item
    WHERE order_id IN (700120)
)
ORDER BY il.item_id



#---- employees----

#instrcutions table
SELECT task, station
FROM instruction
where emp_id ={}

#receive page table 1
SELECT arrival_time, vehicle_no, asn_status
FROM asn 
where DATE(arrival_date) = curdate()

SELECT arrival_time, vehicle_no, asn_status FROM asn  where DATE(arrival_date) = curdate()

#table 2
SELECT ai.item_id, i.item_name, i.item_desc, ai.quantity
FROM asn_items ai, item i
WHERE ai.item_id = i.item_id
AND asn_id = {}

SELECT ai.item_id, i.item_name, i.item_desc, ai.quantity FROM asn_items ai, item i WHERE ai.item_id = i.item_id AND asn_id = {}

#receive pag table 3(discrepancy report)
SELECT ai.item_id, i.item_name, ai.quantity
FROM asn_items ai, item i
WHERE ai.item_id = i.item_id
AND asn_id = 458123 {}

SELECT ai.item_id, i.item_name, ai.quantity FROM asn_items ai, item i WHERE ai.item_id = i.item_id AND asn_id = {}

#received items
SELECT item_id  FROM item_location WHERE item_id IN (SELECT item_id from asn_items WHERE asn_id = {}


select ai.item_id, il.location, ai.quantity 
from asn_items ai, item_location il 
WHERE ai.item_id = il.item_id 
AND ai.asn_id = '491732'{}



select item_id, quantity 
from asn_items
WHERE item_id Not IN (
    select ai.item_id from asn_items ai, item_location il where ai.item_id = il.item_id AND asn_id = '491732'
)AND asn_id = '491732'

select item_id, quantity from asn_items WHERE item_id Not IN ( select ai.item_id from asn_items ai, item_location il where ai.item_id = il.item_id AND asn_id = '491732')AND asn_id = '491732'

--put away tables
select ri.item_id, i.item_name, ri.location 
from received_items ri, item i
where ri.item_id = i.item_id

