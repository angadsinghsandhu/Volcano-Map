# imports
import folium as fl

# file handles
fhand = '''./Volcanoes_USA.txt'''
data = open(fhand).readlines()

# helper functions
def get_coordinates(text) :
    coordinates = []
    a = []
    elev = []
    for i in text :
        i = i.rstrip()
        arr = i.split(',')
        try :
            lat = float(arr[8])
            lon = float(arr[9])
            e = float(arr[5])
            a = [lat, lon]
        except ValueError:
            continue
        coordinates.append(a)
        elev.append(e)
    return (coordinates, elev)

def height_intensity(h):
    if h < 1000 :
        return 'green'
    elif h > 3000 :
        return 'red'
    else :
        return 'orange'

# getting coordinates
(lst, height) = get_coordinates(data)

map = fl.Map(location=[40,-100])  #creating a map object
fgv = fl.FeatureGroup(name='Volcanoes')

# lst = [[13.357,74.79], [13.356,74.79], [13.358,74.79], [13.357,74.80]]
for coordinate, ele in zip(lst, height):
    fgv.add_child(fl.CircleMarker(location=coordinate, radius=6, popup="Elevation = {}".format(ele),
    fill_color=height_intensity(ele), color='grey', fill_opacity=0.6))

#adding popurlation polygon using geoJSON
fgp = fl.FeatureGroup(name='Popurlation')
fh = '''D:/Code/Python/Courses/The Python Mega Course Build 10 Real World Applications/11 Application 2 Creating Webmaps with Python and Folium/world.json'''
dat = open(fh, encoding="utf-8-sig").read()

fgp.add_child(fl.GeoJson(data=dat,
style_function = lambda x: {
'fillColor' : 'green' if x['properties']['POP2005'] < 10000000  # lesser than 10,000,000
else 'red' if x['properties']['POP2005'] > 20000000     # greater than 20,000,000
else 'orange'
}))

# adding to map
map.add_child(fgv)
map.add_child(fgp)
map.add_child(fl.LayerControl())
map.save('./index.html')  #creating and saving maps in html
