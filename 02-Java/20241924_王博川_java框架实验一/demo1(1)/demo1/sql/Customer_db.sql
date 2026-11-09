DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `phone` varchar(50) NOT NULL,
    `email` varchar(255) DEFAULT NULL,
    `address` varchar(500) DEFAULT NULL,
    `level` varchar(50) NOT NULL DEFAULT '普通',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `customer` (`name`, `phone`, `email`, `address`, `level`) VALUES
    ('刘小明', '13800138001', 'liuxm@example.com', '北京市海淀区中关村大街1号', 'VIP'),
    ('王美丽', '13900139002', 'wangml@example.com', '上海市浦东新区陆家嘴环路100号', '普通'),
    ('陈大伟', '13700137003', 'chendw@example.com', '广州市天河区珠江新城', 'VIP'),
    ('杨丽娜', '13600136004', 'yangln@example.com', '深圳市南山区科技园', '高级'),
    ('赵国强', '13500135005', 'zhaogq@example.com', '杭州市西湖区文三路', '普通'),
    ('孙红梅', '13400134006', 'sunhm@example.com', '成都市高新区天府大道', '高级'),
    ('周建华', '13300133007', 'zhoujh@example.com', '南京市鼓楼区中山路', 'VIP'),
    ('吴小芳', '13200132008', 'wuxf@example.com', '武汉市洪山区珞瑜路', '普通'),
    ('郑志强', '13100131009', 'zhengzq@example.com', '西安市雁塔区高新路', '高级'),
    ('黄丽娟', '13000130010', 'huanglj@example.com', '厦门市思明区厦禾路', '普通');