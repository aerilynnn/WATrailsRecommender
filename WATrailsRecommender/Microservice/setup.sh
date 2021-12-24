mkdir -p ~/.streamlit/
echo "[general]
email = \"aerilynnn@gmail.com\"
" > ~/.streamlit/credentials.toml
echo "[theme]
base='light'
primaryColor='#c70506'
secondaryBackgroundColor='#8e7135'
textColor='#093f07'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
