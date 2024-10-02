import pandas as pd  # type: ignore
import cv2  # type: ignore
import numpy as np  # type: ignore

# Load the color data from the CSV file
color_data_df = pd.read_csv('colors.csv')

# Print out the columns for debugging
print("Columns in the CSV file:", color_data_df.columns)

# Strip any whitespace and normalize to uppercase
color_data_df.columns = color_data_df.columns.str.strip().str.upper()
print("Cleaned Columns:", color_data_df.columns)

# Map your actual column names to R, G, B, and COLOR_NAME
color_data_df.rename(columns={
    '93': 'R',
    '138': 'G',
    '168': 'B',
    'AIR FORCE BLUE (RAF)': 'COLOR_NAME'  # Assuming this is the color name
}, inplace=True)

# Ensure that the required columns exist
required_columns = ['R', 'G', 'B', 'COLOR_NAME']
for col in required_columns:
    if col not in color_data_df.columns:
        raise KeyError(f"Column '{col}' not found in the cleaned CSV columns: {color_data_df.columns}")


# Function to detect color by clicking on an image
def detect_color_on_click(image_path):
    image = cv2.imread(image_path)

    # Function to calculate distance and return the closest color name
    def get_closest_color(r, g, b):
        min_dist = float('inf')
        closest_color = None
        for i, row in color_data_df.iterrows():
            dist = np.sqrt((r - row['R']) * 2 + (g - row['G']) * 2 + (b - row['B']) * 2)
            if dist < min_dist:
                min_dist = dist
                closest_color = row['COLOR_NAME']
        return closest_color

    # Mouse callback function
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            b, g, r = image[y, x]
            color_name = get_closest_color(r, g, b)
            print(f"Color at ({x}, {y}): {color_name}, RGB: ({r}, {g}, {b})")

    cv2.namedWindow('Image')  # Create a named window
    cv2.imshow('Image', image)  # Display image in the named window
    cv2.setMouseCallback('Image', mouse_callback)  # Set callback on the named window
    cv2.waitKey(0)  # Wait until a key is pressed
    cv2.destroyAllWindows()  # Close the window


# Example usage
if __name__ == "__main__":
    image_path = 'colorpic.jpg'  # Replace with your image file path
    detect_color_on_click(image_path)
