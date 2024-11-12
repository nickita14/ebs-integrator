from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


admin.site.site_header = 'EBS Integrator Project'
admin.site.site_title = 'EBS Integrator Project'
admin.site.index_title = 'Functionality'

urlpatterns = [
    path('api/admin/', admin.site.urls),

    path('api/schema/', staff_member_required(SpectacularAPIView.as_view()), name='schema'),
    path('api/schema/redoc/', staff_member_required(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),
    path('api/schema/swagger-ui/', staff_member_required(SpectacularSwaggerView.as_view(url_name='schema')), name='django-admindocs-docroot'),

    # path('api/v1/', include('api.urls')),
]
