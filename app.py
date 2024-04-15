import os
import input_coordinates
import get_elevations_in_finland
import year_slider


from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# route for showing the map
@app.route('/map', methods=['POST', 'GET'])
def map():
   data = request.json # Get JSON data from the request body
   latitude = data['latitude']
   longitude = data['longitude']
   zoom = data['zoom']
   year_value = data['myRange']
   with open('index.txt', 'r') as file:
      index = int(file.read())
   index = str(index + 1)
   with open('index.txt', 'w') as file:
      file.write(index)

   # Send coordinates to the scripts
   coordinates = input_coordinates.transform_coordinates(latitude, longitude, zoom)
   elevations = get_elevations_in_finland.get_elevations_in_finland(coordinates)
   img_name = year_slider.create_slider(elevations, year_value, index)


   # Send a response back to the html page
   response_data = {'image_url': img_name}
   
   # Remove old map.png files after drawing new map from @map function
   directory = 'static/images/'
   file_name = f"map{int(index)-2}.png"
   file_path = os.path.join(directory, file_name)

   if os.path.exists(file_path):
      os.remove(file_path)
   return jsonify(response_data)


if __name__ == '__main__':
   with open('index.txt', 'w') as file:
      file.write("1")
   app.run()
   
