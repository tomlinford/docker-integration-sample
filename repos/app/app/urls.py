import hvac
import os

from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.models import User

from rest_framework import permissions, routers, serializers, viewsets

from secret.models import Secret


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("url", "username", "email")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SecretSerializer(serializers.HyperlinkedModelSerializer):
    secret = serializers.CharField()

    def save(self, user):
        secret = self.validated_data.pop("secret")
        instance = super(SecretSerializer, self).save(user=user)
        try:
            client = hvac.Client(
                url=os.environ["VAULT_URL"], token=settings.VAULT_TOKEN)
            client.write("secret/{}".format(instance.pk), value=secret)
        except:
            instance.delete()
            raise

    class Meta:
        model = Secret
        fields = ("url", "secret")


class SecretViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SecretSerializer

    def get_queryset(self):
        return Secret.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        super(SecretViewSet, self).perform_destroy(instance)
        client = hvac.Client(
            url=os.environ["VAULT_URL"], token=settings.VAULT_TOKEN)
        client.delete("secret/{}".format(instance.pk))


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"secrets", SecretViewSet, base_name="secret")

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^api-auth/",
        include("rest_framework.urls", namespace="rest_framework")),
]
