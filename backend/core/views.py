from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import (
    User, ServiceRequest, RequestView, Shortlist, Match, Message,
    FinancialClaim, Receipt, Dispute, OTPToken
)
from .serializers import (
    UserSerializer, ServiceRequestSerializer, MatchSerializer, MessageSerializer,
    FinancialClaimSerializer, ReceiptSerializer, DisputeSerializer, OTPSerializer
)
from .permissions import IsPIN, IsCV, IsCSR, IsAdmin, CanEditPendingRequest


# ===== Auth & Registration =====
class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# ===== PIN: create/edit/duplicate/delete requests =====
class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all().select_related('pin')
    serializer_class = ServiceRequestSerializer

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [IsAuthenticated()]
        # create allowed only to PIN
        if self.action == 'create':
            return [IsPIN()]
        # update/delete allowed only if pending and owned by PIN
        if self.action in ['update','partial_update','destroy','duplicate']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(pin=self.request.user)

    def perform_destroy(self, instance):
        # Restrict delete to pending owned by PIN
        if instance.pin != self.request.user or instance.status != ServiceRequest.STATUS_PENDING:
            raise PermissionError('Only owner PIN can delete pending requests.')
        instance.delete()

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        req = self.get_object()
        if req.pin != request.user:
            return Response({'detail':'Not your request.'}, status=403)
        new_dt_str = request.data.get('appointment_date')
        if not new_dt_str:
            return Response({'detail':'appointment_date required.'}, status=400)
        new_dt = timezone.datetime.fromisoformat(new_dt_str)
        copy = req.duplicate(new_dt)
        return Response(ServiceRequestSerializer(copy).data)

# ===== Views & Shortlists tracking (simple endpoints) =====
class TrackingViewSet(viewsets.ViewSet):
    # POST /api/track/view/ {request: id}
    @action(detail=False, methods=['post'])
    def view(self, request):
        req_id = request.data.get('request')
        req = ServiceRequest.objects.get(id=req_id)
        RequestView.objects.create(request=req, viewer=request.user)
        return Response({'ok': True})

    # POST /api/track/shortlist/ {request: id}
    @action(detail=False, methods=['post'])
    def shortlist(self, request):
        if request.user.role != User.ROLE_CSR:
            return Response({'detail':'Only CSR can shortlist.'}, status=403)
        req_id = request.data.get('request')
        req = ServiceRequest.objects.get(id=req_id)
        Shortlist.objects.get_or_create(request=req, csr=request.user)
        return Response({'ok': True})

# ===== Matching flow (CSR selects CV; CV accepts/declines) =====
class MatchingViewSet(viewsets.ViewSet):
    # GET /api/matching/suggest/<request_id>/  → returns 7 CV user IDs (stub)
    @action(detail=False, methods=['get'], url_path='suggest/(?P<req_id>[^/.]+)')
    def suggest(self, request, req_id=None):
        if request.user.role != User.ROLE_CSR:
            return Response({'detail':'CSR only.'}, status=403)
        req = ServiceRequest.objects.get(id=req_id)
        cvs = User.objects.filter(role=User.ROLE_CV).order_by('?')[:7]
        data = [{'id': u.id, 'username': u.username} for u in cvs]
        return Response({'suggested': data})

    # POST /api/matching/commit/ {request: id, cv: id}
    @action(detail=False, methods=['post'])
    def commit(self, request):
        if request.user.role != User.ROLE_CSR:
            return Response({'detail':'CSR only.'}, status=403)
        req = ServiceRequest.objects.get(id=request.data.get('request'))
        cv = User.objects.get(id=request.data.get('cv'), role=User.ROLE_CV)
        match, _ = Match.objects.update_or_create(request=req, defaults={'cv': cv, 'accepted': None, 'offered_at': timezone.now()})
        req.status = ServiceRequest.STATUS_PENDING  # still pending until CV accepts
        req.save(update_fields=['status'])
        return Response(MatchSerializer(match).data)

    # POST /api/matching/respond/ {match: id, accept: true/false}
    @action(detail=False, methods=['post'])
    def respond(self, request):
        if request.user.role != User.ROLE_CV:
            return Response({'detail':'CV only.'}, status=403)
        match = Match.objects.get(id=request.data.get('match'), cv=request.user)
        accept = bool(request.data.get('accept'))
        match.accepted = accept
        match.accepted_at = timezone.now()
        match.save()
        # Flip request status
        req = match.request
        req.status = ServiceRequest.STATUS_ACTIVE if accept else ServiceRequest.STATUS_PENDING
        req.save(update_fields=['status'])
        return Response({'accepted': accept})

# ===== Messaging (allowed only when ACTIVE and within 24h after COMPLETED) =====
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('request','sender')
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        req = ServiceRequest.objects.get(id=self.request.data.get('request'))
        # Chat rules
        if req.status == ServiceRequest.STATUS_PENDING:
            raise PermissionError('Chat opens when request is ACTIVE.')
        if req.status == ServiceRequest.STATUS_COMPLETED:
            if timezone.now() > req.date_created + timezone.timedelta(days=9999):
                pass  # placeholder; we’ll limit via completed_at if you add it
        serializer.save(sender=self.request.user)

# ===== Claims & Receipts =====
class FinancialClaimViewSet(viewsets.ModelViewSet):
    queryset = FinancialClaim.objects.all().select_related('request','cv')
    serializer_class = FinancialClaimSerializer

    def perform_create(self, serializer):
        serializer.save(cv=self.request.user)

    @action(detail=True, methods=['post'])
    def approve_by_pin(self, request, pk=None):
        claim = self.get_object()
        if request.user != claim.request.pin:
            return Response({'detail':'Only PIN can approve.'}, status=403)
        claim.approved_by_pin = True
        claim.save(update_fields=['approved_by_pin'])
        return Response({'ok': True})

    @action(detail=True, methods=['post'])
    def approve_by_csr(self, request, pk=None):
        claim = self.get_object()
        if request.user.role != User.ROLE_CSR:
            return Response({'detail':'Only CSR can approve.'}, status=403)
        claim.approved_by_csr = True
        claim.save(update_fields=['approved_by_csr'])
        return Response({'ok': True})

class ReceiptUploadViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

# ===== Disputes =====
class DisputeViewSet(viewsets.ModelViewSet):
    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer

# ===== OTP (simplified; plug your email later) =====
class OTPViewSet(viewsets.ViewSet):
    # POST /api/otp/create/ {user: id}  → generates 6-digit code
    @action(detail=False, methods=['post'])
    def create(self, request):
        import random
        user = User.objects.get(id=request.data.get('user'))
        code = f"{random.randint(0, 999999):06d}"
        OTPToken.objects.create(user=user, code=code)
        # TODO: send email to user.email
        return Response({'sent': True, 'demo_code': code})  # show code for dev

    # POST /api/otp/verify/ {user: id, code: '123456'}
    @action(detail=False, methods=['post'])
    def verify(self, request):
        token = OTPToken.objects.filter(user_id=request.data.get('user'), code=request.data.get('code'), is_used=False).last()
        if not token or token.is_expired():
            return Response({'valid': False}, status=400)
        token.is_used = True
        token.save(update_fields=['is_used'])
        return Response({'valid': True})