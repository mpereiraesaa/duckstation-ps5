#!/usr/bin/env python3
"""Put DuckStation PS5's package together from prospero-win's builds.

    tools/make_package.py --prospero-win DIR --title DIR --host-wine DIR
                          --duckstation-zip FILE --version VERSION --out DIR

The package unzips into the console's /data:

    homebrew/PPSA99990/      the app: the title (tools/build_native.sh with
                             DuckStation PS5's identity) and the Wine runtime
    DuckStationPS5/          the user's folder
      duckstation/           the official DuckStation build goes here
      bios/  games/          the BIOS and the games
      settings.ini           DuckStation's, ready to play: Vulkan, 16:9 full
                             screen, the DualSense on port 1, the games folder
      system/                the app's profile and Wine prefix

DuckStation itself is not in it: the official release zip ships beside it,
unchanged. --duckstation-zip only names that zip, to record its SHA-256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLE_ID = "PPSA99990"
DATA = "DuckStationPS5"
DATA_ON_CONSOLE = f"/data/{DATA}"
# What the PS5 cannot use: import libraries and the drivers that need the
# PC's own libraries (as prospero-win's tools/package_release.sh leaves out).
PC_ONLY = {"winex11.drv", "winegstreamer.dll", "wpcap.dll", "sane.ds", "gphoto2.ds"}
RECIPE = """\
name: DuckStation
game_slug: duckstation
runner: wine
prospero:
  graphics: auto
script:
  game:
    exe: drive_c/windows/system32/notepad.exe
    prefix: $GAMEDIR
  installer:
  - task: {name: create_prefix, prefix: $GAMEDIR, arch: win64}
"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def copy_tree(source: Path, dest: Path, skip=lambda name: False) -> None:
    for item in sorted(source.rglob("*")):
        if item.is_file() and not skip(item.name):
            target = dest / item.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def app_folder(args: argparse.Namespace, app: Path) -> dict:
    """The title and its Wine runtime, as prospero-win's packager lays them out."""
    pw = args.prospero_win
    wine_ps5 = pw / ".deps" / "wine-ps5"
    report = json.loads((wine_ps5 / "report.json").read_text())
    if args.libvulkan:
        # A RADV libvulkan.prx built apart from this Wine build, with its sources.
        report["sources"].update(ps5_mesa=args.ps5_mesa, ps5_vulkan=args.ps5_vulkan)
    elif not (wine_ps5 / "prx" / "sce_module" / "libvulkan.prx").exists() or not report["sources"].get("ps5_mesa"):
        sys.exit("make_package: the PS5 Wine build has no RADV libvulkan.prx (build_wine_ps5.sh --radv)")
    copy_tree(args.title, app, skip=lambda name: name == "dev.conf")
    lib, share = app / "win" / "wine" / "lib" / "wine", app / "win" / "wine" / "share" / "wine"
    for arch in ("i386-windows", "x86_64-windows"):
        for module in sorted((args.host_wine / "lib" / "wine" / arch).iterdir()):
            if module.is_file() and module.suffix != ".a" and module.name not in PC_ONLY:
                (lib / arch).mkdir(parents=True, exist_ok=True)
                shutil.copy2(module, lib / arch / module.name)
        if (wine_ps5 / "pe" / arch).is_dir():
            for module in (wine_ps5 / "pe" / arch).glob("*.dll"):
                shutil.copy2(module, lib / arch / module.name)
    copy_tree(wine_ps5 / "prx" / "sce_module", lib / "x86_64-unix")
    if args.libvulkan:
        shutil.copy2(args.libvulkan, lib / "x86_64-unix" / "libvulkan.prx")
    copy_tree(args.host_wine / "share" / "wine" / "nls", share / "nls")
    copy_tree(wine_ps5 / "prx" / "fonts", share / "fonts")
    # The console refuses an eboot or a module without execute permission.
    for module in [app / "eboot.bin", *app.rglob("*.prx")]:
        module.chmod(0o755)
    # The licences: prospero-win's own and its notices, Wine's and FreeType's.
    shutil.copy2(pw / "LICENSE", app / "LICENSE")
    shutil.copy2(pw / "THIRD_PARTY.md", app / "THIRD_PARTY.md")
    copy_tree(pw / "LICENSES", app / "LICENSES")
    for name in ("LICENSE", "COPYING.LIB", "AUTHORS", "NOTICES.md"):
        (app / "LICENSES" / "wine").mkdir(parents=True, exist_ok=True)
        shutil.copy2(wine_ps5 / "source" / name, app / "LICENSES" / "wine" / name)
    (app / "LICENSES" / "freetype").mkdir(parents=True, exist_ok=True)
    for name in ("LICENSE.TXT", "docs/FTL.TXT"):
        shutil.copy2(wine_ps5 / "freetype" / "src" / name, app / "LICENSES" / "freetype")
    return report


