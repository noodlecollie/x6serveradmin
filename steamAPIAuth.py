import os
import json

class SteamAPIAuth():
	def __init__(self, filePath=None):
		self.apiKey = ""
		self.steamID = ""

		if filePath is None:
			return

		if not os.path.isfile(filePath):
			raise OSError(f"Steam API auth file {filePath} does not exist.")

		with open(filePath, "r") as inFile:
			data = json.load(inFile)

			if not isinstance(data, dict):
				raise RuntimeError(f"Steam API auth file {filePath} was not specified as a JSON object.")

			if "apiKey" not in data:
				raise RuntimeError(f"Steam API auth file {filePath} did not contain an apiKey item.")

			if "steamID" not in data:
				raise RuntimeError(f"Steam API auth file {filePath} did not contain a steamID item.")

			self.apiKey = data["apiKey"]
			self.steamID = data["steamID"]

	def createAuthJson(self, filePath):
		output = \
		{
			"apiKey": self.apiKey,
			"steamID": self.steamID
		}

		with open(filePath, "w") as outFile:
			json.dump(output, outFile)
