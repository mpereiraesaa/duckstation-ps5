; DuckStation PS5: the official DuckStation build in its Big Picture mode.
; D: is /data/DuckStationPS5 (the prefix's dosdevices link table).
[application]
id = duckstation
name = DuckStation
executable = D:\duckstation\duckstation-qt-x64-ReleaseLTCG.exe
working_directory = D:\duckstation
arguments = -bigpicture -fullscreen
prefix = duckstation
runtime = wine-wow64
architecture = pe64
graphics = auto

[display]
desktop = 1920x1080
; true: a counter in the top left; with framegen, the game's frames and the
; pictures shown each second ("30 -> 60")
show_fps = false
; frame generation: 2 shows two pictures for each frame the game draws, the
; one between made by MihawkGen, so a 30 fps game reaches 60. For 30 fps
; games only: a 60 fps game runs slower with it. off, 2, 3 or 4
framegen = off

[input]
mode = xinput
