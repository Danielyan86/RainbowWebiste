from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from project_name.views import homepage
from ShowRings.views import *
from SearchDiamond.views  import search_diamond

urlpatterns = patterns("",
#     url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^$", homepage),
    url(r"^rings/$", show_rings),
    url(r"^searchdiamond/$", search_diamond),
    
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
