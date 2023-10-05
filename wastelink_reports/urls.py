"""
URL configuration for wastelink_reports project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import pivot, home, instockmtddone, suppliervolume, kelloggs_report
from .views import aging_report,home
urlpatterns = [
    path('admin/', admin.site.urls),
    path("pivot/",pivot,name="pivot"),
    path("aging_report/",aging_report,name="aging_report"),
    path("instockmtddone/",instockmtddone,name="instockmtddone"),
    path("suppliervolume/",suppliervolume,name="suppliervolume"),
    path("kelloggs_report/",kelloggs_report,name="kelloggs_report"),
    path("",home,name="home"),

]
