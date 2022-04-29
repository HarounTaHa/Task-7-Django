from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import MemberUser
from .models import Plan, Vendor
from .serializers import PlanSerializer, VendorSerializer


class PlanDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Plan.objects.get(pk=pk)
        except Plan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        subscription = self.get_object(pk)
        serializer = PlanSerializer(subscription)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        plan = self.get_object(pk)
        print(plan)
        serializer = PlanSerializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorList(APIView, LimitOffsetPagination):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        vendors = Vendor.objects.all()

        result_page = self.paginate_queryset(vendors, request, view=self)

        serializer = VendorSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        if isinstance(request.data, list):
            for obj in request.data:
                serializers = VendorSerializer(data=obj)
                if serializers.is_valid():
                    serializers.save()
            return Response({'Status': 'Added List Of Objects'}, status=status.HTTP_200_OK)

        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_objects(self, mac):
        try:
            vendor = Vendor.objects.get(mac=mac)
            return vendor
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, mac, format=None):
        try:
            token_user = Token.objects.get(key=request.auth.key)
        except:
            return Response({'Message': 'The Token is not valid'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = MemberUser.objects.get(id=token_user.user.pk)
        # subscription = user.subscription_user.all()
        # print(subscription)
        try:
            subscription = Plan.objects.get(user=user.pk)
        except:
            return Response({'Message': 'The User is not register with any plan in SaaS'},
                            status=status.HTTP_400_BAD_REQUEST)
        print(subscription.limit)
        print(subscription.count)
        if subscription.limit != subscription.count:
            subscription.count += 1
            subscription.save()
            vendor = self.get_objects(mac)
            serializer = VendorSerializer(vendor)
            return Response({'count request': subscription.count, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'Message': 'you have reached your maximum limit please upgrade your subscription plan'},
                status=status.HTTP_400_BAD_REQUEST)
    # else:
    #      return Response({'Message': 'must add user id in body'}, status=status.HTTP_400_BAD_REQUEST)
