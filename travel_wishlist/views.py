from http.client import HTTPResponse
from urllib.error import HTTPError
from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

#add login decorator to all emthods
@login_required
def place_list(request):

    if request.method == 'POST':
        #create new place
        form = NewPlaceForm(request.POST) #creating a form from data in the request
        place = form.save(commit = False) #creating a model object from forms
        place.user = request.user
        if form.is_valid():
            place.save()
            return redirect('place_list') #reloads homepage

    #querying the db
    #that way each method contains info about the current user
    places = Place.objects.filter(user=request.user).filter(visited = False)

    form = NewPlaceForm()

    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': form})
#rendering -- combining a template of data

@login_required
def about(request):
    author='Daria'
    about = 'My first Django project: list of place I have visited and want to visit'
    return render(request,'travel_wishlist/about.html',{'author': author, 'about':about} )

@login_required
def place_was_visited(request,place_pk):
    if request.method == 'POST':
        place =get_object_or_404(Place,pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')

@login_required
def places_visited(request):
    visited=Place.objects.filter(visited=True)
    return render(request,'travel_wishlist/visited.html', {'visited':visited})

    
@login_required
def place_details(request,place_pk):
    #captured args will be privovided
    place = get_object_or_404(Place,pk=place_pk)
    #does this place belong to the current user
    if place.user != request.user:
        return HttpResponseForbidden()

    #is this a GET request (show data + form), or a POST request (update Place object)?
   
    #if it is a POST request, validate form data and update model
    if request.method == 'POST':
        #we will make the new TripReview Object from the data that was sent with Http request 
        #and we will put in user's data and use that to update the model instance from the db
        #form here encapsulating the users data
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            #save to update the TripReviewForm object with data provided
            form.save()
            #messages are a way of showing temporary messages to the user
            messages.info(request, 'Trip inofrmation updated')
        else:
            messages.info(request, form.errors)
        return redirect('place_details', place_pk = place_pk)

    else:
         #if it is a GET request, show Place info and form
         #if place is visited, show form, if the place is not visited then don't show the form 
        if place.visited:
            review_form = TripReviewForm(instance = place)
            #show form
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            #don't show form
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk = place_pk)
    if place.user == request.user:
        place.delete()
        #have to do a return
        return redirect('place_list')

    else:
        return HttpResponseForbidden()
