# Current Process on ML Client

1. Use `./docker-run.sh` to activate the machine learning docker container.
2. Images taken by hardware devices are stored under `/shared/img` within the container.
3. The `core` reads the images in `/shared/img` and analyzes how focus the user is.
4. The results are stored as `result.json` in `/app/output`, waiting to be transferred to MongoDB.

## Several Important Things

1. The camera controller is supposed to store all the images it captures under the directory: `/shared/img/`

