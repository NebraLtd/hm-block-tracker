#!/bin/bash
export PATH=$PATH:/usr/bin:/snap/bin
docker exec miner miner snapshot take /var/data/saved-snaps/latest
BLOCK_HEIGHT=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest | head -1 | awk {'print $2'})
BLOCK_HASH=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest | tail -2 | head -1 | awk {'print $
2'} | sed 's/[()<>"]//g')
mv /var/miner_data/saved-snaps/latest /var/miner_data/saved-snaps/snap-$BLOCK_HEIGHT
echo "{\"height\": $BLOCK_HEIGHT, \"hash\": \"$BLOCK_HASH\"}" > /var/miner_data/saved-snaps/latest.json
gsutil cp /var/miner_data/saved-snaps/snap-$BLOCK_HEIGHT gs://nebra-snapshots/snap-$BLOCK_HEIGHT
gsutil cp /var/miner_data/saved-snaps/latest.json gs://nebra-snapshots/latest.json
rm /var/miner_data/saved-snaps/snap-$BLOCK_HEIGHT
