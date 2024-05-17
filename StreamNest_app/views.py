from datetime import date

from pyexpat.errors import messages
from django.contrib import messages

from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.shortcuts import redirect, render
from . models import *
from django.db.models import Avg







def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            request.session["user_ID"] = user.id
            return redirect('index3') 
        else:
            wrong_message = "Wrong email or password"
            messages.error(request, wrong_message) 
    return render(request, 'signin.html')

def SignOut(request):
    logout(request)
    return redirect('index3')


def signup(request):
    if request.POST:
        
        name=request.POST["u_name"]
        email=request.POST["u_email"]
        password=request.POST["u_pass"]
        login=Login.objects.create_user(username=email,password=password,userType='customer',viewpassword=password)
        login.save()
      
        obj=user_reg.objects.create( user=login,u_name=name,u_email=email,u_password=password,)
        obj.save()
        return redirect('signin')
    return render(request,'signup.html')
@login_required(login_url='signin')
def profile(request):
    user_id = request.session.get("user_ID")
   
      

    data = user_reg.objects.filter(user__id=user_id)
    reg_id = user_reg.objects.get(user__id=user_id)
    if 'update_name' in request.POST:
            new_name = request.POST.get('u_name')
            new_email = request.POST.get('u_email')
          
            
            reg_id.u_name = new_name
            reg_id.u_email = new_email
            reg_id.save()
    new_pass=None
    message=None
    if 'update_pass' in request.POST:
            old_pass = request.POST.get('oldpass')
            new_pass = request.POST.get('newpass')
            if (old_pass==reg_id.u_password):
                reg_id.u_password = new_pass
                reg_id.save()
                message = "Password updated successfully"
            else:
                 message = "Old password is incorrect"     
          
    reg = get_object_or_404(user_reg, user__id=user_id)
    m_comments = review_of_movies.objects.filter(user_id=reg)
    s_comments = review_of_series.objects.filter(user_id=reg)
    m_comment_count=m_comments.count()  
    s_comment_count=s_comments.count()  
    comment_count=int(m_comment_count) + int(s_comment_count)


    

    reg = get_object_or_404(user_reg, user__id=user_id)
    watchlater_items = Watchlater_of_movies_and_series.objects.filter(user_id=reg)
    watch_later_count=watchlater_items.count()        
                   
    selected_amt = request.POST.get('amount')  
    plan = None
    if selected_amt in ['50', '100', '200']:  
        plan = int(selected_amt)
        user_reg_obj = get_object_or_404(user_reg, user__id=user_id)
        obj, created = Plans.objects.get_or_create(selected_plan=plan, user_id=user_reg_obj)
        if created: 
            obj.save()

    context={
        'data':data,
        'message': message,
        'watch_later_count': watch_later_count,
        'comment_count': comment_count
    }
    return render(request,'profile.html',context)



def home(request):
    most_rated_movies = movies.objects.annotate(avg_rating=Avg('review_of_movies__user_rating')).order_by('-avg_rating')
    for movie in most_rated_movies:
        if movie.avg_rating is not None:
            movie.avg_rating = round(movie.avg_rating, 2)
            
    
    latest_movies = movies.objects.order_by('-id')[:8]
    for movie in latest_movies:
        ratings = review_of_movies.objects.filter(movies_id=movie).values_list('user_rating', flat=True)
        
        if ratings:
            average_rating = sum(ratings) / len(ratings)
            movie.avg_rating = round(average_rating, 2)
        else:
            movie.avg_rating = None
    
    latest_series = series.objects.order_by('-id')[:8]
    for series_obj in latest_series:
        series_episodes = episodes.objects.filter(season_id__series_id=series_obj)
        series_avg_rating = review_of_series.objects.filter(episodes_id__in=series_episodes).aggregate(avg_rating=Avg('user_rating'))['avg_rating']
        if series_avg_rating is not None:
            series_obj.avg_rating = round(series_avg_rating, 2)
        else:
            series_obj.avg_rating = None
            
    movies_with_plan = movies.objects.exclude(m_plan=0)
    movies_with_plan1 = movies_with_plan.annotate(avg_rating=Avg('review_of_movies__user_rating')).order_by('-avg_rating')
   

    u_id = request.session.get("user_ID")
    user_plan = Plans.objects.filter(user_id=u_id).exists()



    context = {
        'has_plan':user_plan,
        'plan_movies':movies_with_plan1,
        'latest_movie': latest_movies,
        'latest_series': latest_series,
        'most_rated_movies': most_rated_movies
    }

    return render(request,'index3.html',context)

def header(request):
    return render(request,'header.html')
def about(request):
    return render(request,'about.html')

