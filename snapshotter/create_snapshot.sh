#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

export PATH=$PATH:/usr/bin:/snap/bin

if [ "$PRODUCTION" == "1" ]; then
    SNAPSHOT_BUCKET='helium-snapshots.nebracdn.com'
else
    SNAPSHOT_BUCKET='helium-snapshots-stage.nebracdn.com'
fi


# Let's first start by sanity checking that the miner works as expected
CURRENT_MINER_HEIGHT=$(docker exec miner miner info height | awk {'print $2'})
CURRENT_SNAPSHOT_HEIGHT=$(curl -s https://$SNAPSHOT_BUCKET/latest-snap.json | jq .height &2>/dev/null)
if [[ "failed" == *"$CURRENT_MINER_HEIGHT"* ]]; then
    echo "Got error from miner. Restarting miner and exiting."
    docker restart miner
    exit 0
fi

if [ "$CURRENT_SNAPSHOT_HEIGHT" -gt "$CURRENT_MINER_HEIGHT" ]; then
    echo "The remote snapshot is ahead of the current miner. Exiting."
    exit 0
fi


# Initial sanity checks passed. Continuing on with a snapshot.
echo "About to take snapshot"
# Sometimes the snapshot times out and needs more time to finish
docker exec miner miner snapshot take /var/data/saved-snaps/latest || (echo "Snapshot still loading, sleeping..." && sleep 60)

echo "Parsing snapshot (1/3)"
BLOCK_HEIGHT=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest.gz | head -1 | awk {'print $2'})

echo "Parsing snapshot (2/3)"
BLOCK_HASH_PART1=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest.gz | tail -3 | head -1 | awk {'print $2'})

echo "Parsing snapshot (3/3)"
BLOCK_HASH_PART2=$(docker exec miner miner snapshot info /var/data/saved-snaps/latest.gz | tail -2 | head -1 | awk {'print $1'})
BYTE_ARRAY="${BLOCK_HASH_PART1}${BLOCK_HASH_PART2}"
BASE64URL_FORMAT=$(python3 /home/snapshot/hm-block-tracker/snapshotter/base64url_encoder.py "$BYTE_ARRAY")
TMPDIR=$(mktemp -d)

mv /var/miner_data/saved-snaps/latest.gz "$TMPDIR/snap-$BLOCK_HEIGHT.gz"
echo "{\"height\": $BLOCK_HEIGHT, \"hash\": \"$BYTE_ARRAY\"}" | tee -a "$TMPDIR/latest.json"
echo "{\"height\": $BLOCK_HEIGHT, \"hash\": \"$BASE64URL_FORMAT\"}" | tee -a "$TMPDIR/latest-snap.json"

# Ensure neither snaphot 'height' nor 'hash' are empty.
echo "Verifying snapshot integrity"
ARE_SNAPSHOTS_VALID=1
for file in $TMPDIR/{latest.json,latest-snap.json}; do
    SANITY_CHECK=$(jq '.[] | select(. == null or . == "")' < "$file")
    if [ -n "$SANITY_CHECK" ]; then
        echo "'hash' or 'height' returned empty in $file. Will not upload snapshots."
        ARE_SNAPSHOTS_VALID=0
    fi
done

# Only upload snapshots if they are all valid.
if [ "$ARE_SNAPSHOTS_VALID" -eq "1" ]; then
    echo "Copying snapshot to GCS"
    gsutil cp "$TMPDIR/snap-$BLOCK_HEIGHT.gz" "gs://$SNAPSHOT_BUCKET/snap-$BLOCK_HEIGHT.gz"
    gsutil cp "$TMPDIR/latest.json" "gs://$SNAPSHOT_BUCKET/latest.json"
    gsutil cp "$TMPDIR/latest-snap.json" "gs://$SNAPSHOT_BUCKET/latest-snap.json"
fi

echo "Removing TMPDIR and docker.config. Finished."
rm -rf "$TMPDIR" docker.config
