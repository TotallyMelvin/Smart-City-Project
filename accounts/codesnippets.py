
###############################
## Jamie Section Start
###############################

def get_google_url(search_loc, search_selections, webpage_identifer):
    ## Creator: Jamie Kostaschuk
    ## Description: This method will generate the google maps embeded
    ## link that can creaate the map functionality for the site
    ## the link will be based on the search_loc (location and search_selections inputs
    ## the webpage_identifier tells the function how to parse the inputs
    ##      because the different webpages pass their data to this form differently.
    ## Webpage Identifiers:
    ##      0 = Map Page
    ##      1 = Business Data Page

    ## base weblink parts that will be used to genete the links. these 2 aspects will be combined
    ## with the search location and search selections in between them to create the link
    search_base = ["https://www.google.com/maps/embed/v1/search?q=", "&key=AIzaSyCo8hPtObahI8239nap_CvlDo0mUTkqx6Q"]


    
    if webpage_identifer == 0: ## MapView/page
        search_str = ',+'.join(search_selections)
        search_input = search_str + '+in+' + search_loc ## combine the data that is being input
        
    elif webpage_identifer == 1: ## AddBusinessDataView
        ## remove whitespace from any user input
        new_string = search_selections.replace(" " , ",+")
        search_str = ',+'.join([new_string])
        search_input = search_str + '+in+' + search_loc ## combine the data that is being input
    
    ## create the link
    searchable_link = search_base[0] + search_input + search_base[1]
    
    return searchable_link

    
###############################
## Jamie Section End
###############################
