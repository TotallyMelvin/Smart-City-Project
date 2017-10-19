def get_google_url(search_loc, search_selections, webpage_identifer):
    ## This method will generate the google maps embeded link that can creaate the map functionality for the site
    search_base = ["https://www.google.com/maps/embed/v1/search?q=", "&key=AIzaSyCo8hPtObahI8239nap_CvlDo0mUTkqx6Q"]


    
    if webpage_identifer == 0: ## MapView/page
        search_input = [search_loc] + search_selections ## combine the data that is being input
    elif webpage_identifer == 1: ## AddBusinessDataView
        ## new string is to remove whitespace from any user input
        new_string = search_selections.replace(" " , ",+") 
        search_input = [search_loc] + [new_string]
    search_str = ',+'.join(search_input)
    searchable_link = search_base[0] + search_str + search_base[1]
    print(searchable_link)
    
    return searchable_link

    
