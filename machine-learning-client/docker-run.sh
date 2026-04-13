sudo docker build . -t ml-client

clear
sudo docker run -it --rm -u $(id -u):$(id -g) -v $(pwd):/app -v $(pwd)/../img:/shared/img -w /app ml-client bash
sudo docker rmi ml-client
sudo docker builder prune
clear