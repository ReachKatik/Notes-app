from website import create_app

app = create_app()

# helps us to run main.py when directly called otherwise it wont
if __name__ == '__main__':
    app.run(debug=True)