def prefix_folder(args: argparse.Namespace, dest: Path) -> None:
    """A fresh Wine prefix, written as the console reads it: links
    that stay inside become .pw-symlinks tables (prospero-win's pw_prefix), and
    two more point into the user's folder: D: and Documents\\DuckStation, the
    folder DuckStation keeps its data in when it exists."""
    pw = args.prospero_win
    sys.path.insert(0, str(pw / "tools"))
    import pw_prefix  # noqa: E402  (prospero-win's own link and registry rules)

    with tempfile.TemporaryDirectory() as work:
        recipe = Path(work) / "duckstation.yml"
        recipe.write_text(RECIPE)
        library = Path(work) / "library"
        subprocess.run([sys.executable, str(pw / "tools" / "pw_install.py"), str(recipe),
                        "--library", str(library), "--wine", str(args.host_wine / "bin" / "wine")],
                       check=True, stdout=subprocess.DEVNULL)
        prefix = library / "prefixes" / "duckstation"
        files, dirs, links = pw_prefix.local_tree(prefix)
        for directory in sorted(dirs):
            (dest / directory).mkdir(parents=True, exist_ok=True)
        for key, path in sorted(files.items()):
            target = dest / key
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(pw_prefix.to_console(key, path.read_bytes()))
        links.setdefault("dosdevices", {})["d:"] = DATA_ON_CONSOLE
        links.setdefault("drive_c/users/prospero/Documents", {})["DuckStation"] = DATA_ON_CONSOLE
        (dest / "drive_c" / "users" / "prospero" / "Documents").mkdir(parents=True, exist_ok=True)
        for directory, table in links.items():
            text = "".join(f"{name}\t{target}\n" for name, target in sorted(table.items()))
            (dest / directory / pw_prefix.LINK_TABLE).write_text(text)


def data_folder(args: argparse.Namespace, data: Path) -> None:
    for folder, note in (("duckstation", "PUT-DUCKSTATION-HERE.txt"), ("bios", "PUT-BIOS-HERE.txt"),
                         ("games", "PUT-GAMES-HERE.txt")):
        (data / folder).mkdir(parents=True)
        shutil.copy2(ROOT / "data" / note, data / folder / note)
    shutil.copy2(ROOT / "data" / "settings.ini", data / "settings.ini")
    profiles = data / "system" / "profiles"
    profiles.mkdir(parents=True)
    shutil.copy2(ROOT / "data" / "duckstation.profile", profiles / "duckstation.profile")
    (profiles / "profiles.lst").write_text("duckstation.profile\n")
    prefix_folder(args, data / "system" / "prefixes" / "duckstation")


def sources(args: argparse.Namespace, report: dict, out: Path) -> None:
    pw = args.prospero_win
    git = lambda *a: subprocess.run(["git", "-C", str(pw), *a], capture_output=True, text=True).stdout.strip()
    commit = git("rev-parse", "HEAD") + (" (with uncommitted changes)" if git("status", "--porcelain") else "")
    lapy = json.loads((pw / "build" / "native" / "lapy-helper-release.json").read_text())
    src = report["sources"]
    lines = [
        f"DuckStation PS5 {args.version}",
        "",
        "Made for the official DuckStation build, unchanged, that ships beside this package:",
        f"  {args.duckstation_zip.name}  SHA-256 {sha256(args.duckstation_zip)}",
        "",
        "Runtime (homebrew/PPSA99990):",
        f"  prospero-win  https://github.com/mpereiraesaa/prospero-win  commit {commit}",
        f"  Wine  https://gitlab.winehq.org/wine/wine  commit {report['wine_commit']},"
        f" with prospero-win's patches ({len(report['patches'])})",
        f"  RADV (libvulkan.prx)  https://github.com/mpereiraesaa/PS5_Mesa  commit {src['ps5_mesa']},",
        f"    linked by https://github.com/mpereiraesaa/PS5_Vulkan  commit {src.get('ps5_vulkan')}",
        f"  Lapy JB Daemon (lapy.elf)  {lapy.get('release_url')}",
    ]
    mihawkgen = pw / "third_party" / "mihawkgen" / "COMMIT"
    if mihawkgen.is_file():
        lines.append(f"  MihawkGen (frame generation, in libvulkan.prx)  https://github.com/mihawk-99/PS5_MihawkGen"
                     f"  commit {mihawkgen.read_text().strip()}")
    lines += [
        "",
        "THIRD_PARTY.md and LICENSES/ in the app folder say what each part is and its licence.",
    ]
    (out / "SOURCES.txt").write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for name in ("prospero-win", "title", "host-wine", "duckstation-zip", "out"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--libvulkan", type=Path, help="a RADV libvulkan.prx built apart (needs --ps5-mesa)")
    parser.add_argument("--ps5-mesa", help="the PS5_Mesa commit --libvulkan was built from")
    parser.add_argument("--ps5-vulkan", help="the PS5_Vulkan commit that linked it")
    args = parser.parse_args()
    if args.libvulkan and not args.ps5_mesa:
        parser.error("--libvulkan needs --ps5-mesa")
    out = args.out / f"DuckStationPS5-{args.version}"
    if out.exists():
        shutil.rmtree(out)
    report = app_folder(args, out / "homebrew" / TITLE_ID)
    data_folder(args, out / DATA)
    sources(args, report, out / "homebrew" / TITLE_ID)
    shutil.copy2(ROOT / "README.md", out / "README.md")
    archive = args.out / f"DuckStationPS5-{args.version}.zip"
    archive.unlink(missing_ok=True)
    subprocess.run(["zip", "-qr", str(archive), "homebrew", DATA, "README.md"], cwd=out, check=True)
    print(f"make_package: {archive} ({archive.stat().st_size // (1 << 20)} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
