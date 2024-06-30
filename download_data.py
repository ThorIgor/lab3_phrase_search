import os
import requests

def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    filename = os.path.join(dest_folder, url.split("/")[-1])
    if filename in os.listdir(dest_folder):
        return filename
    print(f"Downloading {filename} from {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return filename

urls = [
    "https://www.gutenberg.org/cache/epub/6593/pg6593.txt",
    "https://www.gutenberg.org/cache/epub/5197/pg5197.txt",
    "https://www.gutenberg.org/cache/epub/345/pg345.txt",
    "https://www.gutenberg.org/cache/epub/100/pg100.txt",
    "https://www.gutenberg.org/cache/epub/1342/pg1342.txt",
    "https://www.gutenberg.org/cache/epub/84/pg84.txt",
    "https://www.gutenberg.org/cache/epub/2701/pg2701.txt",
    "https://www.gutenberg.org/cache/epub/145/pg145.txt",
    "https://www.gutenberg.org/cache/epub/6761/pg6761.txt",
    "https://www.gutenberg.org/cache/epub/4085/pg4085.txt"
]

if __name__ == "__main__":
    for url in urls:
        download_file(url, "input")
