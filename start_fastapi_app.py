import uvicorn
from fastapi_app.app import app

uvicorn.run(app, host='0.0.0.0', port=8000)
