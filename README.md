# Steganography App
## Overview
This project is a Streamlit-based web application that allows users to hide secret messages within images using steganography. The app provides two main functionalities:

## Encrypt an Image: 
Users can upload an image, enter a secret message, and optionally set a password to encrypt the message into the image.

## Decrypt an Image: 
Users can upload an encrypted image, enter the password (if set), and specify the message length to decrypt the hidden message.

The application uses basic steganography techniques to encode and decode messages within the pixel values of the image.

## Features
* User-Friendly Interface: The app is designed with a clean and intuitive interface, making it easy for users to navigate and use.
* Password Protection: Users can optionally set a password to protect their encrypted messages.
* Image Upload: Supports uploading images in JPG and PNG formats.
* Real-Time Encryption/Decryption: The app processes the image and message in real-time, providing immediate feedback.
* Download Encrypted Image: After encryption, users can download the image with the hidden message.

## Dependencies
* Streamlit: For building and running the web application.
* OpenCV: For image processing and manipulation.
* NumPy: For handling image data as arrays.

Enjoy hiding your secrets in images! 🔐🖼️
