
from django.urls import path
from  . import views

urlpatterns = [
    path('',views.home,name='index3'),
    path('header/',views.header,name='header'),
    path('about/',views.about,name='about'),
    path('admin/',views.admin,name='admin'),
    path('category/<genere>',views.category,name='category'),
    path('details/<int:id1>/', views.details, name='details'),
    path('contacts/',views.contacts,name='contacts'),
    path('footer/',views.footer,name='footer'),
    path('interview/',views.interview,name='interview'),
    path('live/',views.live,name='live'),
    path('pricing/',views.pricing,name='pricing'),
    path('privacy/',views.privacy,name='privacy'),
    path('profile/',views.profile,name='profile'),
    path('signin/', views.signin, name='signin'),
    path('SignOut/',views.SignOut,name='SignOut'),
    path('signup/',views.signup,name='signup'),
    path('movie/<id1>',views.movies1,name='movie'),
    path('movies/',views.all_movies,name='movies'),
    path('series/<id2>',views.seriesview,name='series'),
    path('all-series/',views.tv_shows_view,name='all-series'),
    path('category-of-series/<genere>',views.category_of_series,name='category-of-series'),
    path('search/',views.searh,name='search'),
    path('watchlater/',views.watch_later,name='watchlater'),
    path('add_To_Watchlater_From_all_Series/<id>',views.add_To_Watchlater_From_all_Series,name='add_To_Watchlater_From_all_Series'),
    path('addToWatchlaterFromallmovies/<id>',views.addToWatchlaterFromallmovies,name='addToWatchlaterFromallmovies'),
    path('Remove_Watchlater/<id>',views.Remove_Watchlater,name='Remove_Watchlater'),
    path('add_To_Watchlater_From_Details/<id>',views.add_To_Watchlater_From_Details,name='add_To_Watchlater_From_Details'),


    

]
