import os
import sys
import subprocess
import hashlib
import time

class FileExpedient:
    pass
    
mypath = sys.argv[1]

f = []
results = []

for (dirpath, dirnames, filenames) in os.walk(mypath):
    for filename in filenames:
        full_path = os.path.abspath(os.path.join(dirpath, filename))

        # Execute "file" command for target file
        filecmdoutput = subprocess.Popen("/usr/bin/file {0}".format(full_path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().split(':')[-1].strip()
        
        # Fill the FileExpedient objects stored in a list
        file_expedient = FileExpedient()
        file_expedient.full_path = full_path
        file_expedient.relative_path = os.path.join(dirpath, filename)
        file_expedient.filename = filename
        file_expedient.last_data_access = time.ctime(os.path.getatime(full_path))
        file_expedient.last_data_modification = time.ctime(os.path.getmtime(full_path))
        file_expedient.file_status_last_changed = time.ctime(os.path.getctime(full_path))
        file_expedient.size = os.path.getsize(full_path)
        file_expedient.filecmdoutput = filecmdoutput
        file_expedient.extension = filename.split('.')[-1]
        file_expedient.md5hash = hashlib.md5(open(full_path, 'rb').read()).hexdigest()
        file_expedient.sha256hash = hashlib.sha256(open(full_path, 'rb').read()).hexdigest()
        results.append(file_expedient)
    
for file_expedient in results:
    print "Full path: {0}".format(file_expedient.full_path)
    print "Relative path: {0}".format(file_expedient.relative_path)
    print "Filename: {0}".format(file_expedient.filename)
    print "Last data access: {0}".format(file_expedient.last_data_access)
    print "Last data modification: {0}".format(file_expedient.last_data_modification)
    print "File status last change: {0}".format(file_expedient.file_status_last_changed)
    print "File size: {0}".format(file_expedient.size)
    print "File command result: {0}".format(file_expedient.filecmdoutput)
    print "File extension: {0}".format(file_expedient.extension)
    print "MD5 hash: {0}".format(file_expedient.md5lhash)
    print "SHA256 hash: {0}".format(file_expedient.sha256hash)
    print "\n"
    
