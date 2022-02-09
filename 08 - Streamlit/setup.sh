mkdir -p ~/.streamlit/
cat <<-EOF > ~/.streamlit/config.toml
[server]
headless = true
port = $PORT
enableCORS = false

[theme]
primaryColor="#303e75"
backgroundColor="#d7e3ec"
secondaryBackgroundColor="#ced7e2"
textColor="#020531"
EOF
