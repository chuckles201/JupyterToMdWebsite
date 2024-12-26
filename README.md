# JupyterToMdWebsite


> Automatically reads JSON from a given URL, and parses it into good markdown that fits with Hugo website (any theme). 


Here are the instructions to set up:

## Downloading

1. Git clone in a folder/directory one step-up from your hugo website
2. ```conda env create -f environment.yml``` to create conda environemnt.

## Using in hugo

1. Create a new hugo post with ```hugo new posts/my_post_here.md```
2. Surround the part of your page your importing from with with ```{{< start_token >}}``` and ```{{< end_token >}}```
3. Go back to the cloned directory, and edit the ```post_to_url.json``` file as follows:

```
{
    "jupyter;posts/test_ipynb.md":"https://github.com/chuckles201/VQ-VAE-Implementation/blob/main/data/download.ipynb?raw=true",
}
```

with the format of ```"any-language;posts/post_url.md":"githubrawlink"```

4. Lastly, copy shortcodes for detail_rain, code_output, and others in your ```/layouts/shortcodes``` directory in your site. For tutorials on creating a custom shortcodes look [here](https://www.youtube.com/watch?v=Eu4zSaKOY4A&list=PLLAZ4kZ9dFpOnyRlyS-liKL5ReHDcj4G3&index=22&ab_channel=GiraffeAcademy). detail_rain is the CSS that displays/formats your code, and the code_output formats your output. ***I have my examples linked in the ```examples``` folder, copy all of them here, and modify them later for best results***.

> Now, running ```python siteconverter.py``` should automatically update the posts that you've linked! 

Leave an issue if this is not working

