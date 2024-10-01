from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('catalog.urls', 'catalog'), namespace='catalog')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
