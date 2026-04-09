# PixelRun
<img src="assets/images/icon.png" width=80>\
A remake of my old game. Inspired by Geometry Dash.

# Gameplay
There are SOME gameplay mechanics you'll see in the game

# Gamemodes
<img src="assets/images/skins/cube/cube_default.png">\
Cube: jumps on click\
<img src="assets/images/skins/ufo/ufo_default.png">\
UFO: jumps lower, but can jump in the air\
<img src="assets/images/skins/ball/ball_default.png">\
Ball: changes gravity on click

# Portals
Portals activate on touch and apply special effect\
<img src="assets/images/gravity_portal.png" width=75>\
Gravity portal: changes gravity to the opposite one.\
<img src="assets/images/upside_down_portal.png" width=75>\
Upside Down portal: sets your gravity to upside down mode\
<img src="assets/images/normal_gravity_portal.png" width=75>\
Normal Gravity portal: sets your gravity to default\
<img src="assets/images/cube_portal.png" width=75>\
Cube portal: sets your gamemode to cube\
<img src="assets/images/ufo_portal.png" width=75>\
UFO portal: sets your gamemode to UFO\
<img src="assets/images/ball_portal.png" width=75>\
Ball portal: sets your gamemode to ball

# Orbs
Orbs activate on click and collision with player and apply special effect\
<img src="assets/images/jump_orb.png" width=50>\
Jump orb: allows to jump in the air\
<img src="assets/images/gravity_orb.png" width=50>\
Gravity orb: changes gravity

# Gameplay images
<img src="readme/gameplay_cube1.png" width=350>
<img src="readme/gameplay_cube2.png" width=350>
<img src="readme/gameplay_ufo1.png" width=350>
<img src="readme/gameplay_ufo2.png" width=350>
<img src="readme/gameplay_ball1.png" width=350>
<img src="readme/gameplay_ball2.png" width=350>

# Level Editor
By using level editor you can create your own levels and play them. Level save in JSON format.\
<img src="readme/editor1.png" width=350>
<img src="readme/editor2.png" width=350>

# Credits
Game by Angry Muni 

Skins textures by: RobTopGames

Portals, orbs, triggers,
checkpoint textures by RobTopGames

Background music: Me Time by Avanti

Inspired by Geometry Dash by RobTopGames

# Build command
The official build is made by using PyInstaller. Installation:\
`pip install pyinstaller`\
Command:\
`pyinstaller --onefile --noconsole --add-data "assets;assets" --icon icon_build.ico --collect-all pygame main.py`