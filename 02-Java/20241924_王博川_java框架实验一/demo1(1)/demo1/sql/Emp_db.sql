DROP TABLE IF EXISTS `emp`;
CREATE TABLE `emp` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `age` int(11) NOT NULL,
    `dept` varchar(255) NOT NULL,
    `salary` decimal(10,2) NOT NULL,
    `hire_date` date NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `emp` (`name`, `age`, `dept`, `salary`, `hire_date`) VALUES
    ('张三', 28, '技术部', 8500.00, '2020-05-12'),
    ('李四', 32, '技术部', 12000.00, '2018-03-08'),
    ('王五', 25, '市场部', 6500.00, '2022-07-01'),
    ('赵六', 35, '财务部', 9800.00, '2017-11-20'),
    ('孙七', 29, '人事部', 7200.00, '2021-01-15'),
    ('周八', 41, '技术部', 15000.00, '2015-09-01'),
    ('吴九', 27, '市场部', 6800.00, '2022-04-10'),
    ('郑十', 33, '财务部', 10500.00, '2019-06-25'),
    ('钱十一', 26, '技术部', 7800.00, '2021-09-18'),
    ('陈十二', 30, '人事部', 7000.00, '2020-12-01');