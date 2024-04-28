pkill python
pkill -f chromium-browser
cd ./webui
../venv/bin/python ./app.py &
cd ..
./venv/bin/python ./facial_detection/demo.py &
#export DISPLAY=:1
chromium-browser --kiosk http://localhost:5000/
