# Snapshotter

This rough guide provides instructions on how to configure a GCP instance for spitting out snapshots to GCS on crontab. We
will use this to provide private snapshots to Nebra customers for faster syncing than the upstream blessed snapshots.

## Installation
### VM Installation

* Create new VM in GCP
  * I found 2GB RAM caused heap size reached error during snapshot, so upped instance size to 4GB RAM (e2-medium)
  * Ubuntu 20.04 LTS used, but below instructions probably work with most recent Debian variants.
* Update OS
  * `sudo su`
  * `apt-get update`
  * `apt-get upgrade`
* Install Docker
  * `apt-get install apt-transport-https ca-certificates curl gnupg lsb-release`
  * `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`
  * `echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
  * `apt-get update`
  * `apt-get install docker-ce docker-ce-cli containerd.io`
* Create directory for the miner data
  * `mkdir /var/miner_data`
  * `chmod 755 /var/miner_data`
* Create directory for the miner config and copy in sys.config from the repo
  * `mkdir /var/miner_config`
  * `cp <repo_base_dir>/snapshotter/sys.config /var/miner_config/.`
* Run miner container
  * `docker run --volume /var/miner_config:/opt/miner/config --volume /var/miner_data:/var/data -d -p 127.0.0.1:4467:4467 --restart=always --name miner quay.io/team-helium/miner:latest-amd64`
* Fetch the latest snapshot from upstream bucket, you can find the <block> height of the latest snapshot from the API - https://api.helium.io/v1/snapshots
  * `cd /var/miner_data/saved-snaps; wget https://snapshots.helium.wtf/mainnet/snap-<block>`
* Import the snapshot
  * `docker exec miner miner snapshot load /var/data/saved-snaps/snap-<block>`
* Initialise Google Cloud Service Account on the instance by following this guide... https://gist.github.com/ryderdamen/926518ddddd46dd4c8c2e4ef5167243d
* Create a user to perform snapshotting and add it to the Docker group.
  * `useradd --shell /bin/bash snapshot`
  * `usermod -G docker snapshot`
* Assume the user and checkout the Github repository into their home directory.
  * `su - snapshot`
  * `git clone https://github.com/NebraLtd/hm-block-tracker.git`
* Create appropriate SystemD configurations in /etc/systemd/system based on the sample files in the repository
  * `vi /etc/systemd/system/snapshot.service`
  * `vi /etc/systemd/system/snapshot.timer`
* Test functionality
  * `systemctl start snapshot.service`
  * Should complete cleanly synchronously in the user's shell
* Once happy enable the timer
  * `systemctl enable snapshot.timer`


### Google Cloud Storage Bucket

#### Set up helium-snapshots buckets

```
$ gsutil mb \
    -p nebra-production \
    -c standard \
    -l us \
    gs://{helium-snapshots,helium-snapshots-stage}.nebracdn.com

$ gsutil iam ch allUsers:objectViewer \
    gs://{helium-snapshots,helium-snapshots-stage}.nebracdn.com

$ gsutil ubla set on \
    gs://{helium-snapshots,helium-snapshots-stage}.nebracdn.com

$ gsutil lifecycle set misc/snapshots_lifecycle.json \
    gs://{helium-snapshots,helium-snapshots-stage}.nebracdn.com

```
