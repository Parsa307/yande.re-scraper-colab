import os
import requests
from urllib.parse import unquote
from IPython.display import display, HTML

# Ask user for a tag
TAG = input("Enter the tag: ").strip()

if not TAG:
    print("A tag is required.")
else:
    API_URL = f"https://yande.re/post.json?tags={TAG}"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        if not data:
            print("No images found.")
        else:
            # Create directory for the images
            directory = f"{TAG}"
            os.makedirs(directory, exist_ok=True)

            for post in data:
                image_url = post.get('jpeg_url')
                if image_url:
                    filename = unquote(image_url.split('/')[-1])
                    filepath = os.path.join(directory, filename)

                    # Download the image
                    img_data = requests.get(image_url).content
                    with open(filepath, 'wb') as f:
                        f.write(img_data)
                    print(f"Downloaded: {filename}")

            display(HTML(f"<b>All images saved in:</b> {directory}"))

    except requests.exceptions.RequestException as e:
        print("Error fetching images:", e)
