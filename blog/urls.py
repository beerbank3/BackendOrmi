from django.urls import path
from blog.views import Index

urlpatterns = [
    #path(패턴, 매핑)
    path("", Index.as_view())
]