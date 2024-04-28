from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .forms import SearchForm
from .models import Movie, User, Category
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from django.views.generic import View
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .serializers import (MovieSerializer, CategorySerializer ,RegisterSerializer, LoginSerializer, LogoutSerializer)


PAGE_SIZE_PER_CATEGORY = 20

@api_view(['GET', 'POST', 'DELETE'])
def index_view(request):
    categories_to_display = ['Action', 'Adventure', 'Anime', 'Tech', 'Romance', 'Thriller', 'Drama', 'Comedy', 'Fantasy', 'Crime', 'Mystery', 'Historical']
    data = {}
    for category_name in categories_to_display:
        movies = Movie.objects.filter(category__name=category_name)
        if request.method == 'POST':
            search_text = request.POST.get('search_text')
            movies = movies.filter(name__icontains=search_text)
        data[category_name] = movies[:PAGE_SIZE_PER_CATEGORY]

    search_form = SearchForm()
    return render(request, 'netflix/index.html', {
        'data': data.items(),
        'search_form': search_form
    })

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET", "POST"])
def movie_list(request):
    if request.method == 'GET':
        companies = Movie.objects.all()
        serializer = MovieSerializer(companies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET", "POST"])
def category_list(request):
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_movies_by_category(request, category_id):
    try:
        movies = Movie.objects.filter(category__id=category_id)
        movie_serializer = MovieSerializer(movies, many=True)
        data = {
            'movies': movie_serializer.data
        }
        return Response(data)
    except (Movie.DoesNotExist):
        raise NotFound("No movies or TV series found for the specified genre ID.")
