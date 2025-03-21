from app import create_app  # Importing the function to create the app

app = create_app()          # Initializing the app instance

if __name__ == "__main__":  # Entry point of the script
    app.run(debug=True)     # Running the app in debug mode
