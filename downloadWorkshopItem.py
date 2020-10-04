import requests
import os
import wget
from steamAPIAuth import SteamAPIAuth

__BASE_API_URL = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1"

def downloadItem(auth : SteamAPIAuth, id : str, outputDir : str, overwrite : bool = False) :
	if not os.path.isdir(outputDir):
		raise OSError(f"Output directory {outputDir} does not exist.")

	headers = \
	{
		"x-webapi-key": auth.apiKey
	}

	postData = \
	{
		"itemcount": 1,
		"publishedfileids[0]": id,
	}

	print("Making request for workshop item:", id)

	result = requests.post(url=__BASE_API_URL, data=postData, headers=headers)

	if result.status_code != 200:
		raise RuntimeError(f"Request for {result.url} returned status code {result.status_code} with content:\n{result.text}")

	jsonData = result.json()

	if jsonData["response"]["result"] < 1:
		raise RuntimeError(f"Request for {result.url} did not return a valid workshop item.")

	itemData = jsonData["response"]["publishedfiledetails"][0]
	fileName = os.path.basename(itemData["filename"])
	fileSize = itemData["file_size"]
	title = itemData["title"]
	fileURL = itemData["file_url"]
	fileSizeMB = fileSize / (1024 * 1024)

	print(f"Found workshop item: '{title}' ({fileName}, {fileSizeMB:.2f}MB)")

	fileDestPath = os.path.join(outputDir, fileName)
	if not overwrite and os.path.isfile(fileDestPath):
		raise OSError(f"File {fileDestPath} already exists on disk and overwriting is forbidden.")

	print("Downloading from URL:", fileURL)
	print("Destination file:", fileDestPath)

	wget.download(fileURL, out=fileDestPath)
