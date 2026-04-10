mkdir -p ~/.streamlit/
echo "\
[server]\n\
[server]\n\
port=$PORT\n\
enabless=false\n\
headless=true\n\
\n\
" > ~/.streamlit/config.toml
