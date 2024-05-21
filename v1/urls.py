from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from v1.views.register import RegisterViewSet
from v1.views.verify_token import VerifyTokenViewSet
from .views import health_check
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register('register', RegisterViewSet, basename='register')
router.register('verify', VerifyTokenViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Django Workshop API",
        default_version='v1',
        description="Django Workshop API created using Swagger for generating documentation",
        terms_of_service="https://github.com/tilda-center/django-workshop/blob/main/LICENSE",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD 2"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = router.urls + [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('health-check/', health_check, name='health-check'),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
