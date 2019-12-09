from django.db import models

class Stock_Table(models.Model):
    Date = models.TextField()
    Stock_Name1 = models.CharField(max_length=50)
    Stock_Name2 = models.CharField(max_length=50)
    Signal = models.TextField()

    def __str__(self):
        return self.Date

class  Kosdaq_StockName(models.Model):
    stock_name =models.CharField(max_length=50)
    stock_code=models.CharField(max_length=50)

    def __str__(self):
        return self.stock_name

class  Kospi_StockName(models.Model):
    stock_name =models.CharField(max_length=50)
    stock_code=models.CharField(max_length=50)

    def __str__(self):
        return self.stock_name


class Target_StockName(models.Model):
    stock_name = models.CharField(max_length=50)

    def __str__(self):
        return self.stock_name




class  Stock_Pair_Trade(models.Model):
    Date = models.CharField(max_length=20)
    Base_stock = models.CharField(max_length=20)
    Pair_stock = models.CharField(max_length=20)
    Cash_Balance = models.IntegerField(default=0)
    Count1 = models.IntegerField(default=0)
    Count2 = models.IntegerField(default=0)
    Avg_price1 = models.IntegerField(default=0)
    Avg_price2 = models.IntegerField(default=0)
    def __str__(self):
        return self.Pair_stock
# Create your models here.
