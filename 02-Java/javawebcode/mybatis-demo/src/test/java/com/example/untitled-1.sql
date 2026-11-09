CREATE DATABASE mybatis_db DEFAULT CHARSET utf8;
USE mybatis_db;
CREATE TABLE user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50),
  password VARCHAR(50),
  email VARCHAR(100)
);
INSERT INTO user(username,password,email) VALUES('alice','123','a@x.com'),('bob','456','b@x.com');