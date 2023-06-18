import re
import os, sys, shutil, glob

print("Building site to generate warnings...")
os.system("mkdocs build -c > log 2>&1")

with open("log", "r") as l:
    logs = l.readlines()

log_warnings = [l for l in logs if "WARNING" in l]
print("Warnings Messages found:")
print(len(log_warnings))

pattern = ".*contains a link to '?(.*png|.*jpg|.*jpeg|.*PNG|.*JPG|.*JPEG)'?"


def find_images(log):
    regex = re.compile(pattern)
    match = regex.match(log)
    if match:
        return match.group(1)
    else:
        return None


images = [find_images(l) for l in log_warnings if find_images(l)]
images = list(set(images))
print("Images found:")
print(len(images))

new_base_dir = "./all_notebooks"
if not os.path.exists(new_base_dir):
    os.makedirs(new_base_dir)

for file in images:
    new_file = os.path.join(new_base_dir, file)
    new_dir = os.path.dirname(new_file)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    shutil.copyfile(file, new_file)

print("Done. Here are the images copied:")
print(images)

print("Creating final site...")
os.system("mkdocs build -c")
