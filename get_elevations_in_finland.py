import requests

def get_elevations_in_finland(coordinates_list):
    '''Creates elevation matrix of floats from given border coordinates'''

    western = coordinates_list[0]
    eastern = coordinates_list[1]
    southern = coordinates_list[2]
    northern = coordinates_list[3]
    
    # Transform coordinates suitable to the URL    
    if western.find(".") == -1:
        western += "."
    if eastern.find(".") == -1:
        eastern += "."
    if southern.find(".") == -1:
        southern += "."
    if northern.find(".") == -1:
        northern += "."
    
    while len(western) < 17:
        western += "0"
    while len(eastern) < 17:
        eastern += "0"
    while len(southern) < 17:
        southern += "0"
    while len(northern) < 16:
        northern += "0"

    western = western.replace(".", "")
    western=  western[:6] + "." + western[6:]

    eastern = eastern.replace(".", "")
    eastern=  eastern[:6] + "." + eastern[6:]

    southern = southern.replace(".", "")
    southern =  southern[:7] + "." + southern[7:]

    northern = northern.replace(".", "")
    northern =  northern[:7] + "." + northern[7:]

    # Create URL
    base_url = "https://avoin-karttakuva.maanmittauslaitos.fi/ortokuvat-ja-korkeusmallit/wcs/v2?api-key="
    latitudes = f"({western},{eastern})"
    longitudes = f"({southern},{northern})"
    api_key = '' # Insert API key here as a string
    url = f"{base_url}{api_key}&service=WCS&version=2.0.1&request=GetCoverage&CoverageID=korkeusmalli_2m&SUBSET=E{latitudes}&SUBSET=N{longitudes}&format=text/plain&"

    # Extract web page's text content
    response = requests.get(url)
    if response.status_code != 200:
        print("Incorrect coordinates")
    text = response.text


    # Make text content rows into list and remove metadata, leave just elevation data
    rows = text.split("\n")
    rows = rows[6:len(rows)-2]

    # Make string list into float matrix
    elevations = []
    for row in rows:
        row = row[1:]
        row = row.replace("\r", "")
        string_row = row.split(" ")
        float_row = [float(x) for x in string_row]
        elevations.append(float_row)

    return elevations