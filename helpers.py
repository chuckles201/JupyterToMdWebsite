import regex as re
from PIL import Image
import base64
from io import BytesIO # creates fake-file
import os
    
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

# testing
stre = "hello/blog/other/image/ot/png.py"
stre = stre.split("hello/blog/")
# print(stre)

#####