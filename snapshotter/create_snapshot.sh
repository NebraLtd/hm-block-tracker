#!/bin/bash

export PATH=$PATH:/usr/bin:/snap/bin

if [ "$PRODUCTION" == "1" ]; then
    SNAPSHOT_BUCKET='helium-snapshots.nebra.com'
else
    SNAPSHOT_BUCKET='helium-snapshots-stage.nebra.com'
fi

docker exec miner miner snapshot take /var/data/saved-snaps/latest
BLOCK_HEIGHT=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest | head -1 | awk {'print $2'})
BLOCK_HASH_PART1=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest | tail -3 | head -1 | awk {'print $2'})
BLOCK_HASH_PART2=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest | tail -2 | head -1 | awk {'print $1'})
BYTE_ARRAY="${BLOCK_HASH_PART1}${BLOCK_HASH_PART2}"
BASE64URL_FORMAT=$(python3 base64url_encoder.py "$BYTE_ARRAY")

mv /var/miner_data/saved-snaps/latest /var/miner_data/saved-snaps/snap-$BLOCK_HEIGHT
echo "{\"height\": $BLOCK_HEIGHT, \"hash\": \"$BYTE_ARRAY\"}" > /var/miner_data/saved-snaps/latest.json
echo "{\"height\": $BLOCK_HEIGHT, \"hash\": \"$BASE64URL_FORMAT\"}" > /var/miner_data/saved-snaps/latest-snap.json

gsutil cp /var/miner_data/saved-snaps/snap-$BLOCK_HEIGHT "gs://$SNAPSHOT_BUCKET/snap-$BLOCK_HEIGHT"
gsutil cp /var/miner_data/saved-snaps/latest.json "gs://$SNAPSHOT_BUCKET/latest.json"
gsutil cp /var/miner_data/saved-snaps/latest-snap.json "gs://$SNAPSHOT_BUCKET/latest-snap.json"

rm docker.config
rm /var/miner_data/saved-snaps/snap-$BLOCK_HEIGHT
