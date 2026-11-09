CREATE TABLE 借阅 (
    证件号 CHAR(10) NOT NULL,
    图书编号 CHAR(13) NOT NULL,
    借阅日期 DATE NOT NULL,
    应还日期 DATE NOT NULL,
    归还日期 DATE,
    罚款金 MONEY NOT NULL DEFAULT 0.0 CHECK (罚款金 >= 0.0),
    CONSTRAINT Book_Borrow_pkzjsh PRIMARY KEY (证件号, 图书编号, 借阅日期),
    CONSTRAINT Book_Borrow_fkzjh FOREIGN KEY (证件号) REFERENCES 读者 (证件号),
    CONSTRAINT Book_Borrow_fktsbh FOREIGN KEY (图书编号) REFERENCES 图书 (图书编号)
);