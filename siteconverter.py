import os
import sys
import requests
import json
import regex as re
import nbconvert
import helpers

### Helper functions ###

# function to write at specific 
# location in file
def write_mdfile(start_token,stop_token,file,to_write):
    with open(file,'r') as file_read:
        text = file_read.read()
        
    # split any new-line
    # parethesis preserve info
    tokens = re.split(r'(\n+)',text)
    # replace all-inbetween!
    try:
        start = tokens.index(start_token)
        stop = tokens.index(stop_token)
    except:
        raise Exception("Missing note-b token")

    tokens = [(tokens[i]) for i in range(len(tokens)) if i>stop or i<start]


    # append to_write (note-b)
    tokens.insert(start,to_write)
    
    # inserting before/after the tokens...
    tokens.insert(start+1,stop_token)
    tokens.insert(start,start_token)

    # writing back to file
    with open(file,'w') as file_write:
        file_write.write("".join(tokens))
    
# # make sure there is \n at begin/end
# write_mdfile('{{< jupyter_token >}}','{{< /jupyter_token >}}','test.md',"\nnote-b\ndata\nhere\n")

### Code-Converter ###
'''Given just language, and data,
convert the code simple into md!'''
def code_to_md(data_str,language):
    data_str = list(data_str)
    # start code-block
    start = f'\n{{{{< detail_rain summary= "{language}" open="True" >}}}}\n```{language}\n'
    end = f'\n{{{{</ detail_rain >}}}}\n'
    data_str.insert(0,start)
    data_str.append(end)
    
    data_str = "".join(data_str)
    data_str = format_out(data_str)
    return data_str



#####################

#####################
### Image-Handler ###
'''
Converts images from raw-byte-form to 
actual image!

'''
#####################

#####################
### Formatting Output ###
'''
Formatting output so we don't
accidentally have html code!

'''
def format_out(text):
    
    # Replace `<` with `&lt;` only if not preceeded by `{{'
    pattern = r'(?<![{{])<'
    replacement = "&lt;"
    text = re.sub(pattern,replacement,text)
    
    # preceeds two characters
    pattern = r'>(?![}}])'
    replacement = "&gt;"
    text = re.sub(pattern,replacement,text)
    return text
    
#####################

#################
### CONVERTER ###

'''Converter

Loops through each cell, 
and based on the type, will output
this to markdown. If it is an image,
it will convert/save in the appropriate folder.

For each markdown, simply append the markdown to the
list of 'stuff' with \n for linespace specified

For images, implement image-loader, and save this
into static/post_name, and then load in markdown

For code, load into appropriate code-block, and for
output of code, also load into appropriate codeblock.'''

