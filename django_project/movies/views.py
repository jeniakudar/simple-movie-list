from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required

from .models import Movie, Photo
from .forms import MovieForm, ImageForm, SignUpForm, DriverForm


@login_required(login_url='login')
def movie_read(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_read.html', {'movies': movies})


def movie_description(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    photos_list = movie.photo_set.all()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            photo.movie = movie
            #import pdb
            #pdb.set_trace()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            photo.save()
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    return render(request, 'movies/movie_description.html', {'movie': movie, 'photos': photos_list})


@login_required(login_url='login')
def movie_search(request):
    movies = Movie.objects.contains(request.GET['q'])
    return render(request, 'movies/movie_read.html', {'movies': movies})


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        driver_form = DriverForm(request.POST)
        if user_form.is_valid() and driver_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            driver_form = DriverForm(request.POST, instance=user.driver)
            driver_form.full_clean()
            driver_form.save()
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        user_form = SignUpForm()
        driver_form = DriverForm()
    return render(request, 'movies/sign_up.html', {
        'user_form': user_form,
        'driver_form': driver_form
})


def save_movie_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            movies = Movie.objects.all()
            data['html_movie_read'] = render_to_string('movies/partial_movie_read.html', {
                'movies': movies
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
    else:
        form = MovieForm()
    return save_movie_form(request, form, 'movies/movie_create.html')


def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
    else:
        form = MovieForm(instance=movie)
    return save_movie_form(request, form, 'movies/movie_update.html')


def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    data = dict()
    if request.method == 'POST':
        movie.delete()
        data['form_is_valid'] = True
        movies = Movie.objects.all()
        data['html_movie_read'] = render_to_string('movies/partial_movie_read.html', {
            'movies': movies
        })
    else:
        context = {'movie': movie}
        data['html_form'] = render_to_string('movies/movie_delete.html', context, request=request)
    return JsonResponse(data)


def remove_photo(request, pk):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))
