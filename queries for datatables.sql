-- manager side order page table 1
SELECT o.order_id, c.name as "Customer Name", SUM(oi.quantity) as "num of items", order_status, placed_date 
FROM orders o, customer c, order_item oi 
where o.order_id = oi.order_id 
AND o.customer_id = c.customer_id
AND o.order_status != "delivered"
Group BY placed_date;

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