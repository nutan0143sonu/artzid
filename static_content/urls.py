from django.conf.urls import url

from static_content.views import *

urlpatterns = [
    url(r'^get-privacy-policy$', PrivacyPolicyView.as_view()),
    url(r'^get-terms-and-conditions$', TermsAndConditionsView.as_view()),
    url(r'^AboutUs$', AboutUsView.as_view()),
]