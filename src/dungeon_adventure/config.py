import os

# Get the directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to get to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))

# Define the path to the resources directory
RESOURCES_DIR = os.path.join(PROJECT_ROOT, "DungeonAdventure/resources")

FONT_PATH = os.path.join(RESOURCES_DIR, "fonts/")
