from src import create_app

app = create_app()
if __name__ == '__main__':
    # app.run(debug=True) Para rodar na maquina
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
