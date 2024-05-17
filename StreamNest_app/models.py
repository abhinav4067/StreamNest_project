from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser



class Login(AbstractUser):
    userType = models.CharField(max_length=50, null=True)
    viewpassword = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username



   


class user_reg(models.Model):
    user=models.OneToOneField(Login,on_delete=models.CASCADE,null=True)
    u_name=models.CharField(max_length=50,null=True)
    u_email=models.EmailField(null=True)
    u_password=models.CharField(max_length=50,null=True)
   

class movies(models.Model):
    m_language=models.CharField(max_length=50)  
    m_name=models.CharField(max_length=50) 
    m_genre=models.CharField(max_length=50)
    m_file=models.FileField(null=True)
    m_actors=models.CharField(max_length=100)
    m_poster=models.ImageField(null=True)
    m_year=models.IntegerField(default=2024)
    m_age=models.IntegerField(default=16)
    m_description=models.CharField(max_length=1000,default="It was good movie........")
    m_plan=models.IntegerField(default=0)


class series(models.Model):
    s_language=models.CharField(max_length=50)   
    s_name=models.CharField(max_length=50) 
    s_genre=models.CharField(max_length=50)
    s_actors=models.CharField(max_length=100) 
    s_cover_pic=models.ImageField(null=True)

class season(models.Model):
    series_id=models.ForeignKey(series,on_delete=models.CASCADE)
    which_season=models.IntegerField(default=1)
    class Meta:
        unique_together = ('series_id', 'which_season',)

    def __str__(self):
        return f"{self.series_id.s_name} - Season {self.which_season}"


class episodes(models.Model):
    season_id=models.ForeignKey(season,on_delete=models.CASCADE)    
    e_cover_pic=models.ImageField(null=True)
    e_file=models.FileField(null=True)
    which_episode=models.IntegerField(default=1,null=True)
    episode_name=models.CharField(max_length=100) 


class review_of_movies(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    user_review=models.TextField(max_length=500,null=True)
    user_rating=models.IntegerField(default=0)
    review_date=models.DateField(null=True)
    movies_id=models.ForeignKey(movies,on_delete=models.CASCADE,null=True)
    review_like=models.IntegerField(null=True)  
      


class review_of_series(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    review_title=models.TextField(max_length=100,null=True)
    user_review=models.TextField(max_length=500,null=True)
    user_rating=models.IntegerField(default=0)
    review_date=models.DateField(null=True)
    episodes_id=models.ForeignKey(episodes,on_delete=models.CASCADE,null=True)
    review_like=models.IntegerField(null=True)     


class comment_of_series(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    user_comment=models.TextField(max_length=500,null=True)
    review_date=models.DateField(null=True)
    episodes_id=models.ForeignKey(episodes,on_delete=models.CASCADE,null=True)


class Watchlater_of_movies_and_series(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    movies_id=models.ForeignKey(movies,null=True,on_delete=models.CASCADE)
    series_id=models.ForeignKey(series,null=True,on_delete=models.CASCADE)
    episode_id=models.ForeignKey(episodes,null=True,on_delete=models.CASCADE)
      
class Plans(models.Model):
    selected_plan=models.IntegerField(default=0,null=True)
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    movies_id=models.ForeignKey(movies,null=True,on_delete=models.CASCADE)
    series_id=models.ForeignKey(series,null=True,on_delete=models.CASCADE)