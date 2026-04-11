sudo docker build . -t ml-client
sudo docker run -it --rm ml-client bash
sudo docker rmi ml-client
