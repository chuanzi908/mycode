DROP TABLE IF EXISTS `emp_customer`;
CREATE TABLE `emp_customer` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `emp_id` int(11) NOT NULL,
    `customer_id` int(11) NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_emp_id` (`emp_id`),
    KEY `idx_customer_id` (`customer_id`),
    CONSTRAINT `fk_ec_emp` FOREIGN KEY (`emp_id`) REFERENCES `emp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_ec_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `emp_customer` (`emp_id`, `customer_id`) VALUES
    (1, 1), (1, 3), (1, 7),
    (2, 1), (2, 2), (2, 5),
    (3, 4), (3, 6),
    (4, 3), (4, 8), (4, 10),
    (5, 2), (5, 9),
    (6, 1), (6, 5), (6, 7),
    (7, 4), (7, 6), (7, 8),
    (8, 3), (8, 9), (8, 10),
    (9, 1), (9, 2), (9, 4),
    (10, 5), (10, 7), (10, 8);