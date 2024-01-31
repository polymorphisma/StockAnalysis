from rest_framework import serializers
from .models import TestDatabase, StockData, StockSignal


class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['id', 'date', 'ticker', 'open', 'high', 'low', 'close', 'volume', 'value', 'stock_id']

class StockSignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockSignal
        fields = ['id', 'ticker', 'stochrsi', 'sma', 'rsi', 'momentum', 'macd', 'ema', 'boolinger', 'updated_date', 'sector_id']