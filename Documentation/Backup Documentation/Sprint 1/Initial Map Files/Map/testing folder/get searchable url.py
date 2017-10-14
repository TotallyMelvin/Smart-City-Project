

example = "https://www.google.com/maps/embed/v1/search?q=brisbane,+museum&key=AIzaSyCo8hPtObahI8239nap_CvlDo0mUTkqx6Q"

brisbane = "https://www.google.com/maps/embed/v1/search?q=brisbane&key=AIzaSyCo8hPtObahI8239nap_CvlDo0mUTkqx6Q"

str_input = ['brisbane', 'zoo', 'park']



def get_google_url(search_input):
    search_base = ["https://www.google.com/maps/embed/v1/search?q=", "&key=AIzaSyCo8hPtObahI8239nap_CvlDo0mUTkqx6Q"]
    search_str = ',+'.join(search_input)

    searchable_link = search_base[0] + search_str + search_base[1]
    print(search_str)
    print(searchable_link)


get_google_url(str_input)

        
    
