DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `price` decimal(10,2) NOT NULL,
    `stock` int(11) NOT NULL DEFAULT 0,
    `description` varchar(500) DEFAULT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `product` (`name`, `price`, `stock`, `description`) VALUES
    ('MacBook Pro 14寸', 14999.00, 50, 'Apple M3芯片，16GB内存，512GB SSD'),
    ('iPhone 15 Pro', 7999.00, 200, 'A17 Pro芯片，钛金属设计'),
    ('iPad Air', 4599.00, 120, 'M2芯片，10.9英寸Liquid Retina显示屏'),
    ('AirPods Pro 2', 1899.00, 300, '主动降噪，USB-C充电盒'),
    ('Apple Watch S9', 3199.00, 150, 'S9 SiP芯片，血氧监测'),
    ('Dell XPS 15', 12999.00, 40, 'Intel i7，32GB内存，1TB SSD'),
    ('ThinkPad X1 Carbon', 13999.00, 30, 'Intel i7，16GB内存，512GB SSD'),
    ('罗技MX Master 3S', 699.00, 500, '无线蓝牙鼠标，静音点击'),
    ('HHKB Professional 2', 2199.00, 80, '静电容键盘，60%布局'),
    ('4K显示器 27寸', 2999.00, 100, 'IPS面板，HDMI/DP接口');