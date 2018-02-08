# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from .models import Snippet
from django.contrib.auth.models import User
from .serializers import SnippetSerializer, UserSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import renderers
from django.contrib.auth.mixins import LoginRequiredMixin


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update' and 'destroy' actions.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
