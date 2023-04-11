from django.urls import path, include
from . import views


urlpatterns = [
    path('trades', views.trades, name='trades'),
    path('trades/delete/<int:pk>', views.delete_trade, name='t_del'),
    path('subcontractors',views.subcontractors, name='subcontractors'),
    path('subcontractors/<int:id>', views.sub_detail, name='sub_detail'),
    path('subcontractors/<int:id>/add_employee', views.add_employee, name='add_employee'),
    path('subcontractors/<int:sub>/set_primary/<int:emp>', views.set_primary_employee, name='set_primary'),
    path('subcontractors/<int:sub>/add_trade', views.add_trade, name='add_trade'),
    path('subcontractors/<int:sub>/update_employee/<int:emp>', views.upd_emp, name='upd_employee'),
    path('subcontractors/<int:sub>/update', views.upd_sub, name='upd_sub')
]
