-- vehicles table
create table vehicles(vid int primary key,vehiclenumber varchar(10));

-- transactin table
create table transactions(tid int primary key,company varchar(100),vehicle int,source varchar(100),destination varchar(100),transaction_date date ,FOREIGN KEY(vehicle) REFERENCES vehicles(vid));