def json_to_md(data_dict,language,path_img):
    # list of cells
    cells = data_dict["cells"]

    # full string/file
    data_stream = []
    
    # for each cell which is a dictionary
    # with source,outputs,
    for i, cell in enumerate(cells):
        # markdown cell
        if cell["cell_type"] == "markdown":
            # list of elements
            lines = cell["source"]
            # print(f"MD: {i}/{len(cells)}, source: {lines}")
            
            # markdown-format
            lines.append("\n{{</ markdown >}}\n")
            lines.insert(0,"\n{{< markdown >}}\n")
            
            # concat
            lines = "".join(lines)
            data_stream.append(lines)
        
        elif cell["cell_type"] == "code":
            # print(f"CODE: {i}/{len(cells)}, keys: {(cell.keys())}")
            # going through to get order
            for lj, key in enumerate(reversed(list(cell.keys()))):
                if key == "source":
                    # print(f"    Source: {lj}/{len(list(cell.keys()))}")
                    #######1. SOURCE #######
                    # list of elements
                    lines = cell[key]
                    
                    # for code-formatting
                    end = str("\n```\n{{</ detail_rain >}}\n")
                    start ="".join(['\n{{< detail_rain summary="code" open="true" >}}\n',f"```{language}\n"])
                    lines.append(end) 
                    lines.insert(0,start)
                    
                    # concat to file
                    lines = "".join(lines)
                    data_stream.append(lines)            
                    #########################
                    
                elif key == "outputs":
                    # print(f"    Output: {lj}/{len(list(cell.keys()))}")
                    need_end = False # track state of console
                    outputs = cell[key]
                    
                    # for each output in list (dict)
                    for output in outputs:
                        # for each dict
                        current_keys = list(output.keys())
                        # checking if we have text
                        if "text" in current_keys:
                            #### Standard Text/Stream Output ####
                            end = str("\n")
                            
                            # not already begun
                            if not need_end:
                                start = '\n{{< code_output summary="Output:" open="true" >}}\n'
                                need_end = True
                            else:
                                start = ""
                            
                            # all current-lines
                            lines = [start]
                            lines.append("".join(output["text"]))
                            
                            # append all-together
                            lines.append(end)
                            data_stream.append("".join(lines))
                            
                        # data-dict
                        elif "data" in current_keys:
                            # if it is plain-text
                            if "text/plain" in list(output["data"].keys()):
                                #### copied ####
                                language_temp = "" # no-lang
                                end = str("\n")
                                # not already begun
                                if not need_end:
                                    start = '\n{{< code_output summary="Output:" open="true" >}}\n'
                                    need_end = True
                                else:
                                    start = ""
                                lines = [start]
                                lines.append("".join(output["data"]["text/plain"]))
                                lines.append(end)
                                data_stream.append("".join(lines))

                                
                            ### IMG-CONVERT ###
                            img_in = False
                            image_types = ["png","jpg","jpeg","img","webp","gif","pdf","svg","eps"]
                            img_ext = ""
                            for type in image_types:
                                if f"image/{type}" in list(output["data"].keys()):
                                    img_in = True
                                    img_ext = type
                                    
                            if img_in:
                                start = "\n"
                                if not need_end:
                                    start = '\n{{< code_output summary="Output:" open="true" >}}\n'
                                    need_end = True
                                end = str("{{</ code_output >}}{{< br >}}\n")
                                need_end = False # got end
                                
                                # saving image at path!
                                raw_data = output["data"][f"image/{img_ext}"]
                                # making sure path is correct
                                img_name = f"cell_{i}_img.png"
                                path_img_new = "".join([path_img, f"/{img_name}"])
                                helpers.image_base64_save(raw_data=raw_data,
                                                          path_to_save=path_img_new)                            
                                
                                # not using /blog/static in md (implied)
                                # saving with image name
                                path_img_abs = path_img_new.split("/blog/static")[1]
                                print(f"*IMAGE SAVED: {path_img_new}")
                                img_data = f'{{{{< image_output src="{path_img_abs}" >}}}}'
                                
                                lines = [start]
                                lines.append(img_data)
                                lines.append(end)
                                data_stream.append("".join(lines))
                            ######################3
                                
                                
                                
                                          
                    # not end on image
                    if need_end:
                        end = str("{{</ code_output >}}{{< br >}}\n")
                        need_end = False
                        data_stream.append(end)     
            
    
    # making all 1-list
    text = "".join(data_stream)
    text = format_out(text)
    return text

#################


### MAIN PROGRAM ###

def main():
    # retreive url
    with open('post_to_url.json','r') as f:
        post_url_dict = json.load(f)

    for post_lang in list(post_url_dict.keys()):
        # language and post
        language,post = post_lang.split(';')
        print(language,post)

        url = post_url_dict[post_lang]
        print(url)
        # requesting url
        r = requests.get(url)
        
        # path to post
        path = os.path.abspath(f'../blog/content/{post}')
        
        if language == "jupyter":
            # getting dict
            data_raw = json.loads(r.text)
            # create image directory for post
            path_img = os.path.abspath(f'../blog/static/images/{post}'[:-3])
            os.makedirs(path_img,exist_ok=True)
                    
            # parsing text...
            code_lang = data_raw["metadata"]["kernelspec"]["language"]
            to_write = json_to_md(data_raw,language=code_lang,path_img=path_img) # quick
            
            write_mdfile(start_token="{{< start_token >}}",
                        stop_token="{{< end_token' >}}",
                        file=path,
                        to_write=to_write)
    
            print("*****JUPYTER*****")
            print(f"Wrote file: {path}\nFrom URL: {url} ({len(to_write)} chars)")
            print("*****JUPYTER*****")
            
        else:
            # getting raw-text
            data_raw = r.text
            # writes markdown file
            to_write = code_to_md(data_raw,language)
            # for arbitrary code-language!
            write_mdfile(start_token="{{< start_token >}}",
                        stop_token="{{< end_token' >}}",
                        file=path,
                        to_write=to_write)
            print(f"*****{language}*****")
            print(f"Wrote file: {path}\nFrom URL: {url} ({len(to_write)} chars)")
            print(f"*****{language}*****")
      
main()


