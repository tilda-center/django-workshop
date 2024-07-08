from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from v1.views.register import RegisterViewSet
from v1.views.verify_token import VerifyTokenViewSet
from v1.views.lecture import ProfessorLectureViewSet
from v1.views.event import ProfessorEventViewSet
from .views import health_check

router = DefaultRouter()
router.register('register', RegisterViewSet, basename='register')
router.register('verify', VerifyTokenViewSet)
router.register('professor/lectures', ProfessorLectureViewSet)

lectures_router = routers.NestedDefaultRouter(router, 'professor/lectures', lookup='lecture')
lectures_router.register('events', ProfessorEventViewSet, basename='lecture-events')

urlpatterns = router.urls + lectures_router.urls + [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('health-check/', health_check, name='health-check'),
]
