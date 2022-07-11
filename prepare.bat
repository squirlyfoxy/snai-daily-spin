@echo off

pip install selenium
goto :parse

:firefox
    curl https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip --output geckodriver-v0.31.0-win64.zip
    externals/zipjs.bat unzip -source geckodriver-v0.31.0-win64.zip

:chrome
    curl https://chromedriver.storage.googleapis.com/2.41/chromedriver_win32.zip --output chromedriver_win32.zip
    externals/zipjs.bat unzip -source chromedriver_win32.zip

:parse
    if /i "%~1"=="firefox"  goto firefox & goto end
    if /i "%~1"=="chrome" goto chrome & goto end

    echo "Usage: prepare.bat [-firefox|-chrome]"

:end
    exit
