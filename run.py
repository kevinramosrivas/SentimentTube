
from application import create_app

# load_dotenv(dotenv_path='.flaskenv')
app = create_app()

def main():
    app.run(host='127.0.0.1', port=105, debug=True)

if __name__ == '__main__':
    main()