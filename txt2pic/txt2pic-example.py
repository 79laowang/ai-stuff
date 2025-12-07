import requests
import json
import os
from urllib.parse import urlparse
from datetime import datetime

url = "https://open.bigmodel.cn/api/paas/v4/images/generations"

headers = {
    "Authorization": f"Bearer {os.environ.get('BIGMODEL_API_TOKEN')}",
    "Content-Type": "application/json"
}

data = {
    "model": "cogView-4-250304",
    "prompt": "一只可爱的小猫咪，坐在阳光明媚的窗台上，背景是蓝天白云.",
    "size": "1024x1024",
    "quality": "standard"
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    result = response.json()
    print("Success!")
    print(json.dumps(result, indent=2))

    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save the response metadata
    response_filename = f"bigmodel_response_{timestamp}.json"
    with open(response_filename, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResponse saved to {response_filename}")

    # Create pics directory if it doesn't exist
    os.makedirs("pics", exist_ok=True)

    # Download and save the image(s)
    if "data" in result and len(result["data"]) > 0:
        for i, image_data in enumerate(result["data"]):
            if "url" in image_data:
                # Download the image
                img_response = requests.get(image_data["url"])
                img_response.raise_for_status()

                # Determine file extension
                parsed_url = urlparse(image_data["url"])
                path = parsed_url.path
                file_extension = os.path.splitext(path)[1] or ".png"

                # Save the image to pics directory
                filename = f"pics/generated_image_{i}_{timestamp}{file_extension}"
                with open(filename, "wb") as f:
                    f.write(img_response.content)
                print(f"Image saved to {filename}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    if 'response' in locals():
        print(f"Response: {response.text}")
