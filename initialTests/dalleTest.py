#key = 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
from openai import OpenAI

client = OpenAI(
    api_key = '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'
)

print("Welcome to DALL·E image generator. Type a description and receive an image!")

while True:
    prompt = input("Enter an image description: ")
    if prompt:
        try:
            # Create an image based on the user's description
            response = client.images.generate(
                prompt=prompt,
                n=1,  # number of images to generate
                size="256x256"  # size of the image
            )

            # Assuming the API returns a list of generated images
            image_url_list = []
            image_data_list = []
            for image in response.data:
                image_url_list.append(image.model_dump()["url"])
                image_data_list.append(image.model_dump()["b64_json"])
            print(image_url_list)
            print(image_data_list)
           

            # Here you might add code to download the image and display it,
            # or simply instruct the user to visit the URL.

        except Exception as e:
            print(f"An error occurred: {e}")
