import webbrowser
import os

# Get the absolute path to the HTML file
html_path = os.path.abspath('index.html')
# Open the file in the default browser
webbrowser.open('file://' + html_path) 