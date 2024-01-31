from django.db import models

class TestDatabase(models.Model):
    id = models.CharField(primary_key  = True)
    user = models.CharField(max_length = 100)

class SectorDetail(models.Model):
    id = models.IntegerField(primary_key = True)
    sector_symbol = models.CharField(max_length = 100)
    sector_name = models.TextField()

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['id', 'sector_symbol'], name='Uniqe Sector Detail')
    ]

class StockDetail(models.Model):
    id = models.IntegerField(primary_key = True)
    ticker = models.CharField(max_length = 100)
    company_name = models.TextField()
    email = models.TextField()
    listing_date = models.DateField()
    regulatory_body = models.DateField()
    total_listed_shares = models.FloatField()
    face_value = models.FloatField()
    address = models.TextField()
    active = models.BooleanField()
    sector_id = models.ForeignKey(SectorDetail, on_delete = models.SET_NULL,null =True)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['id', 'ticker'], name='Unique Stock detail')
    ]


class StockData(models.Model):
    id = models.AutoField(primary_key = True)
    date = models.DateField()
    ticker = models.CharField(max_length = 50)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    value = models.FloatField()
    stock_id = models.ForeignKey(StockDetail, on_delete = models.SET_NULL, null=True)


    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['id', 'ticker', 'date'], name='Unique Stock data')
    ]



class SectorData(models.Model):
    id = models.AutoField(primary_key = True)
    date = models.DateField()
    ticker = models.CharField(max_length = 50)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    value = models.FloatField()

    sector_id = models.ForeignKey(SectorDetail, on_delete = models.SET_NULL, null=True)


    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['id', 'ticker', 'date'], name='Unique Sector data')
    ]


class StockSignal(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length = 20)
    stochrsi = models.CharField(max_length= 10)
    sma = models.CharField(max_length= 10)
    rsi = models.CharField(max_length= 10)
    momentum = models.CharField(max_length= 10)
    macd = models.CharField(max_length= 10)
    ema = models.CharField(max_length= 10)
    boolinger = models.CharField(max_length= 10)
    updated_date = models.DateField()

    sector_id = models.ForeignKey(SectorDetail, on_delete = models.SET_NULL, null=True)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['id', 'ticker', 'stochrsi','sma', 'rsi', 'momentum', 'macd', 'ema', 'boolinger', 'updated_date'], name='Unique stock signals')
    ]
