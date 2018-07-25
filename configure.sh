echo "Configuring..."
python -m pip install --upgrade pip
python -m pip install lxml
python -m pip install bs4
python -m pip install requests
git submodule update --init --recursive --remote
echo "Success! You should be good to go! :)" 
