from django.contrib import admin
from django.conf.urls import url,include


urlpatterns = [url('admin/', admin.site.urls),
               url(r'^$',include('home.urls')),
               url(r'stock',include('stock.urls')),
               url(r'crypto',include('crypto.urls')),
               url(r'api/b2b/crypto/blockchail/trend',include('Api.urls'))
               ]

