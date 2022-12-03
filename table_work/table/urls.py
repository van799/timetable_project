from django.urls import path

from . import views

app_name = 'table'

urlpatterns = [
    path('', views.index, name="index"),
    path(
        'create/', views.create_table, name='create_table'
    ),
    path(
        'edit_table/<int:event_id>/', views.edit_table, name='edit_table'
    ),
    path(
        'comment/<int:selected_calendar>/', views.add_comment, name='add_comment'
    ),
    path(
        'analytics/', views.analytics, name='analytics'
    ),
]
