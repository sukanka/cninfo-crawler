from src import readsheet
from sys import argv

if __name__ == "__main__":
    start = 0
    if len(argv) > 1:
        start = int(argv[1])
    readsheet.start_download(start=start)
