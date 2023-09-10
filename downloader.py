import os
import requests
from bs4 import BeautifulSoup

input_file = 'downloadme.txt'  # Replace with the path to your text file

# Define a function to download a file from a given URL and retain the correct filename
def download_file(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            titlePastebin = None
            try:
                titlePastebin = soup.find(class_='info-top').find('h1')
            except:
                pass

            titleRentry = None
            try:
                titleRentry = soup.find('title')
            except:
                pass

            if titlePastebin is not None:
                filename = titlePastebin.get_text()
                content = soup.find(class_='text').get_text()
            elif titleRentry is not None:
                filename = titleRentry.get_text()
                content = soup.find(attrs={"name": "description"}).get('content')
            elif 'content-disposition' in response.headers:
                content_disposition = response.headers['content-disposition']
                filename = content_disposition.split('filename=')[1].strip('"\'')                                  
            else:
                filename = os.path.basename(url)

            #Download the file and save it with the correct filename
            with open(filename + '_temp', 'w') as file:
                file.write(content)
            with open(filename + '_temp', 'r') as input_file, open(filename, 'w') as output_file:
                for line in input_file:
                    # Check if the line is not blank (contains non-whitespace characters)
                    if line.strip():
                        # Write the non-blank line to the output file
                        output_file.write(line)
            os.remove(filename + '_temp')
            print(f"Downloaded: {filename}")

        else:
            print(f"Failed to download: {url}, Status code: {response.status_code}")

    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

# Read URLs from a text file and download files sequentially
with open(input_file, 'r') as file:
    urls = file.read().splitlines()

for url in urls:
    download_file(url)