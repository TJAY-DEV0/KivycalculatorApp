[app]
title = Calculator
package.name = calculator
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,jpeg
source.include_patterns = assets/*,images/*
version = 0.1
requirements = python3,kivy,numpy,numexpr,cython
orientation = portrait

[android]
fullscreen = 0
android.api = 33
android.permissions = android.permission.READ_MEDIA_IMAGES, android.permission.READ_MEDIA_VIDEO
android.build_tools_version = 30.0.3
android.accept_sdk_license = True