from django.shortcuts import render
from interactive_map.forms import MapForm
from django.views.generic import TemplateView
from interactive_map.codesnippets import get_google_url ## to translate
                                        ## the user input into useable
                                        ## links for google



class MapView(TemplateView): ## the maps page of the website

    map_au_link = "https://www.google.com/maps/embed/v1/search?q=australia&key=AIzaSyCo8hPtObahI8239nap_CvlDo0mUTkqx6Q"
    template_name = 'map/main.html'

    def get(self, request):
        form = MapForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        
        form = MapForm(request.POST)
        if form.is_valid():
            search_location = form.cleaned_data['location']
            search_data = form.cleaned_data['selected_options']

        ## update the google link
        search_link_string = get_google_url(search_location, search_data)

        self.map_au_link = search_link_string
        
        ## return to the UI
        args = {'form': form, 'map_link': self.map_au_link}
        return render(request, self.template_name, args)
            
