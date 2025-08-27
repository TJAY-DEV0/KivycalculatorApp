[app]
# (str) Title of your application
title = Calculator

# (str) Package name
package.name = CalculatorApp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) The file extensions to include in the build, comma separated.
source.include_exts = py,png,jpg,kv,atlas,json

# (list) The directories to include in the build, comma separated.
source.include_dirs = assets,check,files,others,switch

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = openssl,kivy
requirements = kivy,kivymd,cython,numexpr,numpy

# (list) Android permissions
# e.g. android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Presplash of the application
android.presplash_filename = assets/images/optimal_logo.jpg

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = False

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 33

# (str) Android NDK version to use
# The build will automatically find a compatible NDK, no need to specify it.
# You can remove the android.ndk and android.build_tools_version lines
# if they are present.

# (int) Android build tools version
android.build_tools_version = 30.0.3

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) Android NDK version to use
# android.ndk = 25b

#
# OSX specific
#

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1

#
# iOS specific
#

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

#
# Buildozer specific
#

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) python-for-android URL to use for checkout
p4a.url = https://github.com/kivy/python-for-android.git

# (str) python-for-android branch to use
p4a.branch = develop 
