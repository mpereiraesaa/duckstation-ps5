# DuckStation PS5

Play your PlayStation games on a jailbroken PS5 with **DuckStation**, the
PlayStation emulator, in its controller-friendly Big Picture mode. It is the
official DuckStation build for Windows, unchanged, started from its own icon
on the PS5 home screen.

[Español más abajo](#español)

## What you need

- A jailbroken PS5 with etaHEN, kstuff and ShadowMountPlus (the same setup
  other homebrew apps on the home screen need), and an FTP client.
- Your own PlayStation BIOS, dumped from your console, and your own game
  backups. Neither is included.

## Install

Each release has two downloads:

- `DuckStationPS5-<version>.zip`: the app and its folders, set up to play.
- `duckstation-windows-x64-release.zip`: the official DuckStation build this
  release was made for, exactly as its authors published it (see
  [Which DuckStation](#which-duckstation)).

1. Unzip `DuckStationPS5-<version>.zip`. Copy the two folders inside,
   `homebrew` and `DuckStationPS5`, into `/data` on the PS5 over FTP.
2. Unzip `duckstation-windows-x64-release.zip` into
   `/data/DuckStationPS5/duckstation/`, so that folder holds
   `duckstation-qt-x64-ReleaseLTCG.exe`.
3. Put your BIOS in `/data/DuckStationPS5/bios/`.
4. Put your games in `/data/DuckStationPS5/games/` (`.cue`/`.bin`, `.chd`,
   `.pbp`, `.iso`, `.m3u`; one folder per game is fine).
5. Restart ShadowMountPlus (or the console). **DuckStation PS5** appears on
   the home screen.

```
/data/DuckStationPS5/
  duckstation/   the official DuckStation build (step 2)
  bios/          your BIOS
  games/         your games
  system/        the app's own files: leave as is
```

DuckStation keeps its settings, memory cards, save states and screenshots in
`/data/DuckStationPS5/` too.

## Playing

Open **DuckStation PS5** from the home screen. It is ready to play: the
DualSense is the PlayStation controller, the games in
`/data/DuckStationPS5/games/` are in the **Game List**, and the picture is
drawn with Vulkan at six times the original resolution, with PGXP, and fills
the 16:9 screen: 3D games are widened, and games with pre-rendered
backgrounds, which cannot be, are stretched. Change any of it in
DuckStation's **Settings**, for every game or per game.

### Controls

| DualSense | In a game |
|---|---|
| Buttons, sticks, d-pad, L1/R1/L2/R2 | the PlayStation controller's (analog) |
| Options | Start |
| Create | Select |
| **Touchpad** | DuckStation's menu: save and load states, settings, cheats, change disc, exit |
| **Hold L3 + R3** (both sticks) | fast forward, while held |

In DuckStation's menus: d-pad or left stick to move, Cross to choose,
Circle to go back. **Exit** in the main menu (choose to close DuckStation)
takes you back to the PS5 home screen.

### Texture packs

Put a DuckStation texture pack in `/data/DuckStationPS5/textures/<serial>/`
(for example `textures/SLUS-01279/`, the game's serial as DuckStation shows
it in the Game List). Packs of background images (`vram-write-*.png`) load
by themselves. Packs of the newer kind (`texpage-*.png`) also need the
texture cache: in the game's **Game Properties > Graphics > Texture
Replacements**, turn on **Enable Texture Cache** for that game.

## Which DuckStation

| DuckStation PS5 | DuckStation build | Commit | SHA-256 of the zip |
|---|---|---|---|
| 1.0 | `0.1-12442-gdd4a0eb77` (2026-10-25) | [`dd4a0eb`](https://github.com/stenzek/duckstation/commit/dd4a0eb779296a525f8b10b6d9a45911ad6d088f) | `b55d1cf45bdb6d0326a9083cf787ca7d6386dff6c837f6d3b8713f48af2a02b7` |

Use the zip from the same release: the app is tested with that build.
DuckStation's own updater does not work on the console; a new DuckStation
comes with a new DuckStation PS5 release.

## Credits

- [DuckStation](https://www.duckstation.org/) by Stenzek and its
  contributors, under CC BY-NC-ND 4.0. This project is not affiliated with
  DuckStation; it ships the official release unchanged, as a separate
  download, and its icon is DuckStation's duck.
- The app runs DuckStation through
  [prospero-win](https://github.com/mpereiraesaa/prospero-win) (LGPL-2.1),
  with Wine, Mesa's RADV driver and FreeType. `homebrew/PPSA99990`
  carries their licences (`LICENSE`, `THIRD_PARTY.md`, `LICENSES/`) and the
  source revision of each part (`SOURCES.txt`).
- PlayStation is a trademark of Sony Interactive Entertainment. No BIOS,
  game or Sony software is included.

---

## Español

Juega a tus juegos de PlayStation en una PS5 con jailbreak con **DuckStation**,
el emulador de PlayStation, en su modo Big Picture pensado para el mando. Es el
build oficial de DuckStation para Windows, sin cambios, con su propio icono en
el home de la PS5.

### Qué necesitas

- Una PS5 con jailbreak, etaHEN, kstuff y ShadowMountPlus (lo mismo que piden
  otras apps homebrew del home) y un cliente FTP.
- Tu propia BIOS de PlayStation, extraída de tu consola, y tus propias copias
  de los juegos. No se incluye ninguna de las dos.

### Instalación

Cada release trae dos descargas:

- `DuckStationPS5-<versión>.zip`: la app y sus carpetas.
- `duckstation-windows-x64-release.zip`: el build oficial de DuckStation para
  el que se hizo el release, tal cual lo publicaron sus autores (ver
  [Qué DuckStation](#qué-duckstation)).

1. Descomprime `DuckStationPS5-<versión>.zip`. Copia por FTP las dos carpetas
   que trae, `homebrew` y `DuckStationPS5`, en `/data` de la PS5.
2. Descomprime `duckstation-windows-x64-release.zip` en
   `/data/DuckStationPS5/duckstation/`, de modo que esa carpeta contenga
   `duckstation-qt-x64-ReleaseLTCG.exe`.
3. Pon tu BIOS en `/data/DuckStationPS5/bios/`.
4. Pon tus juegos en `/data/DuckStationPS5/games/` (`.cue`/`.bin`, `.chd`,
   `.pbp`, `.iso`, `.m3u`; puedes usar una carpeta por juego).
5. Reinicia ShadowMountPlus (o la consola). **DuckStation PS5** aparece en el
   home.

DuckStation guarda también ahí, en `/data/DuckStationPS5/`, sus ajustes,
tarjetas de memoria, estados guardados y capturas.

### Jugar

Abre **DuckStation PS5** desde el home. Viene listo para jugar: el DualSense
es el mando de PlayStation, los juegos de `/data/DuckStationPS5/games/` salen
en la **Game List** y la imagen se dibuja con Vulkan a seis veces la
resolución original, con PGXP, y llena la pantalla 16:9: los juegos en 3D se
amplían a panorámico, y los de fondos prerrenderizados, que no lo admiten, se
estiran. Puedes cambiar todo en **Settings**, para todos los juegos o por
juego.

#### Controles

| DualSense | En un juego |
|---|---|
| Botones, sticks, cruceta, L1/R1/L2/R2 | los del mando de PlayStation (analógico) |
| Options | Start |
| Create | Select |
| **Touchpad** | el menú de DuckStation: guardar y cargar estados, ajustes, trucos, cambiar disco, salir |
| **Mantener L3 + R3** (los dos sticks) | avance rápido, mientras los mantienes |

En los menús de DuckStation: cruceta o stick izquierdo para moverte, X para
elegir, Círculo para volver. **Exit** en el menú principal (elige cerrar
DuckStation) te devuelve al home de la PS5.

#### Packs de texturas

Pon el pack en `/data/DuckStationPS5/textures/<serial>/` (por ejemplo
`textures/SLES-03225/`, el serial del juego tal como sale en la Game List).
Los packs de fondos (`vram-write-*.png`) cargan solos. Los del formato nuevo
(`texpage-*.png`) necesitan además la caché de texturas: en **Game Properties >
Graphics > Texture Replacements** del juego, activa **Enable Texture Cache**.

### Qué DuckStation

Cada release indica en la tabla de arriba ([Which DuckStation](#which-duckstation))
el build oficial con el que va: su versión, su commit y el SHA-256 del zip.
Usa el zip del mismo release: la app está probada con ese build. El
actualizador de DuckStation no funciona en la consola; un DuckStation nuevo
llega con un nuevo release de DuckStation PS5.

### Créditos

- [DuckStation](https://www.duckstation.org/), de Stenzek y sus colaboradores,
  bajo CC BY-NC-ND 4.0. Este proyecto no está afiliado a DuckStation: incluye
  el release oficial sin cambios, como descarga aparte, y su icono es el pato
  de DuckStation.
- La app ejecuta DuckStation mediante
  [prospero-win](https://github.com/mpereiraesaa/prospero-win) (LGPL-2.1), con
  Wine, el driver RADV de Mesa y FreeType. `homebrew/PPSA99990` lleva sus
  licencias y la revisión de cada parte (`SOURCES.txt`).
- PlayStation es una marca de Sony Interactive Entertainment. No se incluye
  ninguna BIOS, juego ni software de Sony.
