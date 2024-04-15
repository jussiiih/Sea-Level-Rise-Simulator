import input_coordinates
import get_elevations_in_finland
import year_slider


coordinates = input_coordinates.input_coordinates()

elevations = get_elevations_in_finland.get_elevations_in_finland(coordinates)

year_slider.create_slider(elevations)
