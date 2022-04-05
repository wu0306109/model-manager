# Set up the Local Enviornment

## Language Formattor

1. Python: [yapf](https://github.com/google/yapf) with default setting

## Lauch locally

1. [Install Docker Engine](https://docs.docker.com/engine/install/)
2. launch.json

   ```json
   {
     "configurations": [
       {
         "name": "Docker: Python - Flask",
         "type": "docker",
         "request": "launch",
         "preLaunchTask": "docker-run: debug",
         "python": {
           "pathMappings": [
             { "localRoot": "${workspaceFolder}", "remoteRoot": "/app" }
           ],
           "projectType": "flask"
         },
         "env": {
           "GOOGLE_APPLICATION_CREDENTIALS": "PATH_TO_CREDENTIAL_FILE"
         }
       }
     ]
   }
   ```

3. press `F5`

## Unit Test

```shell
>>> pytest

===================================================== test session starts =====================================================
platform darwin -- Python 3.9.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /Users/yangshengwu/Desktop/1102 OOAD/model-manager
plugins: anyio-3.5.0
collected 1 item

tests/test_model_manager.py .                                                                                           [100%]

====================================================== 1 passed in 0.08s ======================================================
```

## References

1. https://flask.palletsprojects.com/en/2.1.x/
