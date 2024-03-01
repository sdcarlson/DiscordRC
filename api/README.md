## Installation

1. Create virtual environment: `python3 -m venv venv`
2. Activate virtual environment: `. venv/bin/activate` (if you're using bash)
3. Install dependencies: `pip3 install -r requirements.txt`
4. Set up database in docker: `./mongo_setup.sh`
5. Run: `cd .. && uvicorn api.main:app --reload`

To see the API documentation, go to http://localhost:8000/docs after running.