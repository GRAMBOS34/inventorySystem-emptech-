# QR Code Inventory System

Made for EMPTECH because the qrcode api of google is deprecated and I couldn't think of a better solution

> _Maybe it's more accurate to say that i just didn't want to deal with google forms and sheets_

# Installation

1. Make sure you have Python and pip installed

   Links:

   Python - https://www.python.org/downloads/

   pip (tutorial) - https://www.youtube.com/watch?v=fJKdIf11GcI&ab_channel=TheCodeCity

2) Make sure you launch the terminal (command prompt) in the project folder

   ```
   cd (your project folder)
   ```

3) Run this command in the terminal

   ```
   py -m pip install -r requirements.txt
   ```

4) Run this for setup

   ```
   py setup.py
   ```

5) Run this to run the server

   ```
   py main.py
   ```

6) Run this if you would like to add more books or users
   ```
   py qrCodeGenerate.py
   ```

# Notes

1. Don't delete any of the images in the qrcodes folder when you install it

2. This'll only work if all devices are on the same network

3. Set your network to private (Go to settings > Network & Internet > Properties (of your network) > Network Profile)
