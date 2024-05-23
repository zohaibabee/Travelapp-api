from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category,Destination,Destination_detail,BookNow
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializer import Destination_detailserializer,Destinationserializer,Categoryserializer,Searchserializer,Bookingserializer
# Create your views here



class Homepage(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, category=None):
        if category:
            destinations = Destination.objects.filter(category__name__icontains=category)
        else:
            destinations = Destination.objects.all()

        serializer = Destinationserializer(destinations, many=True)
        return Response(serializer.data)

class PopularDestination(APIView):
    def get(self, request):
        permission_classes=[IsAuthenticated]
        destinations = Destination.objects.filter(popular=True)
        serializer = Destinationserializer(destinations, many=True)
        return Response(serializer.data)
    
    
class Destinationdetail(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        dest=Destination_detail.objects.get(id=id)
        serializer=Destination_detailserializer(dest)
        return Response(serializer.data)
    
    
class Search(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = Searchserializer(data=request.data)
        if serializer.is_valid():
            search_query = serializer.validated_data.get('search', '')
            if search_query:
                destinations = Destination.objects.filter(category__name__icontains=search_query)
            else:
                destinations = Destination.objects.all()
            result_serializer = Destinationserializer(destinations, many=True)
            return Response(result_serializer.data)
        else:
            return Response(serializer.errors)
        
        
# class Searchable(APIView):
#     def get(self,request):
#         search=request.query_params.get('search','')
#         if search:
#             dest=Destination.objects.filter(category__name__icontains=search)
#         else:
#             dest=Destination.objects.all()
#         serializer=Destinationserializer(dest,many=True)
#         return Response(serializer.data)
    
        
        
class Categoryview(APIView):
    def get(self,request):
        queryset=Category.objects.all()
        serializer=Categoryserializer(queryset,many=True)
        return Response(serializer.data)
    # def post(self,request):
    #     queryset=Category.objects.all()
    #     serializer=Categoryserializer(data=request.data)
    #     if serializer.is_valid():
    #         return Response({'msg':'data created'})
    #     return Response(serializer.errors)
    

    

# class Booknow(APIView):
#     permission_classes=[IsAuthenticated]
#     def post(self,request,id):
#         dest=Destination.objects.get(id=id)
#         user=request.user.email
#         serializer=Bookingserializer(data=request.data,context={'dest':dest,'user':user})
#         if serializer.is_valid():
#             return Response({'msg':'Hello'})

class Booknow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        dest = Destination.objects.get(id=id)
        print(dest)
        # booking_exsist=BookNow.objects.filter(destination=dest).exists()
        # if booking_exsist:
        #     return Response({'msg':'You already  book this destination'})
        booking_exsist=BookNow.objects.filter(user=request.user).exists()
        if booking_exsist:
            return Response({'msg':'You have already booked destination.'}) 
        serializer = Bookingserializer(data=request.data, context={'destination': dest, 'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Booking successful'})
        
        return Response(serializer.errors)
    
class Bookdetail(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        booked_destination=BookNow.objects.get(user=request.user)
        serializer=Bookingserializer(booked_destination)
        return Response(serializer.data)
    
class Checkout(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        booked_destination=BookNow.objects.get(user=request.user)
        if not booked_destination:
            return Response({'msg':"No booking found"})
        per_person_price=booked_destination.destination.price_per_person
        service_fees=400
        total_person=booked_destination.adults+booked_destination.child+booked_destination.kids
        amount=total_person*per_person_price
        total_amount=amount+service_fees
        print(total_amount)
        return Response({'data':{
            'Rental Price':amount,
            'Service Fees':service_fees,
            'Total Amount':total_amount
        }})
