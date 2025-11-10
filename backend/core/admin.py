from django.contrib import admin
from .models import *
admin.site.register([User, 
                     PINPreference, 
                     ServiceRequest, 
                     RequestView, 
                     Shortlist, 
                     Match,
                     Message, 
                     FinancialClaim, 
                     ClaimItem, 
                     Receipt, 
                     Dispute, 
                     OTPToken])