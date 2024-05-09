from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import filters
from rest_framework.filters import SearchFilter
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema


class VendorListCreateAPIView(APIView):
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    def get(self, request):
        search_query = request.GET.get('search', '')

        # Filter vendors based on the search query
        vendors = Vendor.objects.filter(name__icontains=search_query)
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(vendors, request)
        serializer = VendorSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)


    @swagger_auto_schema(
        operation_summary="Create Vendor instance",
        request_body=VendorSerializer,
        consumes=['application/json', 'application/xml', 'application/x-www-form-urlencoded'],
        responses={201: VendorSerializer(), 400: "Invalid data"},
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailAPIView(APIView):
    def get_vendor(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        vendor = self.get_vendor(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update Vendor instance",
        request_body=VendorSerializer,
        consumes=['application/json', 'application/xml', 'application/x-www-form-urlencoded'],
        responses={201: VendorSerializer(), 400: "Invalid data"},
    )

    def put(self, request, pk):
        vendor = self.get_vendor(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        vendor = self.get_vendor(vendor_id)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderListCreateAPIView(APIView):
    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Purchase Order Instance",
        request_body=PurchaseOrderSerializer,
        consumes=['application/json', 'application/xml', 'application/x-www-form-urlencoded'],
        responses={201: PurchaseOrderSerializer(), 400: "Invalid data"},
    )
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Purchase Order Instance",
        request_body=PurchaseOrderSerializer,
        consumes=['application/json', 'application/xml', 'application/x-www-form-urlencoded'],
        responses={201: PurchaseOrderSerializer(), 400: "Invalid data"},
    )
    def put(self, request, pk):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        purchase_order = self.get_object(pk)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorPerformanceAPIView(APIView):
    def get_vendor_performance(self, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            raise Http404("Vendor does not exist")

        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }

        return performance_data

    def get(self, request, vendor_id):
        performance_data = self.get_vendor_performance(vendor_id)
        serializer = VendorPerformanceSerializer(data=performance_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class AcknowledgePurchaseOrderAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Acknowledge Purchase Order Instance",
        request_body=PurchaseOrderSerializer,
        consumes=['application/json', 'application/xml', 'application/x-www-form-urlencoded'],
        responses={201: PurchaseOrderSerializer(), 400: "Invalid data"},
    )
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        return Response(status=status.HTTP_200_OK)
