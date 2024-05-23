from django.urls import path
from . import views
urlpatterns = [
    path('home/',views.Homepage.as_view()),
    path('home/<str:category>/',views.Homepage.as_view()),
    
    path('homep/popular/', views.PopularDestination.as_view()),
    path('destdetail/<int:id>/',views.Destinationdetail.as_view()),
    path('search/',views.Search.as_view()),
    path('booknow/<int:id>/',views.Booknow.as_view()),
    path('bookingdetail/',views.Bookdetail.as_view()),
    path('checkout/',views.Checkout.as_view()),
    path('sidebar/<str:data>/',views.Sidebar.as_view()),
    path('sidebar/',views.Sidebar.as_view()),
    
    
    
    
    # path('searchable/',views.Searchable.as_view()),
    
    
]