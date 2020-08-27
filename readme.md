#Features
1) Add raw milk produced
url: http://0.0.0.0:8000/milk_produced
for post request
input format: {"milk":10}
Id get updated by default
Date added by default
Time added by default,
Stock get updated by default

fetch data using get request


2) processed goods
url: http://0.0.0.0:8000/processed_goods
for post requests
input format: {"product_id": 4,
    "quantity_produced": 555,
    "quantity_used": 460}
pg_id  updated automatically
date  updated automatically
time  updated automatically
stock_left  updated automatically

Get request to fetch data


INsert into tb_raw_milk ("raw_milk_farm_id","raw_milk_product_id","raw_milk_product_quantity","raw_milk_product_price","raw_milk_product_units") 
VALUES
('c45e8593-aa3a-4862-a102-cabf2762dd8f','1c14b02a-fe00-46c8-b4a7-47593d8079a3', 200, 17, 'LTR')

TRUNCATE tb_raw_milk;
TRUNCATE tb_raw_milk_price;
TRUNCATE tb_processed_goods;
TRUNCATE tb_processed_goods_price;
TRUNCATE tb_net_stock;

select * from tb_net_stock 
select * from tb_processed_goods
select * from tb_raw_milk ;

DELETE FROM tb_processed_goods  where pg_id ='db5e10a1-80df-4b84-92d7-0b0aff9c9a7f';

select * from tb_processed_goods_price
INSERT into tb_processed_goods ("pg_product_id", "pg_quantity_produced", "pg_quantity_used","pg_farm_id","pg_units","pg_milk_id","pg_price")
VALUES 
('1c14b03a-fe00-46c8-b4a7-47593d8079a3', 10 , 4, 'c45e8593-aa3a-4862-a102-cabf2762dd8f', 'KG', '1c14b02a-fe00-46c8-b4a7-47593d8079a3', 10.0)


