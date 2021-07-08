# Helium Block Tracker

This repository aims to serve two purposes:
- Periodically generate config files for the Helium miner with a blessed block following that of the upstream blessed block - https://github.com/helium/miner/blob/master/config/sys.config#L42-L44
- In the  future generate snapshots based off of the current blockchain head and ship to an S3 compatible object store for quick hotspot sync from snapshot using the s3_base_url feature of the Helium Miner.

This repository deprecates the following repositories:
- https://github.com/NebraLtd/snapshot-bumper
- https://github.com/NebraLtd/vps-scripts
