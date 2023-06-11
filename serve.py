import uvicorn

host = "0.0.0.0"
port = 8080
app_name = "nabla.main:app"

if __name__ == "__main__":
    uvicorn.run(app_name, host=host, port=port, log_config=None)
