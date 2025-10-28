[app]
title =  Calculator
package.name = kivycalculator
package.domain = org.kivy.calculator
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,cython,pyjnius,https://github.com/kivy/pyjnius/archive/master.zip
orientation = portrait
fullscreen = 0
android.api = 34
android.ndk = 25b
android.ndk_api = 21
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.skip_update = False

# Optional but good practice
presplash.filename = %(source.dir)s/assets/images/optimal_logo.jpg
icon.filename = %(source.dir)s/assets/images/app_logo.png

# (Disabled because GitHub workflow handles signing)
# android.release = True
# android.release_keystore = myapp.jks
# android.release_keyalias = myalias
# android.store_password = 838875
# android.key_password = 838875

# (Optional) Reduce app size
# android.strip = True
# android.log_level = 2

# (Optional) Enable for extra modules
# android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1