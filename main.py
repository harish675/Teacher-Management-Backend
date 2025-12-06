import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from src.app import app  # noqa: E402

import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(app, port=int(os.getenv("PORT")), reload=True)