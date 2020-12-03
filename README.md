# AutoCen
 A small wrapper for NudeNet library.

Installation:
- python3.7 or lower
- NudeNet (https://github.com/notAI-tech/NudeNet) and its dependencies.

Usage:
- Put your images in directory `_in`
- Run `python main.py` on console.
- Get the result images from directory `_out`. The image will still be copy to `_out` even if there's nothing to censore.

Stuff:
- Censoring by three options: Pixelate, Blurring, Good ol' black rectangles.
- You can configure the input path and the output path.
- Frequency is how strong the censoring will be.

TODO:
- Use custom image to censor, with the option of adjusting transparency. (e.g. smoke, cloud, etc.)
