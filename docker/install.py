#sudo docker volume create -d local --opt type=tmpfs --opt device=tmpfs --opt o=size=2g data_source
#sudo docker build -t sam:v1 .