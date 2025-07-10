import pathlib
import re


base_paths = ["content", "templates"]
base_file_types = ["md", "html"]


for path in base_paths:
    for file_type in base_file_types:
        print(f"Checking {file_type} in {path}")
        p = pathlib.Path(path)
        for entry in p.rglob(f"*.{file_type}"):
            print(entry)
            new_string, count = re.subn(
                "media/media",
                "media",
                entry.read_text(),
            )
            if count:
                print(f"{entry} modified")
            entry.write_text(new_string)
