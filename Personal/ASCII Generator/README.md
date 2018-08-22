# Ascii Image Generator
> by Jesse Ashmore

This script will take images from './in/' and convert them all to images built up from ascii characters.

## Install

Requires Pillow as a dependency
`pip install pillow`

I haven't implemented folder creation, so make sure you have the following structure.

```
/in/
/out
   /lum/
   /rgb/
ascii.py
```

## Usage

Place image files in `./in/` folder

Run `python ascii.py`

Choose options with user input.

- RGB colour mode will colour the ascii characters to the original pixel value. BW will only use black and white.

- Resolution is just a scaling option. Warning: High resolution can result in HUGE images if the source is large.

- Background specifies if you want chars on white background, or chars on black background. The char colour is adjusted accordingly.

## Output

Image files encoded in ascii chars to `./out/` and the relevant subfolders `lum` or `rgb`.
