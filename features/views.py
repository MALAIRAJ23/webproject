
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
import nltk
import csv
from django.contrib.auth.decorators import login_required
nltk.download('vader_lexicon')
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    return render(request, 'features/home.html')

def feature(request):
    return render(request, 'features/feature.html')

def elements(request):
    return render(request, 'features/elements.html')

def soundscapes(request):
    return render(request, 'features/soundscapes.html')

def focus(request):
    return render(request, 'features/focus.html')

def socialmedia(request):
    return render(request, 'features/socialmedia.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))  # Redirect to the homepage after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'features/login.html')
import csv
import os
import random
from django.shortcuts import render
from django.http import JsonResponse
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize VADER
sia = SentimentIntensityAnalyzer()

# Define file paths for affirmations and manifestations
AFFIRMATION_CSV_PATHS = {
    'Lighthearted': r'features\templates\features\positive_affirmations_100.csv',
    'In the middle': r'features\templates\features\neutral_affirmations_100.csv',
    'A little overwhelmed': r"features\templates\features\negative_affirmations_100.csv"
}

MANIFESTATION_CSV_PATHS = {
    'Lighthearted': r'features\templates\features\positive_manifestation_100.csv',
    'In the middle': r'features\templates\features\positive_manifestation_100.csv',
    'A little overwhelmed': r'features\templates\features\negative_manifestation_100.csv'
}

def load_affirmations_or_manifestations(file_path):
    """
    Load affirmations or manifestations from the specified CSV file.
    It handles files with 'Affirmation' or 'Manifestation' headers.
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames  # Get the CSV headers

        # Check if either 'Affirmation' or 'Manifestation' exists in headers
        if 'Affirmation' in headers:
            return [row['Affirmation'].strip() for row in reader]
        elif 'Manifestation' in headers:
            return [row['Manifestation'].strip() for row in reader]
        else:
            return [] 

def process_journal_entry(request):
    if request.method == 'POST':
        journal_entry = request.POST.get('journal_entry')

        # Analyze the sentiment of the journal entry using VADER
        sentiment_scores = sia.polarity_scores(journal_entry)
        compound_score = sentiment_scores['compound']

        # Determine if the sentiment is positive, neutral, or negative
        if compound_score >= 0.05:
            mood = 'Lighthearted'
        elif compound_score > -0.05:
            mood = 'In the middle'
        else:
            mood = 'A little overwhelmed'

        # Load corresponding affirmations and manifestations based on the mood
        affirmations = load_affirmations_or_manifestations(AFFIRMATION_CSV_PATHS[mood])
        manifestations = load_affirmations_or_manifestations(MANIFESTATION_CSV_PATHS[mood])

        # Randomly select one affirmation and one manifestation
        selected_affirmation = random.choice(affirmations) if affirmations else "No affirmation available."
        selected_manifestation = random.choice(manifestations) if manifestations else "No manifestation available."

        # Pass the affirmation/manifestation to the result page
        context = {
            'affirmation': selected_affirmation,
            'manifestation': selected_manifestation,
            'mood': mood,
        }
        return render(request, 'features/result.html', context)

    return render(request, 'features/input.html')

def examboost(request):
    return render(request, 'features/examboost.html')

def activities(request):
    return render(request, 'features/activities.html')
