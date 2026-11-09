DROP TABLE IF EXISTS `customer_product`;
CREATE TABLE `customer_product` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `customer_id` int(11) NOT NULL,
    `product_id` int(11) NOT NULL,
    `quantity` int(11) NOT NULL DEFAULT 1,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_customer_id` (`customer_id`),
    KEY `idx_product_id` (`product_id`),
    CONSTRAINT `fk_cp_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_cp_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `customer_product` (`customer_id`, `product_id`, `quantity`) VALUES
    (1, 1, 1), (1, 2, 2), (1, 4, 3),
    (2, 5, 1), (2, 8, 2),
    (3, 1, 2), (3, 6, 1), (3, 10, 1),
    (4, 3, 1), (4, 4, 2), (4, 9, 1),
    (5, 2, 1), (5, 7, 1),
    (6, 5, 2), (6, 8, 3), (6, 10, 2),
    (7, 1, 1), (7, 6, 1), (7, 9, 2),
    (8, 3, 2), (8, 4, 1),
    (9, 2, 1), (9, 7, 2), (9, 8, 1),
    (10, 5, 1), (10, 10, 2), (10, 9, 1);