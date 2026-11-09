-- ========== 供应商表 ==========
CREATE TABLE IF NOT EXISTS supplier (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ========== 给商品表加供应商外键 ==========
ALTER TABLE product ADD COLUMN supplier_id INT AFTER stock;
ALTER TABLE product ADD FOREIGN KEY (supplier_id) REFERENCES supplier(id);

-- ========== 插入供应商测试数据 ==========
INSERT INTO supplier (name, contact_person, phone, email, address) VALUES
('华为电子', '赵总', '13800001111', 'zhao@huawei.com', '深圳市龙岗区'),
('小米科技', '钱经理', '13800002222', 'qian@xiaomi.com', '北京市海淀区'),
('苹果配件', '孙总', '13800003333', 'sun@apple.com', '上海市浦东新区');

-- ========== 给已有商品分配供应商 ==========
UPDATE product SET supplier_id = 1 WHERE name LIKE '%手机%' OR name LIKE '%平板%';
UPDATE product SET supplier_id = 2 WHERE name LIKE '%手环%' OR name LIKE '%音箱%';
UPDATE product SET supplier_id = 3 WHERE name LIKE '%Mac%' OR name LIKE '%耳机%';
-- 剩余未分配的归给华为
UPDATE product SET supplier_id = 1 WHERE supplier_id IS NULL;