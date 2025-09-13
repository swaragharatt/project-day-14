# project-day-14
# QR Code Generator

A **Python desktop tool** that lets you generate and customize QR codes with **zero coding required**.  
Built with a sleek dark theme, this app makes QR code creation **simple, visually appealing, and beginner-friendly**.

---

## Features  

-  Generate QR codes from text or URLs  
-  Choose from **Simple, Rounded, or Gradient** styles  
-  Customize **QR color, background, and size**  
-  Live preview of the QR code within the app  
-  Save generated QR codes directly as **PNG files**  
-  Dark-themed modern GUI with purple accents  

---

## Technologies Used  

- **Python 3** – Core programming language  
- **qrcode** – QR code generation  
- **Pillow (PIL)** – Image processing and preview  
- **tkinter** – GUI framework  
- **ttk** – Modern themed widgets  

---

## Project Structure  

qr-code-generator/  
│── qr_generator.py   # Main Python script  
│── README.md         # Documentation  

---

## How to Run  

1. Clone the repository.  
2. Install dependencies:  
   ```bash
   pip install qrcode[pil] pillow
Run the script:

bash
Copy code
python qr_generator.py
Enter text or a URL in the input box.

Select a QR code style (Simple, Rounded, Gradient).

Customize color, background, and size as needed.

Click "Generate QR" to preview.

Click "Save QR" to store the image as a PNG file.

Example
Input text/URL:

Copy code
(https://youtu.be/xvFZjo5PgG0?si=6uNmcQebihM5pcQ5)

Options chosen:

Style: Rounded

QR Color: #9D4EDD

Background: #0D0D0D

Size: 10

## Output:

![Uploading Screenshot 2025-09-13 194816.png…]()


Author
Swara Gharat
