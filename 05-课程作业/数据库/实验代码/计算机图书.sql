create view 计算机图书
as
select 图书.*,图书类型.图书分类名称
from 图书,图书类型
where 图书.图书分类号=图书类型.图书分类号
     and 图书类型.图书分类名称 like '计算机%'
