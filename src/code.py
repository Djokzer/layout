# Author: Jonas S.
# Date : 25/04/2023
# Code : This is used to get an image of the code
# It uses carbon.now.sh to get the image 

from carbon import Carbon
import asyncio


async def code2img(code : str, code_dir : str) -> str:
    """
        Get an image from a given code
        args:
            code (str) : code to get the image from
            code_dir (str) : directory to save the image to
        returns:
            str : path to the created image
    """

    parts = code.split("```")[1].split("\n")
    lang = parts[0]
    code = "\n".join(filter(None, parts[1:]))

    print(parts)

    client = Carbon(
            downloads_dir = code_dir,
            colour = "rgba(171, 184, 195, 1)",
            shadow = False,
            shadow_blur_radius = "0px",
            shadow_offset_y = "0px",
            export_size = "4x",
            font_size = "14px",
            font_family =  "Fira Code",
            first_line_number = 1,
            language = f"{lang}",
            line_numbers = True,
            horizontal_padding = "20px",
            vertical_padding = "20px",
            theme = "One Dark",
            watermark = False,  
            width_adjustment = True, 
            window_controls =  True,
            window_theme = "sharp",
        )
    return await client.create(code)


if __name__ == "__main__":
    asyncio.run(code2img("```c\nprint('Hello')\nreturn 0\n```", "codes"))
