from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from static_content.serializers import *

class PrivacyPolicyView(APIView):
    def get(self,request):
        try:
            privacyInstance=PrivacyPolicy.objects.all().last()
            serializer=PrivacyPolicySerializers(privacyInstance)
            return Response(serializer.data)
        except Exception as e:
            print("Exception",e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class TermsAndConditionsView(APIView):
    def get(self,request):
        privacyInstance=TermsAndConditions.objects.all().last()
        serializer=TermsAndConditionsSerializers(privacyInstance)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        print("Ip",ip)
        return Response(serializer.data)

class AboutUsView(APIView):
    def get(self,request):
        privacyInstance=PrivacyPolicy.objects.all().last()
        serializer=PrivacyPolicySerializers(privacyInstance)
        return Response(serializer.data)

class CareerView(APIView):
    def post(self,request):
        params = request.data
        serializer = CareerSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status = status.HTTP_200_OK)