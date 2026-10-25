#!/bin/sh
# Build a DuckStation PS5 release.
#
#   ./build.sh PROSPERO_WIN DUCKSTATION_ZIP VERSION [OUT]
#
# PROSPERO_WIN is a prospero-win checkout where these have run:
#   tools/build_wine_ps5.sh --radv <PS5_Vulkan checkout>   the PS5 Wine and RADV
#   tools/build_host_wine.sh                               the PC Wine: PE modules
# DUCKSTATION_ZIP is duckstation-windows-x64-release.zip, the official build
# the release is made for: its duck becomes the icon, and its SHA-256 is
# recorded. It ships beside the package, unchanged, never inside it.
# OUT (default ./release) gets DuckStationPS5-VERSION.zip.
#
# Without a RADV build in PROSPERO_WIN's Wine build, RADV_LIBVULKAN names a
# RADV libvulkan.prx built apart, with RADV_PS5_MESA and RADV_PS5_VULKAN the
# PS5_Mesa and PS5_Vulkan commits it came from.
set -eu

[ $# -ge 3 ] || { sed -n '2,17p' "$0"; exit 2; }
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
pw=$(CDPATH= cd -- "$1" && pwd)
zip=$(realpath "$2")
version=$3
out=$(mkdir -p "${4:-$root/release}" && CDPATH= cd -- "${4:-$root/release}" && pwd)
work=$out/work
rm -rf "$work"
mkdir -p "$work"

# The icon: DuckStation's own duck, from the official zip.
unzip -q -o -j "$zip" resources/images/duck.png -d "$work"
python3 "$root/tools/make_icon.py" "$work/duck.png" "$work/icon0.png"

# The title: prospero-win's, as a single-program title with its own identity
# and the /data helper built for PPSA99990.
PW_FOUNDATION_READY=${PW_FOUNDATION_READY:-1} \
PW_TITLE_ID=PPSA99990 PW_TITLE_NAME="DuckStation PS5" PW_TITLE_ICON="$work/icon0.png" \
PW_DATA_ROOT=/data/DuckStationPS5/system PW_FIXED_PROFILE=duckstation \
PW_LAPY_RELEASE=v0.3.2-experimental-ppsa99990 \
PW_LAPY_ELF_SHA256=5b17b527b97d28ea8a5bbf2a30bb679d7e6987bda321bcda1b9d1b6d0008e453 \
    bash "$pw/tools/build_native.sh"

set -- --prospero-win "$pw" --title "$pw/dist/PPSA99990" \
    --host-wine "$pw/.deps/wine-host/install/usr" --duckstation-zip "$zip" \
    --version "$version" --out "$out"
if [ -n "${RADV_LIBVULKAN:-}" ]; then
    set -- "$@" --libvulkan "$RADV_LIBVULKAN" --ps5-mesa "${RADV_PS5_MESA:?}" --ps5-vulkan "${RADV_PS5_VULKAN:?}"
fi
python3 "$root/tools/make_package.py" "$@"
rm -rf "$work"
