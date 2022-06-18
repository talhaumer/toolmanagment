from django.urls import path

from . import views

urlpatterns = [
    path('tools', views.ToolsView.as_view(), name="tools"),
    path('tools/<int:pk>', views.ToolsView.as_view(), name="tools"),
    path('tools/allocation', views.ToolsAllocationView.as_view(), name="tools allocations"),
    path('tools/available', views.AvailableToolsView.as_view(), name ="available tools"),
    path('tools/listing', views.ToolListingView.as_view(), name="test")
]
