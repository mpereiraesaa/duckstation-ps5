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
show_fps = false

[input]
mode = xinput
