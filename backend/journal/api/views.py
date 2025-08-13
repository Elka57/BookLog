from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, AllowAny

from BookLog.permissions import is_self
from users.models import UserTypes
from journal.models import (
    Author, Genre, Book, BookLog, Quote, Like, Share,
    ApprovalStatus
)
from journal.api.serializers import (
    AuthorSerializer, GenreSerializer, BookSerializer,
    BookLogSerializer, QuoteSerializer, LikeSerializer,
    ShareSerializer
)
from journal.api.filters import QuoteFilter


# 1) «ИЛИ»-permission: если любой из списка даёт True — разрешаем
class OrPermission(BasePermission):
    def __init__(self, perm_classes):
        self.perms = [cls() for cls in perm_classes]

    def has_permission(self, request, view):
        return any(p.has_permission(request, view) for p in self.perms)

    def has_object_permission(self, request, view, obj):
        return any(p.has_object_permission(request, view, obj) for p in self.perms)


# 2) Простые классы по ролям
class IsJournalist(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and int(request.user.user_type) == int(UserTypes.JOURNALIST.value)
        )

class IsReader(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user
            and request.user.is_authenticated
            and (int(request.user.user_type) == int(UserTypes.READER.value))
        )

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and int(request.user.user_type) == int(UserTypes.STAFF.value)
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and int(request.user.user_type) == int(UserTypes.ADMIN.value)
        )


# 3) Запретить только анонимов (возвращает 403, а не 401)
class DenyAnonymous(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous


# 4) Mixin для per‐action permissions
class ActionBasedPermissionsMixin:
    """
    Определяем в подклассах словарь:
        permission_map = {
          'action_name': [PermClass1, PermClass2, …],
          …
        }
    Если для action даётся несколько классов — они объединяются через OR (OrPermission).
    Если action нет в map — берётся [AllowAny] (то есть метод публичный).
    """
    permission_map = {}

    def get_permissions(self):
        perms = self.permission_map.get(self.action)
        if perms is None:
            return [AllowAny()]

        if not isinstance(perms, (list, tuple)):
            perms = [perms]

        if len(perms) == 1:
            return [perms[0]()]
        return [OrPermission(perms)]

class ModeratedMixin:
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            status=ApprovalStatus.PENDING,
        )

    def perform_update(self, serializer):
        extra = {}
        if self.request.user.user_type == UserTypes.JOURNALIST.value:
            extra['status'] = ApprovalStatus.PENDING
        serializer.save(**extra)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        obj = self.get_object()
        obj.status = ApprovalStatus.APPROVED
        obj.save(update_fields=['status'])
        return Response(self.get_serializer(obj).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        obj = self.get_object()
        obj.status = ApprovalStatus.REJECTED
        obj.save(update_fields=['status'])
        return Response(self.get_serializer(obj).data, status=status.HTTP_200_OK)

# ——— AuthorViewSet ——————————————————————————————————————————————————

class AuthorViewSet(ActionBasedPermissionsMixin, ModeratedMixin, viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    permission_map = {
        'create':         [IsJournalist, IsStaff,    IsAdmin],
        'list':           AllowAny,
        'retrieve':       AllowAny,
        'update':         [IsJournalist, IsStaff,    IsAdmin],
        'partial_update': [IsJournalist, IsStaff,    IsAdmin],
        'destroy':        [IsStaff,     IsAdmin],
        'approve':        [IsStaff,     IsAdmin],
        'reject':         [IsStaff,     IsAdmin],
    }


# ——— GenreViewSet ——————————————————————————————————————————————————

class GenreViewSet(ActionBasedPermissionsMixin, ModeratedMixin, viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    permission_map = {
        'create':         [IsJournalist, IsStaff, IsAdmin],
        'list':           AllowAny,
        'retrieve':       AllowAny,
        'update':         [IsJournalist, IsStaff, IsAdmin],
        'partial_update': [IsJournalist, IsStaff, IsAdmin],
        'destroy':        [IsStaff,     IsAdmin],
    }


# ——— BookViewSet ——————————————————————————————————————————————————

class BookViewSet(ActionBasedPermissionsMixin, ModeratedMixin, viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author', 'genre').all()
    serializer_class = BookSerializer

    permission_map = {
        'create':         [IsJournalist, IsStaff, IsAdmin],
        'list':           AllowAny,
        'retrieve':       AllowAny,
        'update':         [IsJournalist, IsStaff, IsAdmin],
        'partial_update': [IsJournalist, IsStaff, IsAdmin],
        'destroy':        [IsStaff,     IsAdmin],
        'approve':        [IsStaff,     IsAdmin],
        'reject':         [IsStaff,     IsAdmin],
    }

# ——— BookLogViewSet ——————————————————————————————————————————————————

class BookLogViewSet(ActionBasedPermissionsMixin, viewsets.ModelViewSet):
    queryset = BookLog.objects.select_related(
        'book', 'book__author', 'book__genre'
    )
    serializer_class = BookLogSerializer

    permission_map = {
        'create':         [IsJournalist, IsStaff, IsAdmin],
        'list':           DenyAnonymous,  # только залогиненным
        'retrieve':       DenyAnonymous,
        'update':         [IsJournalist, IsStaff, IsAdmin],
        'partial_update': [IsJournalist, IsStaff, IsAdmin],
        'destroy':        [IsJournalist, IsStaff, IsAdmin],
    }


# ——— QuoteViewSet ——————————————————————————————————————————————————

class QuoteViewSet(ActionBasedPermissionsMixin, viewsets.ModelViewSet):
    queryset = Quote.objects.select_related(
        'book', 'book__author', 'book__genre', 'book_log'
    ).prefetch_related('like_records__user', 'share_records__user')
    serializer_class = QuoteSerializer
    filterset_class = QuoteFilter

    permission_map = {
        'create':         [IsJournalist, IsReader, IsStaff, IsAdmin],
        'list':           AllowAny,
        'retrieve':       AllowAny,
        'update':         [is_self, IsStaff, IsAdmin],
        'partial_update': [is_self, IsStaff, IsAdmin],
        'destroy':        [is_self, IsStaff, IsAdmin],
    }


# ——— LikeViewSet ——————————————————————————————————————————————————

class LikeViewSet(ActionBasedPermissionsMixin, viewsets.ModelViewSet):
    queryset = Like.objects.select_related('user', 'quote')
    serializer_class = LikeSerializer

    permission_map = {
        'create':         [IsJournalist,  IsReader, IsStaff, IsAdmin],
        'list':           AllowAny,
        'retrieve':       AllowAny,
        'destroy':        [is_self, IsStaff, IsAdmin],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ——— ShareViewSet ——————————————————————————————————————————————————

class ShareViewSet(ActionBasedPermissionsMixin, viewsets.ModelViewSet):
    queryset = Share.objects.select_related('user', 'quote')
    serializer_class = ShareSerializer

    permission_map = {
        'create':         [IsJournalist,  IsReader, IsStaff, IsAdmin],
        'list':           AllowAny,
        'retrieve':       AllowAny,
        'destroy':        [is_self, IsStaff, IsAdmin],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
