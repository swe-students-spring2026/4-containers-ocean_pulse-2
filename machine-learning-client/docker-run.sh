sudo docker build . -t ml-client

clear
sudo docker run -it --rm -v $(pwd):/app -w /app ml-client bash
sudo docker rmi ml-client
clear