import urllib2
from bs4 import BeautifulSoup
import re
import webbrowser
import requests
from os.path import join
import os
import win32api
import sys

request = urllib2.Request("http://<webServer>/builds/Trunk/BUILD_TRUNK_APP-RELEASE/")
response = urllib2.urlopen(request)
soup = BeautifulSoup(response)
myList = []
counter = 1
buffer_size = 1024*8*8*8 #size of the buffer - helper variable for indicating downloaded percentage

for a in soup.findAll('a'): #search for all links on that page (<a tag is the tag which all HTML links have)
    versions = re.sub('/', '', a['href']) #find all href links in html (<a href=...) and substract it's slash from the end "/" because it's included in b always
    myList.append(versions); #add to list all versions of builds from web's link


latestVersionNum = myList[len(myList)-1] #latestVersionNum is 4-digit number of the last version of the build, last element appended to Python list


html_content = urllib2.urlopen('http://<webServer>/builds/Trunk/BUILD_TRUNK_APP-RELEASE/' + latestVersionNum + '/archive/update.xml').read()
matches = re.findall('<LatestBuildNum>(\d+)</LatestBuildNum>', html_content);
matches1 = re.findall('((<LatestVersion>)(\d+\W\d\W\d)(</LatestVersion>))', html_content);

temp_path = r'\\<someFileshareLocation>Team Shares\Clients\<AppName>\Public\Installations\Jabber installers\Trunk_Installers\\'
newpath = temp_path + latestVersionNum + ' - Version ' + matches1[0][2] + '.' + matches[0]
if not os.path.exists(newpath):
    os.makedirs(newpath)

directory = temp_path + latestVersionNum + ' - Version ' + matches1[0][2] + '.' + matches[0]

url1 = urllib2.urlopen('http://<webServer>/builds/Trunk/BUILD_TRUNK_APP-RELEASE/'+ latestVersionNum +'/archive/<InstallerName>.msi')
meta = url1.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading %s Bytes" %file_size

def download_file(url, counter): #function definition for downloading files
    local_filename = url.split('/')[-1]
    local_filename = join(directory, local_filename)
    r = requests.get(url, stream=True) #steam = True so we can download larger files from web
    with open(local_filename, 'wb') as f: #It is good practice to use the with keyword when dealing with file objects. This has the advantage that the file
                        #is properly closed after its suite finishes, even if an exception is raised on the way. It is also much shorter than writing equivalent try-finally blocks
        
        for chunk in r.iter_content(chunk_size=buffer_size): #iterate through 1MB chunks of memory
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)  #write to that chunk
                f.flush()
                file_size_dl = counter*buffer_size
                percentage_indicator = file_size_dl * 100. / file_size
                if (percentage_indicator>100) : percentage_indicator = 100
                status = r"%10d  [%3.2f%%]" % (file_size_dl, percentage_indicator)
                print status
                counter += 1
    return local_filename

if os.listdir(directory) == []:
    download_file('http://<webServer>/builds/Trunk/BUILD_TRUNK_APP-RELEASE/'+latestVersionNum+'/archive/<InstallerName>.msi', counter)
else:
    print "A folder with that name already exists"
    sys.exit()

