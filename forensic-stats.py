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

expedients_file = open("expedients.txt", 'w')
statistics_file = open("statistics.txt", 'w')

number_of_files = 0
file_command_statistics = {}
file_extension_statistics = {}
smallest_file = None
biggest_file = None

print "[*] Browsing directory"
for (dirpath, dirnames, filenames) in os.walk(mypath):
    for filename in filenames:
        number_of_files += 1
        if number_of_files % 10 == 0:
            print "Files reviewed: {0}".format(number_of_files)
            
        full_path = os.path.abspath(os.path.join(dirpath, filename))

        # Execute "file" command for target file
        filecmdoutput = subprocess.Popen(["/usr/bin/file", "{0}".format(full_path)], stdout=subprocess.PIPE).communicate()[0].split(':')[-1].strip()
        
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

        if not smallest_file or file_expedient.size < smallest_file.size:
            smallest_file = file_expedient
        if not biggest_file or file_expedient.size > biggest_file.size:
            biggest_file = file_expedient

        file_command_statistics[file_expedient.filecmdoutput] = file_command_statistics.get(file_expedient.filecmdoutput, 0) + 1

        file_extension_statistics[file_expedient.extension] = file_extension_statistics.get(file_expedient.extension, 0) + 1


print "[*] Writing file expedients in {0}".format("expedients.txt")
for file_expedient in results:
    expedients_file.write("Full path: {0}\n".format(file_expedient.full_path))
    expedients_file.write("Relative path: {0}\n".format(file_expedient.relative_path))
    expedients_file.write("Filename: {0}\n".format(file_expedient.filename))
    expedients_file.write("Last data access: {0}\n".format(file_expedient.last_data_access))
    expedients_file.write("Last data modification: {0}\n".format(file_expedient.last_data_modification))
    expedients_file.write("File status last change: {0}\n".format(file_expedient.file_status_last_changed))
    expedients_file.write("File size: {0}\n".format(file_expedient.size))
    expedients_file.write("File command result: {0}\n".format(file_expedient.filecmdoutput))
    expedients_file.write("File extension: {0}\n".format(file_expedient.extension))
    expedients_file.write("MD5 hash: {0}\n".format(file_expedient.md5hash))
    expedients_file.write("SHA256 hash: {0}\n\n".format(file_expedient.sha256hash))

print "[*] Writing statistics in {0}".format("statistics.txt") 
statistics_file.write("Generic Statistics\n")
statistics_file.write("==================\n")
statistics_file.write("Number of files: {0}\n".format(number_of_files))
statistics_file.write("Smallest file: {0} Size: {1}\n".format(smallest_file.full_path, smallest_file.size))
statistics_file.write("Biggest file: {0} Size: {1}\n".format(biggest_file.full_path, biggest_file.size))
statistics_file.write("\n")
statistics_file.write("File Command Statistics\n")
statistics_file.write("=======================\n")
for filecmdoutput in file_command_statistics.keys():
    statistics_file.write("{0} {1}\n".format(file_command_statistics[filecmdoutput], filecmdoutput))
statistics_file.write("\n")    
statistics_file.write("File Extension Statistics\n")
statistics_file.write("=========================\n")
for extension in file_extension_statistics.keys():
    statistics_file.write("{0} {1}\n".format(file_extension_statistics[extension], extension))    
statistics_file.write("\n")

print "[*] DONE!"    
