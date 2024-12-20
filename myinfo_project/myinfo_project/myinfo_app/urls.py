from django.urls import path
from .views import (
    MyInfoAuthURLView,
    MyInfoRetrieveAccessTokenView,
    MyInfoRetrieveDataView,
)

urlpatterns = [
    path('auth-url/', MyInfoAuthURLView.as_view(), name='auth-url'),
    path('access-token/', MyInfoRetrieveAccessTokenView.as_view(), name='access-token'),
    path('retrieve-data/', MyInfoRetrieveDataView.as_view(), name='retrieve-data'),
]
