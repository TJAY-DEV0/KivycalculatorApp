[app]
title = Kivy Calculator
package.name = kivycalculator
package.domain = org.tjaydev
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 34
android.minapi = 24
android.ndk = 27b

android.release_keystore = new-release-key.jks
android.release_keyalias = myalias
android.keyalias_passwd = yourpassword
android.keystore_passwd = yourpassword
android.arch = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
