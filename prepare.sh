pip install selenium
if [ "$1" = "-firefox" ]; then
    wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
    tar -xvzf geckodriver-v0.31.0-linux64.tar.gz
    chmod +x geckodriver
else if [ "$1" = "-chrome" ]; then
    wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    chmod +x chromedriver
else
    echo "$1 is not supported, supported browsers are: "
    echo "Firefox -> Use -firefox"
    echo "Chrome -> Use -chrome"
fi
fi