# ------------------------------------------
# Practice Project: Drawing a USA Map
# ------------------------------------------

import matplotlib.pyplot as plt

usa_map_file = "USA_Counties_555x352.png"

try:
    # Read the image
    img = plt.imread(usa_map_file)

    # Create a figure and plot the image
    plt.figure(figsize=(10, 7))
    plt.imshow(img)
    plt.title("County-level Map of USA")
    plt.axis("off")  # Hide axes

    # ----------------------------------------
    # OPTIONAL: Add scatter points to test overlay
    # Example: center of map and Rice University
    # ----------------------------------------
    # Center point (approximate for 555x352 image)
    center_x = 555 // 2
    center_y = 352 // 2
    plt.scatter(center_x, center_y, color="red", s=50, label="Center of Map")

    # Rice University (approximate pixel coords)
    rice_x = 335
    rice_y = 260
    plt.scatter(rice_x, rice_y, color="blue", s=50, label="Rice University")

    plt.legend(loc="lower left")

    # Show the plot
    plt.show()

except FileNotFoundError:
    print("Error: Could not find the USA map image file.")
    print("Please download 'USA_Counties_555x352.png' and put it in this folder.")
