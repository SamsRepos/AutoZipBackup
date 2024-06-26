import os
import hashlib

# https://stackoverflow.com/questions/36204248/creating-unique-hash-for-directory-in-python

def sha256_of_string(str):
  sha = hashlib.new('sha256')
  sha.update(str.encode())
  return sha.hexdigest()

def sha256_of_file(file_path):
  sha = hashlib.new('sha256')
  with open(file_path, 'rb') as file:
    while True:
      block = file.read(2**10) # Magic number: one-megabyte blocks.
      if not block: break
      sha.update(block)
    return sha.hexdigest()
  
def hash_dir(dir_path):
  hashes = []
  for path, dirs, files in os.walk(dir_path):
    for file in sorted(files): # guarantee same order every time
      hashes.append(sha256_of_file(os.path.join(path, file)))
    for dir in sorted(dirs): # guarantee same order every time 
      hashes.append(hash_dir(os.path.join(path, dir)))
    break # we only need one iteration - to get files and dirs
  return str(sha256_of_string(''.join(hashes)))