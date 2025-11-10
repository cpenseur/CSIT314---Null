# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, ServiceRequestViewSet, MessageViewSet, FinancialClaimViewSet,
    ReceiptUploadViewSet, DisputeViewSet, TrackingViewSet, MatchingViewSet, OTPViewSet
)

router = DefaultRouter()
router.register('register', RegisterView, basename='register')
router.register('requests', ServiceRequestViewSet, basename='requests')
router.register('messages', MessageViewSet, basename='messages')
router.register('claims', FinancialClaimViewSet, basename='claims')
router.register('receipts', ReceiptUploadViewSet, basename='receipts')
router.register('disputes', DisputeViewSet, basename='disputes')

tracking_view = TrackingViewSet.as_view({'post': 'view'})
tracking_shortlist = TrackingViewSet.as_view({'post': 'shortlist'})
match_suggest = MatchingViewSet.as_view({'get': 'suggest'})
match_commit = MatchingViewSet.as_view({'post': 'commit'})
match_respond = MatchingViewSet.as_view({'post': 'respond'})

otp_create = OTPViewSet.as_view({'post': 'create'})
otp_verify = OTPViewSet.as_view({'post': 'verify'})

urlpatterns = [
    path('', include(router.urls)),
    path('track/view/', tracking_view),
    path('track/shortlist/', tracking_shortlist),
    path('matching/suggest/<int:req_id>/', match_suggest),
    path('matching/commit/', match_commit),
    path('matching/respond/', match_respond),
    path('otp/create/', otp_create),
    path('otp/verify/', otp_verify),
]
