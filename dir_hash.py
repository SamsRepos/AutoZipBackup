import os
import hashlib

# https://stackoverflow.com/questions/36204248/creating-unique-hash-for-directory-in-python

def sha1_of_file(file_path):
  sha = hashlib.sha1()
  with open(file_path, 'rb') as file:
    while True:
      block = file.read(2**10) # Magic number: one-megabyte blocks.
      if not block: break
      sha.update(block)
    return sha.hexdigest()
  
def dir_hash(dir_path):
  hashes = []
  for path, dirs, files in os.walk(dir_path):
    for file in sorted(files): # guarantee same order every time
      hashes.append(sha1_of_file(os.path.join(path, file)))
    for dir in sorted(dirs): # guarantee same order every time 
      hashes.append(dir_hash(os.path.join(path, dir)))
    break # we only need one iteration - to get files and dirs
  return str(hash(''.join(hashes)))