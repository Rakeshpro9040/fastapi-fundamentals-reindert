### Note**:** Local repo is available in testpocwindows, so practice here!

### python -c "import sys; print(sys.prefix != sys.base_prefix)"
### python -m pip install "fastapi[all]"
- Here [all] indicates to install all dependent libs<br>
- Main dependent lib is the uvicorn server

### uvicorn carsharing:app --reload
- This is to run the fastapi app
- Here carsharing is the app name
- reload is to auto reload the app whenever we make changes<br>

### Test urls
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Kill process
When running debugger, make sure to kill any existing processes!
### Windows
- netstat -ano | findstr :8000
- taskkill /F /PID PID
### Mac
- lsof -i :8000
- kill PID

## Models
- Fastapi uses Pydantic BaseModel
- refer pydantic foc for more details

## SQLModel
- Built on SQLAlchemy + Pydantic
- SQLAlchemy to read various databases using ORM
- Model classes are Pydantic Models, easily integrated with FastAPI
- Object-Relation Mapping: Classes=Tables, Objects=Rows, Attributes=Columns
- python -m pip install sqlmodel