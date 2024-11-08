from django.urls import path,include
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    #path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
