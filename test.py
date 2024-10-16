# import os
# import requests
# from litellm import completion
# import base64
#
#
# image_file_path = 'resized_image.jpg'
# image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg'
#
# # download and save image
# try:
#     img_data = requests.get(image_url).content
#     with open(image_file_path, 'wb') as handler:
#         handler.write(img_data)
# except Exception as e:
#     print(f"Failed to download image: {e}")
#     exit(1)
#
# llm_key = os.getenv("LLM_KEY")
# llm_base_url = os.getenv("LLM_BASE_URL")
#
# # Read the image and encode it in Base64
# with open(image_file_path, 'rb') as image_file:
#     encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
#
# # openai call
# response = completion(
#     model="openai/gpt-4o",
#     api_key=llm_key,
#     base_url=llm_base_url,
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": f"What's in this image?"},
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
#                 },
#             ],
#         }
#     ],
#     # prompt="Analyze the following image:",
#     # data={"image_base64": encoded_image},
#     # files=[
#     #     {
#     #         "file": open(image_file_path, "rb"),
#     #         "purpose": "fine-tune"
#     #     }
#     # ],
# )
#
# # print(response)
# print(response.choices[0].message.content)
