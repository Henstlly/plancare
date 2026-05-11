from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from cats.views import (
    CatViewSet, UserViewSet, FeedViewSet, MedicationViewSet,
    CarePlanItemViewSet, ExecutionLogViewSet
)

router = routers.DefaultRouter()
router.register('cats', CatViewSet)
router.register('users', UserViewSet)
router.register('feeds', FeedViewSet)
router.register('medications', MedicationViewSet)
router.register('care-plan', CarePlanItemViewSet)
router.register('execution-logs', ExecutionLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
