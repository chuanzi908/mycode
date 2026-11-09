-- 商品表
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `price` decimal(10, 2) NOT NULL DEFAULT 0.00,
    `stock` int(11) NOT NULL DEFAULT 0,
    `category` varchar(100) NOT NULL DEFAULT '',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `product` (`name`, `price`, `stock`, `category`) VALUES
('华为Mate60', 5999.00, 100, '手机'),
('iPhone15', 7999.00, 80, '手机'),
('MacBook Pro', 14999.00, 30, '电脑'),
('ThinkPad X1', 9999.00, 25, '电脑'),
('AirPods Pro', 1899.00, 200, '耳机'),
('Sony WH-1000XM5', 2499.00, 60, '耳机'),
('iPad Air', 4799.00, 45, '平板'),
('小米平板6', 1999.00, 70, '平板'),
('华为手表GT4', 1488.00, 120, '穿戴'),
('Apple Watch S9', 2999.00, 90, '穿戴');

-- 员工表
DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `department` varchar(100) NOT NULL,
    `salary` decimal(10, 2) NOT NULL DEFAULT 0.00,
    `hire_date` date NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `employee` (`name`, `department`, `salary`, `hire_date`) VALUES
('张三', '技术部', 15000.00, '2022-03-15'),
('李四', '技术部', 18000.00, '2021-07-01'),
('王五', '市场部', 12000.00, '2023-01-10'),
('赵六', '市场部', 11000.00, '2022-09-20'),
('孙七', '人事部', 10000.00, '2023-06-05'),
('周八', '人事部', 9500.00, '2024-02-18'),
('吴九', '财务部', 13000.00, '2021-11-30'),
('郑十', '财务部', 14000.00, '2020-08-25'),
('钱一', '技术部', 22000.00, '2019-04-12'),
('陈二', '运营部', 10500.00, '2023-10-08');