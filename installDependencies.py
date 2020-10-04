import subprocess
import sys

__DEPENDENCIES = \
[
	"requests",
	"wget"
]

__PIP = "pip"

if len(sys.argv > 1):
	__PIP = sys.argv[1]

for dep in __DEPENDENCIES:
	subprocess.run([__PIP, "install", dep], shell=True)
