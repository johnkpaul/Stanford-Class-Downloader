#!/usr/bin/python -O
import sys,os,requests,re,urllib

class_url_fragment = "http://www.%s-class.org/course/video/html5_embed?video_id=%d"
src_re = re.compile("src=\"(.*?)\"")

def download_file(video_url,video_filename):
    remote_file = urllib.urlopen(video_url)
    local_file = open(video_filename, "w")
    local_file.write(remote_file.read())
    remote_file.close()
    local_file.close()
    print "downloading video " + video_filename

try:
    class_name = sys.argv[1];
    if not os.path.exists(class_name):
        os.makedirs(class_name)
    video_index = 1;
    while(True):
        url = class_url_fragment % (class_name, video_index)
        r = requests.get(url)
        content = r.content;
        if("Invalid video id" in content):
            break
        else:
            for line in content.split("\n"):
                if "source" in line:
                    matches = src_re.search(line)
                    video_url = matches.groups()[0]
                    video_filename = class_name+"/"+video_url.split("/")[-1]
                    if not os.path.exists(video_filename):
                        download_file(video_url,video_filename)
        video_index = video_index + 1;
except Exception as inst:
    print "USAGE: ./downloader.py ml|db|ai"
    print type(inst)     # the exception instance
    print dir(inst)
    print str(inst)

