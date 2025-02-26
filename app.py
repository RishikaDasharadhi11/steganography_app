import cv2
import numpy as np
import streamlit as st

# Encoding function
def encode_message(image, message, password):
    d = {chr(i): i for i in range(256)}
    n, m, z = 0, 0, 0
    
    for i in range(len(message)):
        image[n, m, z] = d.get(message[i], 0)
        n = (n + 1) % image.shape[0]
        m = (m + 1) % image.shape[1]
        z = (z + 1) % 3

    return image, password

# Decoding function
def decode_message(image, password, user_password, message_length):
    if password and user_password != password:
        return "❌ Incorrect password!"
    
    c = {i: chr(i) for i in range(256)}
    n, m, z = 0, 0, 0
    message = ""

    for i in range(message_length):
        pixel_value = int(image[n, m, z])
        message += c.get(pixel_value, "")
        n = (n + 1) % image.shape[0]
        m = (m + 1) % image.shape[1]
        z = (z + 1) % 3

    return f"🔓 Decrypted Message: {message}"

# Streamlit App
def main():
    st.set_page_config(page_title="🔐 Secret Image Steganography", layout="wide")

    # Custom CSS for Styling
    st.markdown(
        """
        <style>
            body {
                background-color: #121212;
                color: #fff;
            }
            .stApp {
                background: linear-gradient(135deg, #2C2C2C, #1E1E1E);
                color: white;
            }
            .title {
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                color: #FF5733;
            }
            .subtitle {
                text-align: center;
                font-size: 18px;
                color: #FFB266;
            }
            .upload-section {
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
            }
            .image-box {
                border: 2px solid #FF5733;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
            }
            .stButton > button {
                width: 100%;
                border-radius: 8px;
                background-color: #FF5733;
                color: white;
                font-weight: bold;
                padding: 10px;
            }
            .stButton > button:hover {
                background-color: #FF2E00;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Cool Caption on App Load
    st.markdown("<h1 class='title'>🔒 Hide Secrets in Images! 🔒</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Choose an action to proceed.</p>", unsafe_allow_html=True)

    # Store user choice in session state
    if "previous_choice" not in st.session_state:
        st.session_state.previous_choice = None
    if "image_uploaded" not in st.session_state:
        st.session_state.image_uploaded = None

    # User choice: Encrypt or Decrypt
    choice = st.radio("Select an option:", ["🔏 Encrypt an Image", "🔓 Decrypt an Image"])

    # Reset image if user changes choice after encryption
    if st.session_state.previous_choice and st.session_state.previous_choice != choice:
        st.session_state.image_uploaded = None
        st.warning("⚠️ You changed the action! Please upload the image again.")

    st.session_state.previous_choice = choice  # Update choice

    if choice:
        # File uploader prompt
        with st.container():
            st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("📂 Upload an image to process", type=["jpg", "png"], key=choice)
            st.markdown("</div>", unsafe_allow_html=True)

        if uploaded_file:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
            st.session_state.image_uploaded = image  # Store uploaded image in session state

            # Layout with two columns
            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown("<div class='image-box'>", unsafe_allow_html=True)
                st.image(image, caption="📷 Uploaded Image", width=150)
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                if choice == "🔏 Encrypt an Image":
                    st.subheader("🔏 Encrypt a Message")
                    message = st.text_area("Enter your secret message:")
                    password = st.text_input("Set a password (optional):", type="password")

                    if st.button("🔒 Encrypt"):
                        if not message:
                            st.warning("⚠️ Please enter a message to encrypt!")
                        else:
                            encoded_image, set_password = encode_message(image.copy(), message, password)
                            cv2.imwrite("encrypted_image.png", encoded_image)
                            st.success("✅ Message encrypted successfully!")

                            # Display encrypted image below original (small size)
                            st.markdown("<div class='image-box'>", unsafe_allow_html=True)
                            st.image("encrypted_image.png", caption="🛡️ Encrypted Image", width=150)
                            st.markdown("</div>", unsafe_allow_html=True)

                            # Download button
                            st.download_button("⬇️ Download Encrypted Image", data=open("encrypted_image.png", "rb").read(), file_name="encrypted_image.png")

                elif choice == "🔓 Decrypt an Image":
                    st.subheader("🔓 Decrypt a Message")
                    password_input = st.text_input("Enter the decryption password (if set):", type="password")
                    msg_length = st.number_input("Enter the message length:", min_value=1, step=1)

                    if st.button("🔓 Decrypt"):
                        decrypted_message = decode_message(image, password="", user_password=password_input, message_length=msg_length)
                        if "🔓" in decrypted_message:
                            st.success(decrypted_message)
                        else:
                            st.error(decrypted_message)

if __name__ == "__main__":
    main()
