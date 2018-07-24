echo "Configuring..."
python -m pip install --upgrade pip
python -m pip install lxml
git submodule update --init --recursive --remote
echo "Success! You should be good to go! :)" 
