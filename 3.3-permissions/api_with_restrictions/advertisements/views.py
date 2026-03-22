from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Advertisement, AdvertisementStatusChoices
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsCreatorOrAdmin, IsNotCreator


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsCreatorOrAdmin()]
        elif self.action in ['favorite', 'unfavorite']:
            return [permissions.IsAuthenticated(), IsNotCreator()]
        elif self.action == 'favorites_list':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """Фильтруем объявления в зависимости от статуса и прав пользователя"""
        queryset = Advertisement.objects.all()
        user = self.request.user

        # Если пользователь не авторизован, показываем только OPEN
        if not user.is_authenticated:
            return queryset.filter(status=AdvertisementStatusChoices.OPEN)

        if user.is_staff:
            return queryset

        return queryset.filter(
            Q(status=AdvertisementStatusChoices.OPEN) |
            Q(creator=user)
        ).distinct()

    def perform_create(self, serializer):
        """При создании объявления проставляем текущего пользователя"""
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """Добавить объявление в избранное"""
        advertisement = self.get_object()

        if advertisement.favorites.filter(id=request.user.id).exists():
            return Response(
                {"detail": "Объявление уже в избранном"},
                status=status.HTTP_400_BAD_REQUEST
            )

        advertisement.favorites.add(request.user)
        serializer = self.get_serializer(advertisement)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def unfavorite(self, request, pk=None):
        """Удалить объявление из избранного"""
        advertisement = self.get_object()

        if not advertisement.favorites.filter(id=request.user.id).exists():
            return Response(
                {"detail": "Объявление не в избранном"},
                status=status.HTTP_400_BAD_REQUEST
            )

        advertisement.favorites.remove(request.user)
        serializer = self.get_serializer(advertisement)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def favorites_list(self, request):
        """Получить список избранных объявлений пользователя"""
        favorite_ads = request.user.favorite_advertisements.filter(
            status=AdvertisementStatusChoices.OPEN
        )
        serializer = self.get_serializer(favorite_ads, many=True)
        return Response(serializer.data)