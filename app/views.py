from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.shortcuts import render, redirect
from django.db.models import Max
from django.http import JsonResponse


from .models import StockData, StockSignal
from .serializers import StockDataSerializer, StockSignalSerializer


class StockView(APIView):
    def get(self, request):
        ticker = request.GET.get('ticker', None)

        ticker = ticker.upper()
        
        if not ticker:
            return Response({'error': 'Ticker parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            stock_data = StockData.objects.filter(ticker=ticker).order_by('-date')[:100]
            serializer = StockDataSerializer(stock_data, many=True)


            return Response(serializer.data)
        except StockData.DoesNotExist:
            return Response({'error': 'Stock data for this ticker does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HomeView(APIView):
    def get(self, request):
        latest_updated_date = StockSignal.objects.aggregate(Max('updated_date'))['updated_date__max']
        print(latest_updated_date)
        latest_signal = StockSignal.objects.filter(updated_date=latest_updated_date)
        serializer = StockSignalSerializer(latest_signal, many=True)
        print(serializer.data)
        return render(request, 'index.html', {'stock_signals': serializer.data, 'updated_date': latest_updated_date})
    
class CompanyView(APIView):
    def get(self, request):

        
        ticker = request.GET.get('key', None)
        ticker = ticker.upper()
        stock_signals = StockSignal.objects.filter(ticker=ticker)
        serializer = StockSignalSerializer(stock_signals, many=True)
        
        updated_date = StockSignal.objects.latest('updated_date').updated_date
        return render(request, 'company.html', {'stock_signals': serializer.data, 'updated_date': updated_date})

class StockSignalListView(APIView):
    def get(self, request):
        stock_signals = StockSignal.objects.all()
        serializer = StockSignalSerializer(stock_signals, many=True)
        return Response(serializer.data)

class StockSearch(APIView):
    def get(self, request):
        return render(request, 'search.html')

class StockSuggestions(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        suggestions = StockData.objects.filter(ticker__icontains=query).values_list('ticker', flat=True).distinct()[:5]
        return JsonResponse({'suggestions': list(suggestions)})
