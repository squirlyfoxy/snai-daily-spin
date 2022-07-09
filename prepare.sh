pip install selenium
# if -firefox
if [ "$1" = "-firefox" ]; then
    wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
    tar -xvzf geckodriver-v0.31.0-linux64.tar.gz
    chmod +x geckodriver
else
    echo "$1 is not supported, supported browsers are: "
    echo "Firefox -> Use -firefox"
fi