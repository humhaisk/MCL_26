from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',view=views.index,name='home'),
    path('list/',view=views.teamList,name='teamlist'),
    path('admin-site/',view=views.admin_site,name='admin-site'),
    path('admin/',view=views.admin_site,name='admin-dasboard'),
    path('all-bids/',view=views.all_bids,name='all-bids'),
    path('login/',view=views.user_login,name='login'),
    path('logout/',view=views.user_logout,name='logout'),
    path('yt-live/',view=views.yt_live,name='yt-live'),
    ############ API URL ########################
    path("api/random-player/", views.get_random_player),
    path("api/pending-player/", views.get_pending_player),
    path("api/last-transaction-player/", views.get_last_transaction_player),
    path("api/get-count/", views.useful_counter),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


