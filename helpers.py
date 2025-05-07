import regex as re
from PIL import Image
import base64
from io import BytesIO # creates fake-file
import os
import requests
    
####################################3
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

# text = "<test>\n{{< Test >}}\n <test> <test>"

# print(format_out(text))
####################################


####################################
'''Image-Converter!

Give path and data, it will convert
and save to that given path.'''

def image_base64_save(raw_data,path_to_save):
    
    # binary-writing-pdf
    def bytes_to_img(raw_str,save_path):
        # decode to bytes
        raw_bytes = base64.b64decode(raw_str)
        # temporary file
        image = Image.open(BytesIO(raw_bytes))
        
        # show image!
        image.save(f"{save_path}")

    bytes_to_img(raw_data,path_to_save)

####################################


#######DOWNLOADING IMAGE#########
'''Get relative url,
and then download

0. Find all images
1. Replace URL
2. Download image
3. Correct md-path'''
    
with open('../pass.txt','r') as f:
    git_token = f.read().strip()
    print("PASSSSS: ",git_token)
def find_replace_images(text,url,post_name,git_token=git_token):
    
    # download and return right md-insertion
    def download_image_md(path_md_string,original_path=url,post_name=post_name):        
        
        # insert blob
        new_path = original_path.replace('/refs/heads/','/blob/')
        
        # insert github.com
        new_path = new_path.replace('raw.githubusercontent.com','github.com')
        
        # split to change
        url,path = new_path.split('/blob/')
        path = path.split('/')
            

        # formatting raw-md-string
        path_md = path_md_string.split('(')[1][:-1]
        if path_md[0] == "/":
            path_md = path_md[1:]
        path[-1] = path_md
        
        # adding md path to new path
        path = "/".join(path)
        full_url = "/blob/".join([url,path])
        
        # downloading to file
        rel_directory = f"../blog/static/images/{post_name}/{path_md}".split("/")
        rel_directory = "/".join(rel_directory[:-1])
        os.makedirs(rel_directory,exist_ok=True)
        output_filename = f"../blog/static/images/{post_name}/{path_md}"
        download_url = "".join([full_url,"?raw=true"])
        
        # Send an HTTP GET request to the URL
        print("Downloading: ",download_url)
        
        headers = {
            "Authorization":f"{git_token}"
        }
        response = requests.get(download_url,headers=headers)

        # Check if the request was successful
        # should still not break if wrong path!
        if response.status_code == 200:
            # Write the content to a file
            with open(output_filename, "wb") as file:
                file.write(response.content)
            print(f"Image downloaded and saved as {output_filename}")
        else:
            print(f"Failed to download image. HTTP status code: {response.status_code}")
            
        
        # return corrected md-string
        md_path = output_filename.split("/blog/static")[1]
        md_string = f'{{{{< image_output src="{md_path}" >}}}}'
        return md_string
    
    # find all images, w/ desired
    # md pattern
    
    # img_indices:
    # pattern to capture them, findall
    pattern = "!\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.finditer(pattern,text)
    text_new = text
    
    for match in matches:
        str_md = match.group()
        new = download_image_md(str_md,url,post_name)
        text_new = text_new.replace(str_md,new)
        
    
    
    return text_new


# testing if works!
rel_url = "https://raw.githubusercontent.com/chuckles201/DiT-Implementation/refs/heads/main/DDPM/explained.ipynb"
test="Hello\n\n![image](images/form8.png)\n\n ![not an image!]\n\n helleeleol\n\n![imga](images/form1.png)"

