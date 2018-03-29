from cImage import *
import cluster
import sys
import math

def create_centroids(k, image, image_window):
    # This function asks the user to select k pixels with distinct RGB
    # values from the image and store them as centroids. 
    
    centroids = []
    
    # Prompt the user to pick k pixels with distinct RGB values from the image
    print("Select %s centroids by clicking on the image"%(k))
    
    for click in range(1, (int(k)+1)):
        
        # Store the spot clicked on as coordinates
        coordinates = image_window.getMouse()
        
        # Check if the coordinates already exist
        colours, coordinates = checkCoordinates(coordinates, centroids, image, image_window)
        
        # Display the coordinates of each centroid to the user
        print("Centroid %s: "%click, coordinates)
        
        # Store centroids' colours in a list
        colours = (int(colours[0]),int(colours[1]),int(colours[2])) 
        centroids.append(colours)
    
    # Feed out the list of pixel values of the chosen centroids 
    return centroids

def checkCoordinates(coordinates, centroids, image, image_window):
    
    # Convert each set of coordinates into a set of pixels
    colours = image.getPixel(coordinates[0],coordinates[1])
    
    # Check if a selected point has the same RGB values as any previous one
    for item in centroids:
        while colours[0] == item[0] and colours[1] == item[1] and colours[2] == item[2]:
            
            # If yes, prompt the user to choose another pixel
            print("That colour has already been picked, pick another")
            
            # Re-assign the new choice and check again if it already exists
            coordinates = image_window.getMouse()
            colours = image.getPixel(coordinates[0],coordinates[1])   
    
    return colours, coordinates

def create_data_file(image, width, height):
    
    # Create a dictionary to store all the image pixels
    pixelDictionary = {}
    
    # Create an index for the pixels to store them as a value in the key.
    pixelIndex = 0
    
    # Map out the coordinates of each image pixel.
    for row in range(height):
        for column in range(width):
            
            # Find the pixel at each given set of coordinates
            pixel = image.getPixel(row, column)
            
            # Add to the dictionary the pixel's index value as the key
            # And the RGB values as the key's value.
            pixelDictionary[pixelIndex] = (int(pixel[0]),int(pixel[1]),int(pixel[2]))
            
            # Increase the pixel's index count to reference the next pixel
            pixelIndex += 1        
    
    # Feed out the dictionary where all the image's pixel values are stored
    return pixelDictionary


def create_new_image(new_image, clusters, centroids, width, height):
    # This function creates a new image where each pixel has the colour 
    # value of its centroid and returns the new image.
    
    # Set up pixel index to reference each pixel
    index = 0
    
    # Map out the coordinates of each image pixel.
    for row in range(height):
        for col in range(width):
            
            # Get the original pixel
            for item in clusters:
                if index in item:
                    oldPixel = clusters.index(item)
                    
                    # Find the corresponding centroid
                    newPixel = centroids[oldPixel]
                    
                    # Round the corresponding centroid
                    newPixel = (round(newPixel[0]),round(newPixel[1]),round(newPixel[2]))
                    
                    # Set new pixel to the appropriate format
                    newPixel = Pixel(newPixel[0],newPixel[1],newPixel[2])
                    
                    # Replace original pixel with new pixel in the new image
                    new_image.setPixel(row, col, newPixel)

            # Increase the pixel's index count to reference the next pixel
            index += 1
    
    # Feed out the new image that's been generated
    return new_image

def compute_distance(clusters, centroids, dictionary):
    # This function computes the total distance and returns its value
    # which has been rounded to 2 digits beyond the decimal point in form
    # of a string.
    # The total distance is defined as the sum of all distances between
    # points and their centroids.
    
    # Create a variable to track the total distance
    total_dist = 0
    
    # For each cluster
    for i in range(len(clusters)):
        
        # For each pixel's index in a cluster
        for point in range(len(clusters[i])):
            
            # Retrieve the value of that pixel in the pixel index dictionary
            pt = dictionary.get(clusters[i][point])
            
            # Retrieve the centroid value that corresponds to that pixel
            centre = centroids[i]
            
            # Compute the distance between that pixel and its centroid
            # Tabulate that calculated distance to the distance total
            total_dist += math.sqrt(((centre[0] - pt[0])**2) + ((centre[1] - pt[1])**2) + ((centre[2] - pt[2])**2))
    
    # Send back the total distance between all the centroids and 
    # their grouped pixels and format the value to contain two decimal pts.
    return "%.2f"%(total_dist)

def display_image(imagename):
    # This function opens the image whose name is imagename and
    # displays it in a window which is the same size as the image
    # It also returns the image object as well as the window object.    

    # Create a variable to reference the cImage module
    img = FileImage(imagename)
    
    # Open a window displaying the image, with a width and heigh
    # equal to those of the image
    win = ImageWin('k-colouring',img.getWidth(),img.getHeight())
    
    # Display the image
    img.draw(win)
    
    # Feed out the variables associated to cImage and the image's window
    return img, win


def readCommandLineArgs():
    
    # Retrieving the file name of the image we want to process
    inputFile = sys.argv[1]
    
    # Set default number of clusters (k) and number of passes (iterations)
    k = 6
    iterations = 5
    
    # Check if a user manually inputs a number of clusters
    if len(sys.argv) > 2:
        
        # If yes, set the user's input value to the number of clusters 
        k = sys.argv[2]
    
    # Check if a user manually inputs an iteration value
    if len(sys.argv) > 3:
        
        # If yes, set the user's inputted value to the number of iterations
        iterations = sys.argv[3]
    
    # Feed out the created variables from the function
    return inputFile, k, iterations

def main():
    
    # Read and Process the command line arguments.
    (image_name, num_clusters, iterations) = readCommandLineArgs()

    # Read in the original image and display it.     
    image, image_window = display_image(image_name)

    # Get width and height of the original image.
    width = image.getWidth()
    height = image.getHeight()

    # Let the user click on k points of the image, store them as
    # centroids, and print x and y coordinates of them in k lines.    
    image_centroids = create_centroids(num_clusters, image, image_window)
    
    print('\nStarting clustering process')
    
    # Create data_file which is a dictionary with pixel indexes and also
    # the pixels as the values of the dictionary.
    data_file = create_data_file(image, width, height)

    # Make a new copy of the image in order to alter/create a new image.
    new_image = image.copy()
    
    # Set a variable that initiates the passes
    counter = 0
    
    while counter < int(iterations):
        clusters = []
        
        # Partition the color values in the image.
        # Each pixel is grouped in a cluster based on its closest centroid
        clusters = cluster.assignPointsToClusters(image_centroids, data_file)
        
        # Create a new image where each pixel has the colour value of its
        # centroid.        
        new_image = create_new_image(new_image, clusters, image_centroids, width, height)
        
        # Display the new image.
        new_image.draw(image_window)

        # Compute the distance between all the centroids and their pixels
        distance = compute_distance(clusters, image_centroids, data_file)
        
        # Print out the distance statement
        print("Total distance at pass %s: %s"%((counter+1),(distance)))

        # Compute new centroids based on the clusters.         
        image_centroids = cluster.updateCentroids(clusters, image_centroids, data_file)

        # Increase the counter to trigger another pass
        counter += 1
    
    # Save image to new file k_colours.gif
    new_image.save('k_colours.gif')

if __name__ == "__main__":
    main()
