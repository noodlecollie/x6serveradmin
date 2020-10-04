import argparse
import os
import sys

from steamAPIAuth import SteamAPIAuth
from downloadWorkshopItem import downloadItem

__SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
__AUTH_FILE_PATH = os.path.join(__SCRIPT_DIR, "auth.json")

__DEFAULT_GAME_PARENT_DIR = os.path.realpath(os.path.join(__SCRIPT_DIR, ".."))
__DEFAULT_GAME_NAME = os.path.basename(__DEFAULT_GAME_PARENT_DIR)
__DEFAULT_GAME_DIR = os.path.join(__DEFAULT_GAME_PARENT_DIR, __DEFAULT_GAME_NAME)

def __loadAuth():
	if not os.path.isfile(__AUTH_FILE_PATH):
		raise RuntimeError("No auth configuration created - run `create-auth` first.")

	return SteamAPIAuth(__AUTH_FILE_PATH)

def __cmd_Download(args):
	outputDir = args.output_dir

	if outputDir is None:
		outputDir = os.path.join(args.game_dir, "addons")

	downloadItem(__loadAuth(), args.item_id, outputDir, args.overwrite)

def __cmd_CreateAuth(args):
	auth = SteamAPIAuth()

	auth.apiKey = args.api_key
	auth.steamID = args.steam_id

	auth.createAuthJson(__AUTH_FILE_PATH)
	print("Wrote auth file:", __AUTH_FILE_PATH)

def __parseArgs_CreateAuth(subparsers):
	createAuth = subparsers.add_parser("create-auth",
									   help="Creates a Steam API auth for use with the Steam Web API.")
	createAuth.add_argument("--api-key",
							required=True,
							help="API key for requests. Can be created at https://steamcommunity.com/dev/apikey")
	createAuth.add_argument("--steam-id",
							required=True,
							help="Steam ID for requests. Can be found using https://steamidfinder.com/")
	createAuth.set_defaults(func=__cmd_CreateAuth)

def __parseArgs_Download(subparsers):
	downloadWorkshopItem = subparsers.add_parser("download",
												 help="Downloads a workshop item to a specified location.")
	downloadWorkshopItem.add_argument("--item-id",
									  required=True,
									  help="ID of the item to download. This is found at the end of the workshop URL.")
	downloadWorkshopItem.add_argument("--output-dir",
									  default=None,
									  help="Directory in which to place the downloaded item. Defaults to " +
									       "`<gamedir>/addons`")
	downloadWorkshopItem.add_argument("--overwrite",
									  action="store_true",
									  help="If true, allows overwriting of existing downloaded items.")
	downloadWorkshopItem.set_defaults(func=__cmd_Download)

def __parseArgs():
	parser = argparse.ArgumentParser(description="Server administration console.")
	parser.add_argument("-g", "--game-dir",
						help="Path to directory in which game files reside. If not specified, " +
						     "defaults to a subdirectory of the script's parent directory whose " +
							 "name is the same as the parent directory (eg. `<scriptdir>/../left4dead2/left4dead2`).",
						default=__DEFAULT_GAME_DIR)

	subparsers = parser.add_subparsers(title="commands",
									   description="Available commands:",
									   help="Invoke with `x6server.py cmd --help` for help regarding a specific command.")

	__parseArgs_Download(subparsers)
	__parseArgs_CreateAuth(subparsers)

	return parser.parse_args()

def main():
	args = __parseArgs()

	if not os.path.isdir(args.game_dir):
		if args.game_dir == __DEFAULT_GAME_DIR:
			print("Default game directory", args.game_dir, "is not valid. Specify a directory using -g/--game-dir.")
		else:
			print("Specified game directory", args.game_dir, "is not valid.", file=sys.stderr)

		sys.exit(1)

	try:
		args.func(args)
	except Exception as ex:
		print("An error occurred while running the command.", str(ex), file=sys.stderr)
		sys.exit(1)

if __name__ == "__main__":
	main()
