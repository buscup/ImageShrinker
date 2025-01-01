# Image Shrinker Web Application

## Overview

The Image Shrinker Web Application allows users to upload an image and resize it by removing specified numbers of rows and columns. This tool uses the Seam Carving algorithm to intelligently resize images while preserving important visual content. It supports both traditional file upload and drag-and-drop functionality.

## Features

Upload images using a form or drag-and-drop interface.

Specify the number of rows and columns to remove.

View the uploaded image immediately.

Download the processed image after resizing.

Error handling for invalid file uploads or processing issues.

## Requirements

- Python 3.7+
- Flask
- PIL (Pillow)
- NumPy

## Usage

Drag and drop an image file into the upload area or use the form to select a file.

Specify the number of rows and columns to remove.

View the uploaded image immediately.

Download the processed image after resizing.

## Project Structure

app.py: Main Flask application file.

seam_carver.py: Seam Carving algorithm implementation.

templates/: HTML templates for the web interface.

index.html: Main page for uploading and processing images.

download.html: Page for downloading processed images.

static/: Static files for styling and functionality.

css/style.css: Styling for the web application.

js/drag-and-drop.js: JavaScript for drag-and-drop functionality.

js/typewriter.js: JavaScript for typewriter effect.

uploads/: Folder for storing uploaded files.

processed/: Folder for storing processed images.

