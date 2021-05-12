#!/usr/bin/python
# pip install htmlmin
# pip install cssmin
# pip install jsmin
# if platformIO has a different python instance, use this  C:\Users\redma\.platformio\penv\Scripts\pip.exe install htmlmin

import os
import htmlmin
import cssmin
from jsmin import jsmin
import re
import binascii

input_dir = "html"              # Sub folder of webfiles
output_file = "src/webcontent.h"

f_output = open(output_file, "w")
#URL_minify_js   = 'https://javascript-minifier.com/raw' # Website to minify javascript
#URL_minify_html = 'https://html-minifier.com/raw'        # Website to minify html
#URL_minify_css  = 'https://cssminifier.com/raw'         # Website to minify css

f_output.write("// This file is autogenerated. DO NOT MODIFY!!!\n\n")

def removeComments(string):
    #string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
    #string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurrence single-line comments (//COMMENT\n ) from string
    return string

def write_to_file(file, data, dir=""):
    filename, file_extension = os.path.splitext(file)       # Split filename and file extension
    file_extension = file_extension.replace(".","")         # Remove puncuation in file extension

    dir = dir.replace(input_dir,"")                         # Remove the first directory(input_dir)
    dir = dir.replace("\\","/")                             # Change to /
    if (dir == "/index."):
        dir="/index.html"
    f_output.write("// " + dir + "\n")                      # Print comment
    f_output.write("const char* const data_" + filename + "_" + file_extension + "_path PROGMEM = \""+str(dir)+"\";\n")    # print path
    f_output.write("const char data_"+filename+"_"+file_extension+"[] PROGMEM = "+data+"\n\n")            # print binary data

    # f_output.write("#define data_" + filename + "_len " + str(data.count('0x')) +"\n")

def aschii2Hex(text):
    output_str = ""
    x = 1
    strLen = len(text)
    for character in text:
        output_str += hex(ord(character))

        if (x != strLen):
            output_str += ","
        x += 1
    return output_str

def minify_js(input_file):
    data = "R\"=====(\n"
    sourceFile = open (input_file, "r")
    #data = jsmin(sourceFile.read(), quote_chars="'\"`")
    with open (input_file, "r") as sourceFile:
        data+=removeComments(sourceFile.read().replace('  ', '').replace('\t', '').replace('\n\n', '\n'))
    sourceFile.close()
    data += "\n)=====\";"
    return data

def minify_html(input_file):    
    data = "R\"=====(\n"
    with open (input_file, "r") as sourceFile:
        data+=sourceFile.read().replace('  ', '').replace('\t', '').replace('\n\n', '\n')
    sourceFile.close()
    
    #data = htmlmin.minify(data, remove_optional_attribute_quotes=False)    
    data += "\n)=====\";"
    return data

def minify_css(input_file):
    data = "R\"=====(\n"
    with open (input_file, "r") as sourceFile:
        data+=removeComments(sourceFile.read().replace('  ', '').replace('\t', '').replace('\n\n', '\n'))
    sourceFile.close()
    
    #data += cssmin.cssmin(data)
    data += "\n)=====\";"
    return data

def minifyPictures(input_file):
    with open(input_file, 'rb') as f:
        content = f.read()
    print(binascii.hexlify(content))


for root, dirs, files in os.walk(input_dir, topdown=False):
    for name in files:   # for files
        if name.endswith(".js"):
            print(os.path.join(root, name))
            minified = minify_js(os.path.join(root, name))          # minify javascript
            write_to_file(name, minified, os.path.join(root, name)) # write to file

        elif name.endswith(".html"):
            print(os.path.join(root, name))
            minified = minify_html(os.path.join(root, name))        # minify html
            write_to_file(name, minified, os.path.join(root, name)) # write to file

        elif name.endswith(".css"):
            print(os.path.join(root, name))
            minified = minify_css(os.path.join(root, name))         # minify css
            write_to_file(name, minified, os.path.join(root, name)) # write to file
        #elif name.endswith(".png"):
            #minifyPictures(os.path.join(root, name));
            #print(os.path.join(root, name))
            #minified = minifyPictures(os.path.join(root, name))
            #write_to_file(name, minified, os.path.join(root, name))


f_output.close()