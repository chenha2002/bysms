from django.db import models

import datetime
class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=200)

    # 联系电话
    phonenumber = models.CharField(max_length=200)

    # 地址
    address = models.CharField(max_length=200)

class Medicine(models.Model):
    # 药品名
    name = models.CharField(max_length=200)
    # 药品编号
    sn = models.CharField(max_length=200)
    # 描述
    desc = models.CharField(max_length=200)


class Order(models.Model):
    # 订单名
    name = models.CharField(max_length=200,null=True,blank=True)

    # 创建日期
    create_date = models.DateTimeField(default=datetime.datetime.now)

    # 客户
    # Protect: 保护性删除，即如果有外键指向该对象，则不允许删除
    # CASCADE: 级联删除，即如果有外键指向该对象，则同时删除该对象
    # SET_NULL: 设置为空，即如果有外键指向该对象，则将该外键设置为null
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

    # 订单购买的药品，和Medicine表是多对多的关系
    # through参数指定中间表的名称
    medicines = models.ManyToManyField(Medicine, through='OrderMedicine')

class OrderMedicine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)

    # 订单中药品的数量
    amount = models.PositiveIntegerField()

from django.contrib import admin
admin.site.register(Customer)
