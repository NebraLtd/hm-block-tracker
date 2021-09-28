## VM Installation

- Create new VM in GCP
  + I found 2GB RAM caused heap size reached error during snapshot, so upped instance size to 8GB RAM (e2-standard-2)
  + Ubuntu 20.04 LTS used, but below instructions probably work with most recent Debian variants.
- Update OS
  + sudo su
  + apt-get update
  + apt-get upgrade
- Install Docker
  + apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
  + curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  + echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  + apt-get update
  + apt-get install docker-ce docker-ce-cli containerd.io
- Create directory for the miner data
  + mkdir /var/miner_data
- Run miner container
  + docker run --volume /var/miner_data:/var/data -d -p 127.0.0.1:4467:4467 --restart=always --name miner quay.io/team-helium/miner:latest-amd64