def admin(request):
    return render(request,'admin.html')
def category(request,genere):


    category_of_movies=movies.objects.filter(m_genre=genere)
    print(category_of_movies)
    context={
        'category_of_series':category_of_series,
        'category_of_movies':category_of_movies,

    }

    return render(request,'category.html',context)


def category_of_series(request,genere):
    category_of_series=series.objects.filter(s_genre=genere)
    context={
        'category_of_series':category_of_series,

    }
    return render(request,'category-of-series.html',context)

@login_required(login_url='signin')
def movies1(request, id1):
    u_id = request.session.get("user_ID")
    user = user_reg.objects.get(user__id=u_id)
    movie = movies.objects.get(id=id1)
    

    reviews = review_of_movies.objects.filter(movies_id=movie)
    count = reviews.count()

    movie_rating = review_of_movies.objects.filter(movies_id=movie).aggregate(avg_rating=Avg('user_rating'))['avg_rating']
    if movie_rating is not None:
        movie_rating = round(movie_rating, 2)

    if 'savereview' in request.POST:
        review1 = request.POST["review"]
        rating = request.POST["rating"]
        current_date = date.today()
        obj = review_of_movies.objects.create(user_review=review1, user_rating=rating, review_date=current_date, user_id=user,
                                    movies_id=movie)
        obj.save()
        return redirect('movie', id1=id1)

    context = {
        'movie': movie,
        'count': count,
        'reviews': reviews,
        'movie_rating': movie_rating, 
        
    }
    return render(request, 'movie.html', context)

def all_movies(request):
    selected_item = None
    if request.method == 'POST':
        selected_item = request.POST.get('grade')
    
    latest_movies = None
    oldest_movies = None
    popular_movies = None
    
    if selected_item == 'oldest':
        oldest_movies = movies.objects.annotate(avg_rating=Avg('review_of_movies__user_rating')).order_by('id')
    elif selected_item == 'popular':
        popular_movies = movies.objects.annotate(avg_rating=Avg('review_of_movies__user_rating')).order_by('-avg_rating')
    else:
        latest_movies = movies.objects.annotate(avg_rating=Avg('review_of_movies__user_rating')).order_by('-id')
    
    context = {
        'latest_movies': latest_movies,
        'oldest_movies': oldest_movies,
        'popular_movies': popular_movies,
    }
    
    return render(request, 'movies.html', context)


@login_required(login_url='signin')
def seriesview(request, id2):
    u_id = request.session.get("user_ID")
    user = user_reg.objects.get(user__id=u_id)
    series1 = episodes.objects.get(id=id2)
    reviews = review_of_series.objects.filter(episodes_id=series1)
    comments = comment_of_series.objects.filter(episodes_id=series1)
    review_count = reviews.count()
    comment_count = comments.count()

    if 'savecomment' in request.POST:
        comment = request.POST["cmnt"]
        current_date = date.today()
        obj = comment_of_series.objects.create(user_comment=comment, review_date=current_date, user_id=user,
                                               episodes_id=series1)
        obj.save()
       
        return redirect('series', id2=id2)

    if 'savereview' in request.POST:
        title = request.POST["title"]
        review1 = request.POST["review"]
        rating = request.POST["rating"]
        current_date = date.today()
        obj = review_of_series.objects.create(review_title=title, user_review=review1, user_rating=rating,
                                               review_date=current_date, user_id=user,
                                               episodes_id=series1)
        obj.save()

        return redirect('series', id2=id2)

    episode = episodes.objects.get(id=id2)

    context = {
        'comment_count': comment_count,
        'review_count': review_count,
        'reviews': reviews,
        'comments': comments,
        'episode': episode,
    }
    return render(request, 'series.html', context)

def tv_shows_view(request):
    selected_item = None
    if request.method == 'POST':
        selected_item = request.POST['grade']
    latest_series = None
    oldest_series = None
    if selected_item == 'oldest':
        oldest_series = series.objects.order_by('id')
       
    else:
        latest_series = series.objects.order_by('-id')
    episodes1=review_of_series.objects.all()    

    for a in  episodes1:
        c = a.episodes_id.season_id.series_id.id

        print(c)
        

    

    context = {
      
        'oldest_series': oldest_series,
        'latest_series': latest_series
    }
    return render(request, 'all-series.html', context)





  
