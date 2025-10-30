[app]
title = Calculator
package.name = kivycalculator
package.domain = org.tjaydev
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,cython,pyjnius,https://github.com/kivy/pyjnius/archive/master.zip
orientation = portrait
fullscreen = 1
android.permissions = INTERNET

# Optional icons (replace paths if you have your own)
icon.filename = assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 0
builddir = .buildozer

[android]
# Your signing key details
android.release_keystore = my-release-key.jks
android.release_keyalias = myalias
android.keyalias_passwd = yourpassword
android.keystore_passwd = yourpassword
android.arch = armeabi-v7a

# Use prebuilt binaries to speed up builds
p4a.local_recipes = false
p4a.branch = master
p4a.bootstrap = sdl2
android.ndk_api = 21

# Disable building hostpython from source
android.accept_sdk_license = True