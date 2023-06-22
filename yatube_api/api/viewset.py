from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        GenericViewSet):
    pass
