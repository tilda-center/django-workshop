from django.urls import path 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from v1.views.register import RegisterViewSet 
from v1.views.verify_token import VerifyTokenViewSet

router = DefaultRouter()
router.register('register', RegisterViewSet)
router.register('verify', VerifyTokenViewSet)

urlpatterns = router.urls + [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
