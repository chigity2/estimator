from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.projects, name='projects'),
    path('<int:id>', views.project_detail, name='project_detail'),
    path('owners', views.owners, name='owners'),
    path('<int:id>/update', views.update_project, name='update_project'),
    path('<int:id>/note', views.note, name='note'),
    path('<int:id>/add_bid', views.add_bid, name='add_bid'),
    path('<int:project>/<int:id>', views.bid_detail, name='bid_detail'),
    path('<int:project>/<int:id>/update', views.update_bid, name='update_bid'),
    path('<int:project>/<int:id>/<int:package>', views.bid_packages, name='bid_packages'),
    path('<int:project>/<int:id>/<int:package>/invite', views.invite_sub, name='invite_sub'),
    path('<int:project>/<int:id>/<int:package>/<int:subpack>', views.bid_received, name='bid_received'),
    path('<int:project>/<int:id>/<int:package>/<int:subpack>/upd', views.upd_bidding, name='upd_bidding')
]

