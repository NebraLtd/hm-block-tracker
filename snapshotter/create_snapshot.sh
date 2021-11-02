#!/bin/bash

export PATH=$PATH:/usr/bin:/snap/bin

if [ "$PRODUCTION" == "1" ]; then
    TARGET_BUCKET='helium-snapshots.nebra.com'
else
    TARGET_BUCKET='helium-snapshots-stage.nebra.com'
fi

docker exec miner miner snapshot take /var/data/saved-snaps/latest
BLOCK_HEIGHT=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest | head -1 | awk {'print $2'})
BLOCK_HASH_PART1=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest | tail -3 | head -1 | awk {'print $2'})
BLOCK_HASH_PART2=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest | tail -2 | head -1 | awk {'print $1'})
mv /var/miner_data/saved-snaps/latest /var/miner_data/saved-snaps/snap-$BLOCK_HEIGHT
echo "{\"height\": $BLOCK_HEIGHT, \"hash\": \"$BLOCK_HASH_PART1$BLOCK_HASH_PART2\"}" > /var/miner_data/saved-snaps/latest.json
gsutil cp /var/miner_data/saved-snaps/snap-$BLOCK_HEIGHT "gs://$TARGET_BUCKET/snap-$BLOCK_HEIGHT"
gsutil cp /var/miner_data/saved-snaps/latest.json "gs://$TARGET_BUCKET/latest.json"
rm /var/miner_data/saved-snaps/snap-$BLOCK_HEIGHT
