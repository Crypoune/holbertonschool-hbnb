from app import create_app

app = create_app(config_name='development')

if __name__ == '__main__':
    print("Running on http://127.0.0.1:5000/api/v1/")
    app.run(debug=True)