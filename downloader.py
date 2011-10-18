#!/usr/bin/python -O
import sys,os,re,urllib,urllib2

class_url_fragment = "http://www.%s-class.org/course/video/html5_embed?video_id=%d"
src_re = re.compile("src=\"(.*?)\"")

def download_file(video_url,video_filename):
    remote_file = urllib2.urlopen(video_url)
    local_file = open(video_filename, "w")
    local_file.write(remote_file.read())
    remote_file.close()
    local_file.close()
    print "downloading video " + video_filename

def get_url_content(url):
    page = urllib2.urlopen(url)
    return page.read()

def process_url_content(content):
    for line in content.split("\n"):
        if "source" in line:
            matches = src_re.search(line)
            video_url = matches.groups()[0]
            video_filename = class_name+"/"+video_url.split("/")[-1]
            if not os.path.exists(video_filename):
                download_file(video_url,video_filename)

try:
    class_name = sys.argv[1];
    if not os.path.exists(class_name):
        os.makedirs(class_name)
    for video_index in range(0,1000):
        url = class_url_fragment % (class_name, video_index)
        content = get_url_content(url)
        if("Invalid video id" not in content):
            process_url_content(content)
except Exception as inst:
    print "USAGE: ./downloader.py ml|db|ai"

