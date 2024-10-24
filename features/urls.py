from django.urls import path
from .views import home,feature,soundscapes,focus,socialmedia,process_journal_entry,elements,examboost,activities
urlpatterns = [
  
    path('', home, name='home'),
    path('feature/', feature , name='feature'),
    path('soundscapes/', soundscapes, name='soundscapes'),
    path('focus/', focus, name='focus'),
    path('socialmedia/', socialmedia, name='socialmedia'),
    path('input/', process_journal_entry, name='process_journal_entry'),
    path('elements/', elements, name='elements'),
    path('examboost/', examboost, name='examboost'),
    path('activities/', activities, name='activities'),
 
]
