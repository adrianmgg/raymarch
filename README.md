
# About
This is a simple raymarching/sphere tracing renderer I wrote over the course of about a week in early 2020. The rendering is all done in a GLSL shader, the window/input stuff is managed with python.

# Code Overview
| file | description |
| - | - |
| `raymarch/shaders/shader_load_helper.py` | handles loading of shader files, including a (somewhat janky regex based) `#include` handler |
| `raymarch/shaders/fragment_shader.frag` | most of the rendering stuff is in here |
| `main.py` | manages window, keyboard/mouse input, etc. |

# Controls
| Key | Action |
| --- | ------ |
| w | move forwards |
| s | move backwards |
| a | move left |
| d | move right |
| q | move up |
| e | move down |
| shift | move faster while held |
| escape | toggle mouse controls on/off |
| mouse | turn camera |

# Setup/Running
```
pip install -r requirements.txt
python3 main.py
```

# Code I Didn't Write
[Hash Without Sine](https://www.shadertoy.com/view/4djSRW) (`raymarch/shaders/includes/hash_without_sine.glsl`) is under MIT License, Copyright (c)2014 David Hoskins.
[Signed Distance Functions](https://iquilezles.org/www/articles/distfunctions/distfunctions.htm) (`raymarch/shaders/includes/signed_distance_functions.glsl`) are by Inigo Quilez, and are under MIT License (see note on [this page](https://www.iquilezles.org/www/index.htm) about license of code snippets).



