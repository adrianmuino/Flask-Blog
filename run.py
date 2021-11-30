from flaskblog import create_app

app = create_app() # Pass custom configurations to the app if desired, else default configs are used

# Use `python run.py` to run in debug
if __name__ == "__main__":
    app.run(debug=True)