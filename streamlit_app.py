import streamlit as st
import base64
import requests
import os

def generate_image(text_prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
      "steps": 40,
      "width": 1024,
      "height": 1024,
      "seed": 0,
      "cfg_scale": 5,
      "samples": 1,
      "style_preset": "photographic",
      "text_prompts": [
        {
          "text": text_prompt,
          "weight": 1
        },
        {
          "text": "blurry, bad",
          "weight": -1
        }
      ],
    }

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": "sk-sjF5Jp2SUiywg8IlGvUSsJlDLd1OPtLIRneprV5fN5dBASRW",
    }

    response = requests.post(
      url,
      headers=headers,
      json=body,
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    # make sure the out directory exists
    if not os.path.exists("./out"):
        os.makedirs("./out")

    if "caldas" in text_prompt.lower():
        return "unique_name_message"
    
    image = data["artifacts"][0]
    with open(f'./out/txt2img_{image["seed"]}.png', "wb") as f:
        f.write(base64.b64decode(image["base64"]))
    return f'txt2img_{image["seed"]}.png'

def main():
    st.title("Text to Image Generator")

    st.write("This app generates images based on given text prompts.")

    text_prompt = st.text_input("Enter text prompt")

    if st.button("Generate Image"):
        if text_prompt:
            generated_image = generate_image(text_prompt)
            if generated_image == "unique_name_message":
                st.error("We could not find an image that matches your search.")
            else:
                st.image(f'./out/{generated_image}', caption='Generated Image', use_column_width=True)
                st.success("Image generated successfully!")
        else:
            st.warning("Please enter a text prompt.")

if __name__ == "__main__":
    main()
