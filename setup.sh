curso_python_zero_ao_ds -p ~/.streamlit/

echo "\
[general]\n\
email = \"danillo_barros@live.com\"\n\
" > ~/.streamlit/credentials.toml


echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml