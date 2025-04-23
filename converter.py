import os
import re
from datetime import datetime

# Regex pattern that captures datetime and 3 or more float values
pattern = re.compile(
  r"\[datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\)(?:, ([\d.,\s]+))?\]"
)

input_folder = ".out"
output_folder = ".temp"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
  if not filename.endswith(".csv"):
    continue

  filepath = os.path.join(input_folder, filename)

  with open(filepath, "r") as f:
    first_line = f.readline().strip()

  if first_line.startswith("[datetime.datetime("):
    print(f"Processing file: {filename}")

    with open(filepath, "r") as f:
      lines = f.readlines()

    converted_lines = []

    for line in lines:
      match = pattern.match(line.strip())
      if not match:
        print(f"  Skipped line (no match): {line.strip()}")
        continue

      year, month, day, hour, minute, second, microsecond = map(int, match.groups()[:7])
      values_str = match.group(8)

      if not values_str:
        print(f"  Skipped line (no values): {line.strip()}")
        continue

      # Parse the list of float values
      try:
        values = [float(v.strip()) for v in values_str.split(",")]
      except ValueError as e:
        print(f"  Skipped line (value error): {line.strip()}")
        continue

      timestamp = datetime(year, month, day, hour, minute, second, microsecond)
      timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
      formatted_line = f"{timestamp_str};" + ";".join(f"{v:.2f}" for v in values)
      converted_lines.append(formatted_line)

    output_path = os.path.join(output_folder, filename)
    with open(output_path, "w") as f:
      for line in converted_lines:
        f.write(line + "\n")

    print(f"  Written to: {output_path}")
