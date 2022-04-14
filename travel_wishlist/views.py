from django.shortcuts import render,redirect,get_object_or_404
from .models import Place
from .forms import NewPlaceForm
# Create your views here.
def place_list(request):

    if request.method == 'POST':
        #create new place
        form = NewPlaceForm(request.POST) #creating a form from data in the request
        place = form.save() #creating a model object from forms
        if form.is_valid():
            place.save()
            return redirect('place_list') #reloads homepage

    #querying the db
    places = Place.objects.filter(visited = False)

    new_place_form = NewPlaceForm()

    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})
#rendering -- combining a template of data

def about(request):
    author='Daria'
    about = 'My first Django project: list of place I have visited and want to visit'
    return render(request,'travel_wishlist/about.html',{'author': author, 'about':about} )

def places_visited(request):
    visited=Place.objects.filter(visited=True)
    return render(request,'travel_wishlist/visited.html', {'visited':visited})

def place_was_visited(request,place_pk):
    if request.method == 'POST':
        place =get_object_or_404(Place,pk=place_pk)
        place.visited = True
        place.save()

        return redirect('place_list')
