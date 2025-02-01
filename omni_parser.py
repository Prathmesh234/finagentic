'''
We will use this as our omniparser file. 

'''
import matplotlib.pyplot as plt
import time
import cv2
import ast
from gradio_client import Client, handle_file
def initiate_parser(screenshot_path):
    client = Client("microsoft/OmniParser")
    result = client.predict(
		image_input=handle_file(screenshot_path),
		box_threshold=0.05,
		iou_threshold=0.1,
		api_name="/process"
    )
    return result
def plot_boxes(result, image_path):
    # Load image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for proper visualization in matplotlib

# Bounding boxes as a string (converted from JSON or printed dictionary)
    bounding_boxes_str = result
# Convert bounding boxes string to dictionary
    bounding_boxes = ast.literal_eval(bounding_boxes_str)  # Safely parse the dictionary

# Get image dimensions
    img_height, img_width, _ = image.shape

# Draw bounding boxes
    for key, (x, y, w, h) in bounding_boxes.items():
        x1, y1 = int(x * img_width), int(y * img_height)
        x2, y2 = int((x + w) * img_width), int((y + h) * img_height)

    # Draw rectangle on image
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue box with thickness 2
        cv2.putText(image, f"ID {key}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Show image
    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()
   


def main():
    screenshot_path = 'resources/screenshot.png'
    result = initiate_parser(screenshot_path)
    print(type(result))
    plot_boxes(result, screenshot_path)

if __name__ == "__main__":
    main()