@login_required(login_url='signin')
def details(request, id1):
    seasons = season.objects.filter(series_id=id1)
    selected_season = 1

    if request.method == 'POST':
        selected_season = int(request.POST.get('selected_season', 1))
        
    episodess = episodes.objects.filter(season_id__series_id=id1)
    episodes_selected_season = episodes.objects.filter(season_id__series_id=id1, season_id__which_season=selected_season).order_by('which_episode')

    first_episode = None
    first_episode_rating = None
    first_season = season.objects.filter(series_id=id1, which_season=1).first()
    if first_season:
        first_episode = episodes.objects.filter(season_id=first_season).order_by('which_episode').first()
        if first_episode:
            first_episode_review = review_of_series.objects.filter(episodes_id=first_episode).first()
            if first_episode_review:
                first_episode_rating = first_episode_review.user_rating
    
    try:
        series_obj = series.objects.get(pk=id1)
        series_genre = series_obj.s_genre
    except series.DoesNotExist:
        series_genre = None

    u_id = request.session.get("user_ID")
    user = user_reg.objects.get(user__id=u_id)
    series1 = episodes.objects.get(id=id1)
    reviews = review_of_series.objects.filter(episodes_id=series1)
    comments = comment_of_series.objects.filter(episodes_id=series1)
    review_count = reviews.count()
    comment_count = comments.count()

    if 'savecomment' in request.POST:
        comment = request.POST["cmnt"]
        current_date = date.today()
        obj = comment_of_series.objects.create(
            user_comment=comment, review_date=current_date, user_id=user, episodes_id=series1
        )
        obj.save()
        return redirect('details', id1=id1)

    if 'savereview' in request.POST:
        title = request.POST["title"]
        review1 = request.POST["review"]
        rating = request.POST["rating"]
        current_date = date.today()
        obj = review_of_series.objects.create(
            review_title=title, user_review=review1, user_rating=rating, review_date=current_date, user_id=user, episodes_id=series1
        )
        obj.save()
        return redirect('details', id1=id1)

    context = {
        'seasons': seasons,
        'selected_season': selected_season,
        'episodess': episodess,
        'episodes_selected_season': episodes_selected_season,
        'first_episode': first_episode,
        'first_episode_rating': first_episode_rating,
        'series_genre': series_genre,
        'review_count': review_count,
        'comment_count': comment_count,
        'reviews': reviews,
        'comments': comments,
    }

    return render(request, 'details.html', context)




def contacts(request):
    return render(request,'contacts.html')
def footer(request):
    return render(request,'footer.html')
def interview(request):
    return render(request,'interview.html')
def live(request):
    return render(request,'live.html')
def pricing(request):
    return render(request,'pricing.html')
def privacy(request):
    return render(request,'privacy.html')

def searh(request):
    series_result=None
    movi_result=None
    if 'search' in request.POST:
        searchtxt=request.POST['tosearch']
        movi_result=movies.objects.filter(m_name__contains=searchtxt).order_by('-id')
        series_result=series.objects.filter(s_name__contains=searchtxt).order_by('-id')

    context={

        "movi_result":movi_result,
        'series_result':series_result


    } 
    return render(request,'search.html',context)

@login_required(login_url='signin')
def addToWatchlaterFromallmovies(request,id):
    data=movies.objects.get(id=id)
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=Watchlater_of_movies_and_series.objects.create(user_id=user,movies_id=data)
    obj.save()
    return redirect('movies')
@login_required(login_url='signin')
def add_To_Watchlater_From_all_Series(request,id):
    data=series.objects.get(id=id)
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=Watchlater_of_movies_and_series.objects.create(user_id=user,series_id=data)
    obj.save()
    return redirect('all-series')


@login_required(login_url='signin')
def add_To_Watchlater_From_Details(request, id):
    data = episodes.objects.get(id=id)
    u_id = request.session['user_ID']
    user = user_reg.objects.get(user__id=u_id)
    obj = Watchlater_of_movies_and_series.objects.create(user_id=user, episode_id=data)
    obj.save()
    return redirect('details', id1=data.season_id.series_id.id)




@login_required(login_url='signin')
def Remove_Watchlater(request,id):
    watch_remove=Watchlater_of_movies_and_series.objects.get(id=id)
    watch_remove.delete()
    return redirect('watchlater')

def watch_later(request):
   user_id = request.session.get("user_ID")
   reg = get_object_or_404(user_reg, user__id=user_id)
   watchlater_items = Watchlater_of_movies_and_series.objects.filter(user_id=reg)
   movies_watchlater = watchlater_items.filter(movies_id__isnull=False)
   series_watchlater = watchlater_items.filter(series_id__isnull=False)
   episodes_watchlater = watchlater_items.filter(episode_id__isnull=False)

 

      
   
   
 
   
    
   context = {
        'movies_watchlater': movies_watchlater,
        'series_watchlater': series_watchlater,
        'episodes_watchlater':episodes_watchlater,
        'selected_plan':selected_plan
    
    }
   
   return render(request, 'watchlater.html', context)



    