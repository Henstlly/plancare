from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Cat, User, Feed, Medication, CarePlanItem, ExecutionLog
from .permissions import IsOwnerOrReadOnly, IsCatOwnerOrReadOnly
from .serializers import (
    CatSerializer, UserSerializer, FeedSerializer, MedicationSerializer,
    CarePlanItemSerializer, ExecutionLogSerializer
)


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['color', 'owner']
    search_fields = ['name']
    ordering_fields = ['name', 'birth_year']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CarePlanItemViewSet(viewsets.ModelViewSet):
    queryset = CarePlanItem.objects.all()
    serializer_class = CarePlanItemSerializer
    permission_classes = [IsCatOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cat', 'action_type', 'is_active']
    ordering_fields = ['scheduled_time', 'created_at']
    search_fields = ['notes']

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            if self.request.user.is_staff or self.request.user.is_superuser:
                return CarePlanItem.objects.all()
            return CarePlanItem.objects.filter(cat__owner=self.request.user)
        return CarePlanItem.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsCatOwnerOrReadOnly])
    def execute(self, request, pk=None):
        item = self.get_object()
        if not item.is_active:
            return Response(
                {'detail': 'Пункт плана уже неактивен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ExecutionLog.objects.create(
            care_plan_item=item,
            cat=item.cat,
            status='completed',
            notes=request.data.get('notes', '')
        )
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsCatOwnerOrReadOnly])
    def cancel(self, request, pk=None):
        item = self.get_object()
        if not item.is_active:
            return Response(
                {'detail': 'Пункт плана уже неактивен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ExecutionLog.objects.create(
            care_plan_item=item,
            cat=item.cat,
            status='cancelled',
            notes=request.data.get('notes', '')
        )
        item.is_active = False
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsCatOwnerOrReadOnly])
    def history(self, request, pk=None):
        item = self.get_object()
        logs = item.execution_logs.all()
        serializer = ExecutionLogSerializer(logs, many=True)
        return Response(serializer.data)


class ExecutionLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExecutionLog.objects.all()
    serializer_class = ExecutionLogSerializer
    permission_classes = [IsCatOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['cat', 'care_plan_item', 'status']
    ordering_fields = ['executed_at']

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            if self.request.user.is_staff or self.request.user.is_superuser:
                return ExecutionLog.objects.all()
            return ExecutionLog.objects.filter(cat__owner=self.request.user)
        return ExecutionLog.objects.none()
