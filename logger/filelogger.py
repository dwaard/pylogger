import os
from pathlib import Path
from datetime import datetime

class FileLogger:

    def __init__(self):
        self.filename = os.getenv('FILELOGGERFILENAME')
        if self.filename is None:
            raise Exception('FILELOGGERFILENAME is not set')

        if os.getenv('FILELOGGERWILLADDTIMESTAMP', False).lower() in ["true", "1", "yes"]:
            # Create the timestamp
            format = os.getenv('FILELOGGERTIMESTAMPFORMAT', "%d-%m-%Y_%H_%M_%S")
            timestamp = datetime.now().strftime(format)
            # Use Path to breakup the filename
            path = Path(self.filename)
            self.filename = path.with_name(f"{path.stem}_{timestamp}{path.suffix}")
        self.writemode = os.getenv('FILELOGGERWRITEMODE', 'x')
        self.writer = open(self.filename, self.writemode)


    def log(self, data):
        print("Writing to file: ", data)
        self.writer.write(data + '\n')
        self.writer.flush()


    def close(self):
        if self.writer:
            self.writer.close()
            print(f"Closed '{self.filename}'.")
            self.writer = None  # Zet self.file naar None na sluiten
        else:
            print("File already closed or not opened.")