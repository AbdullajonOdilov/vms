from django.urls import path, include

from vendors.views import (
    VendorListCreateAPIView,
    VendorDetailAPIView,
    VendorPerformanceAPIView,
    PurchaseOrderListCreateAPIView,
    PurchaseOrderDetailAPIView, AcknowledgePurchaseOrderAPIView,
)

urlpatterns = [
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('api/vendors/<int:pk>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderDetailAPIView.as_view(), name='purchase-order-detail'),
path('api/purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(),
     name='acknowledge_purchase_order'),
]
