from rest_framework import serializers
from .models import User, PINPreference, ServiceRequest, Match, Message, FinancialClaim, ClaimItem, Receipt, Dispute, OTPToken

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','password','full_name','date_of_birth','home_address','role',
                  'company_name','company_id','company_email','email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        if user.role == User.ROLE_PIN:
            PINPreference.objects.get_or_create(user=user)
        return user


class PINPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PINPreference
        fields = ['preferred_language','preferred_volunteer_gender']

class ServiceRequestSerializer(serializers.ModelSerializer):
    pin_username = serializers.ReadOnlyField(source='pin.username')
    class Meta:
        model = ServiceRequest
        fields = ['id','request_id','pin','pin_username','service_type','appointment_date',
                  'pickup_location','service_location','description','status','date_created',
                  'views','shortlists']
        read_only_fields = ['request_id','status','date_created','views','shortlists']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id','request','cv','offered_at','accepted','accepted_at']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    class Meta:
        model = Message
        fields = ['id','request','sender','sender_username','text','sent_at']
        read_only_fields = ['sent_at']

class ClaimItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimItem
        fields = ['id','category','date_of_expense','total_amount','payment_method','description']

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id','image','uploaded_at']
        read_only_fields = ['uploaded_at']

class FinancialClaimSerializer(serializers.ModelSerializer):
    items = ClaimItemSerializer(many=True)
    class Meta:
        model = FinancialClaim
        fields = ['id','request','cv','approved_by_pin','approved_by_csr','submitted_at','items']
        read_only_fields = ['approved_by_pin','approved_by_csr','submitted_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        claim = FinancialClaim.objects.create(**validated_data)
        for item in items_data:
            ClaimItem.objects.create(claim=claim, **item)
        return claim

class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = ['id','request','pin','incorrect_amount','incorrect_item','incorrect_receipt','description','created_at']
        read_only_fields = ['created_at']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPToken
        fields = ['id','user','code','created_at','is_used']
        read_only_fields = ['created_at','is_used']