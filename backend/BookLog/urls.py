
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,  # опционально для logout
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # dj-rest-auth: login, logout, password change
    path('api/auth/', include('dj_rest_auth.urls')),

    # регистрация + подтверждение email + сброс пароля
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path(
        'api/journal/',
        include(
          ('journal.urls', 'journal'),   # <- tuple из (путь к urls, app_name)
          namespace='journal'            # <- чтобы reverse('journal:…') работал 100%
        )
),

]

# В режиме DEBUG раздаём медиа-файлы
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
