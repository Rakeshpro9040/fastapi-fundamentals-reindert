python -c "import sys; print(sys.prefix != sys.base_prefix)"
python -m pip install "fastapi[all]"
- Here [all] inidicates to install all dependent libs
uvicorn carsharing:app --reload
- Here carsharing is the app name
- reload is to auto reload the app whenever we make changes
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc