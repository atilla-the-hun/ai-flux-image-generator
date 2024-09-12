import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import os
import uuid

from generate_image import generate_image

load_dotenv()

st.set_page_config(
    page_title="Art Machine AI",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure the images directory exists
IMAGES_DIR = "generated_images"
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

def save_image(image, format="PNG"):
    """Save image to disk and return the filename"""
    if format.upper() == 'JPG':
        format = 'JPEG'
    filename = f"{uuid.uuid4()}.{format.lower()}"
    filepath = os.path.join(IMAGES_DIR, filename)
    image.save(filepath, format=format.upper())
    return filename

def get_aspect_ratio(image):
    """Determine the aspect ratio of an image"""
    width, height = image.size
    ratio = width / height
    
    if 1.9 <= ratio < 2.3:
        return "21:9"
    elif 1.5 <= ratio < 1.9:
        return "16:9"
    elif 1.25 <= ratio < 1.5:
        return "3:2"
    elif 0.9 <= ratio < 1.25:
        return "1:1"
    elif 0.75 <= ratio < 0.9:
        return "4:5"
    elif 0.6 <= ratio < 0.75:
        return "2:3"
    elif 0.4 <= ratio < 0.6:
        return "9:16"
    else:
        return "9:21"

def load_images():
    """Load all images from the images directory"""
    images = {'1:1': [], '16:9': [], '21:9': [], '3:2': [], '2:3': [], '4:5': [], '5:4': [], '9:16': [], '9:21': []}
    for filename in os.listdir(IMAGES_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            filepath = os.path.join(IMAGES_DIR, filename)
            img = Image.open(filepath)
            aspect_ratio = get_aspect_ratio(img)
            if aspect_ratio in images:
                images[aspect_ratio].append((filename, img))
    return images

# Streamlit app
col1, col2 = st.columns([18, 1])
with col1:
    st.markdown(
        """
        
            <h1 style="margin-top: -24px;">Art Machine AI</h1>
        
        """,
        unsafe_allow_html=True
    )

st.subheader("Generate images with AI")

# Sidebar
st.sidebar.title("Settings")

# Add dropdown boxes in the sidebar
num_outputs = st.sidebar.number_input("Number of Outputs", value=1, min_value=1, max_value=4, step=1)
aspect_ratio = st.sidebar.selectbox("Aspect Ratio", ["1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "9:16", "9:21"], index=0)
output_format = st.sidebar.selectbox("Output Format", ["jpg", "png", "webp"], index=0)
output_quality = st.sidebar.number_input("Output Quality", value=100, min_value=0, max_value=100, step=1)

# Add Reset button to the sidebar
if st.sidebar.button("Reset"):
    # Clear session state
    st.session_state.clear()
    st.sidebar.success("Page has been reset. Your generated images are still available in the showcase.")

# Main content area
prompt = st.text_input("Enter a prompt then scroll to the bottom:", value=" ")

# Generate Image button
if st.button("Generate Image"):
    with st.spinner("Generating image..."):
        generated_images, elapsed_time = generate_image(prompt, num_outputs, aspect_ratio, output_format, output_quality)
        st.write(f"Image generated in {elapsed_time:.2f} seconds")
        
        # Save generated images to disk and update session state
        st.session_state.full_size_images = []
        for img in generated_images:
            filename = save_image(img, format=output_format)
            st.session_state.full_size_images.append((img, filename))

# Display images by aspect ratio
st.subheader("Image Showcase")
saved_images = load_images()
has_images = any(images for images in saved_images.values())

if has_images:
    for ratio, images in saved_images.items():
        if images:
            st.subheader(f"Aspect Ratio: {ratio}")
            columns = st.columns(4)  # Create 4 columns for the grid
            for i, (filename, img) in enumerate(images):
                with columns[i % 4]:
                    # Create a unique key for each image
                    key = f"img_{i}_{ratio}"
                    # Display thumbnail without the fullscreen hover icon
                    st.image(img, width=100, use_column_width=True)
                    # Create a button that when clicked will open the full-size image
                    button_col = st.columns([1, 2, 1])  # Create three columns for centering
                    with button_col[1]:  # Use the middle column
                        if st.button("Full Size", key=key, help="Click to view the full-size image"):
                            st.session_state.full_size_images = [(img, filename)]

else:
    st.write("No images generated yet.")

# Automatically display the full-size images if new ones were generated
if st.session_state.get('full_size_images', []):
    for img, filename in st.session_state.full_size_images:
        st.image(img, use_column_width=True)
        # Add download button for the full-size image
        img_byte_arr = BytesIO()
        save_format = 'JPEG' if output_format.lower() == 'jpg' else output_format.upper()
        img.save(img_byte_arr, format=save_format)
        img_byte_arr = img_byte_arr.getvalue()

        st.download_button(
            label="Download Full Size Image",
            data=img_byte_arr,
            file_name=filename,
            mime=f"image/{output_format}"
        )
else:
    st.write("No images generated yet.")

# Adding custom CSS to remove fullscreen icon on hover and move buttons slightly to the right
st.markdown(
    """
    <style>
    /* Remove fullscreen icon when hovering over images */
    button[title="View fullscreen"] {
        display: none !important;
    }
    /* Move buttons slightly to the right */
    .stButton button {
        margin-left: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)































# Create columns (removed the image on the right)
#left_col, right_col = st.columns([3, 1])
# With the right column no longer containing an image, you can add other content if needed

# Image to Prompt
#if current_page == "Image to Prompt":
    #image_to_prompt()

# Remove Background
#if current_page == "Remove Background":
    #remove_background()