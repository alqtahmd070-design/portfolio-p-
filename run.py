import uvicorn
from backend.config import HOST, PORT

if __name__ == "__main__":
    print(f"============================================================")
    print(f"  El Kot Luxury Cars - Starting Full-Stack Application")
    print(f"  Server URL:    http://{HOST}:{PORT}/")
    print(f"  Swagger Docs:  http://{HOST}:{PORT}/docs")
    print(f"  Single HTML:   http://{HOST}:{PORT}/ (index.html)")
    print(f"============================================================")
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
