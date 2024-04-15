import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np
import numpy as np
import pandas as pd
# from matplotlib.widgets import Slider

 

def create_slider(elevation_data, year, index):
    '''Creates the slider, takes the elevation data matrix as parameter'''
    # Change matrix to a numpy array
    data_array = np.array(elevation_data)
    # Get predictions
    df = pd.read_csv('data/sea_level_predictions.csv', header=None, names=['Year', 'Sea Level'], skiprows=1)
    df['Sea Level'] = df['Sea Level'].astype(float)

   
    # Finding new value based on new year
    new_value = df[df['Year'] == int(year)]['Sea Level'].iloc[0]
    #Updating the elevation matrix
    updated_elevation_data = data_array - new_value

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_aspect('equal')  # Set aspect ratio to be equal to minimize background
    

    # Pick threshold elevations and colors for elevations 
    colormaps = ListedColormap(['royalblue','dodgerblue','deepskyblue',[0.0, 0.7529411764705882, 0.5333333333333333], [0.00784313725490196, 0.8, 0.4], [0.11372549019607843, 0.8196078431372549, 0.4196078431372549], [0.23529411764705882, 0.8470588235294118, 0.4470588235294118], [0.3333333333333333, 0.8666666666666667, 0.4666666666666667], [0.44313725490196076, 0.8862745098039215, 0.48627450980392156], [0.5529411764705883, 0.9098039215686274, 0.5098039215686274], [0.6627450980392157, 0.9294117647058824, 0.5294117647058824], [0.7725490196078432, 0.9529411764705882, 0.5529411764705883], [0.8823529411764706, 0.9764705882352941, 0.5764705882352941], [0.9921568627450981, 0.996078431372549, 0.596078431372549], [0.9490196078431372, 0.9333333333333333, 0.5686274509803921], [0.8941176470588236, 0.8627450980392157, 0.5411764705882353], [0.8392156862745098, 0.792156862745098, 0.5098039215686274], [0.7843137254901961, 0.7215686274509804, 0.4823529411764706], [0.7294117647058823, 0.6509803921568628, 0.45098039215686275], [0.6745098039215687, 0.5803921568627451, 0.4235294117647059], [0.6196078431372549, 0.5098039215686274, 0.39215686274509803], [0.5647058823529412, 0.4392156862745098, 0.36470588235294116], [0.5098039215686274, 0.37254901960784315, 0.3333333333333333], [0.5450980392156862, 0.41568627450980394, 0.38823529411764707]])
    normalization = BoundaryNorm([-10000, 0, 0.1, 0.2, 1,3,5,7,9,11,13,15,17,19,21,23,25,25,27,29,31], ncolors=24)

    # Display the image
    img = ax.imshow(updated_elevation_data, cmap=colormaps,norm=normalization)

    # Create colorbar with white edges
    cbar = plt.colorbar(img, ax=ax, shrink=1.0)
    cbar.set_label('Elevation (m)', color='white')  # Set the color of the label
    cbar.outline.set_edgecolor('white')  # Set the color of the colorbar outline
    
    # Set the color of the tick labels to white
    cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    
    # Set the color of the minor ticks to white
    cbar.ax.yaxis.set_tick_params(color='white', which='both', length=5)
    
    # Set the color of the map edges to white
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    
    # Set alpha channel to make background transparent
    fig.patch.set_alpha(0)

    # Matplotlib slider if application is used in terminal

    # Add a slider for changing values
    # ax_value = plt.axes([0.25, 0.1, 0.65, 0.03])
    # year_slider = Slider(
    #     ax=ax_value,
    #     label='Year',
    #     valmin=2024,
    #     valmax=2320,
    #     valstep=1,
    #     valinit=2024,
    # )

    # Function to update matrix values when slider is changed
    # def update(val):
    #     new_year = int(val) 
    #     # Finding new value based on new year
    #     new_value = df[df['Year'] == new_year]['Sea Level'].iloc[0]
    #     # Updating the elevation matrix
    #     updated_image = data_array - new_value 
    #     img.set_data(updated_image)  # Update the displayed image
    #     fig.canvas.draw_idle()

    # # Connect slider to update function
    # year_slider.on_changed(update)
    
    # Remove x and y ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Manually adjust the height of the colorbar to match the height of the map
    ax_pos = ax.get_position()
    cbar.ax.set_position([ax_pos.x1 + 0.01, ax_pos.y0, 0.03, ax_pos.height])

    filename = 'static/images/map' + index + '.png'
    plt.savefig(fname=filename, bbox_inches='tight', pad_inches=0)  # Use bbox_inches='tight' to tightly fit the plot and pad_inches=0 to remove padding
    plt.close(fig)  # Close the figure to avoid memory leaks
    
    return filename
    
    # plt.show()
    
