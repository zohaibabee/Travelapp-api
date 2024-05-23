from .models import Category, Destination, Destination_detail,BookNow
from rest_framework import serializers
from .models import BookNow
class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"


class Destinationserializer(serializers.ModelSerializer):
    category=Categoryserializer()
    class Meta:
        model=Destination
        fields="__all__"
        
        

class Destination_detailserializer(serializers.ModelSerializer):
    destinationid=Destinationserializer()
    class Meta:
        model=Destination_detail
        fields="__all__"     
        
        
class Searchserializer(serializers.Serializer):
    search=serializers.CharField(max_length=255)
    
# class Bookingserializer(serializers.ModelSerializer):
#     Destination_detail=Destination_detailserializer()
#     class Meta:
#         model=BookNow
#         fields="__all__"
        
#     def validate(self, attrs):
#         user=self.context.get('user')
#         dest=self.request.get('dest')
#         adults=attrs.get('adults')
#         child=attrs.get('child')
#         kids=attrs.get('kids')
#         startdate=attrs.get('start_date')
#         enddate=attrs.get('end_date')
#         booking=BookNow(user=user,destination=dest,child=child,adults=adults,kids=kids,start_date=startdate,end_date=enddate)
#         booking.save()
#         return attrs

class Bookingserializer(serializers.ModelSerializer):
    class Meta:
        model = BookNow
        fields = ['child', 'adults', 'kids', 'start_date', 'end_date']
        extra_kwargs = {
            'user': {'required': False},
            'destination': {'required': False},
            'child': {'required': False},  # Make child optional
            'adults': {'required': False},  # Make adults optional
            'kids': {'required': False}  # Make kids optional
        }

    def create(self, validated_data):
        user = self.context['user']
        destination = self.context['destination']
        booking = BookNow.objects.create(user=user, destination=destination, **validated_data)
        return booking

        
        
        
        