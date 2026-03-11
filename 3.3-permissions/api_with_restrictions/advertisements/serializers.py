from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'is_favorite')

    def get_is_favorite(self, obj):
        """Проверяет, находится ли объявление в избранном у текущего пользователя"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        request = self.context.get('request')
        if request and request.method == 'POST':
            user = request.user

            if user.is_authenticated:
                open_ads_count = Advertisement.objects.filter(
                    creator=user,
                    status=AdvertisementStatusChoices.OPEN
                ).count()

                if data.get('status') == AdvertisementStatusChoices.OPEN and open_ads_count >= 10:
                    raise serializers.ValidationError(
                        "У пользователя не может быть больше 10 открытых объявлений"
                    )

        return data