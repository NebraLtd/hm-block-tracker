# Helium Block Tracker

This repository contains the tools required for achieving very quick syncing of Helium Miners (typically called "instant sync" by many vendors).

This is facilitated using the following steps:
* use our snapshotter tool ([more info in the README](./snapshotter/README.md)) on GCP to generate miner snapshots every 4 hours (approx 240 blocks) along with a [JSON file](https://helium-snapshots.nebra.com/latest.json) containing information on the snapshot height and snapshot hash for the latest generated snapshot
* periodically (hourly) generate the [config file](https://helium-assets.nebra.com/docker.config) for the Helium miner with a blessed block following that of the latest snapshot mentioned above

These files (config and snapshot) are stored on GCP and cached by Cloudflare for quick and reliable retrieval by hotspots worldwide.

Our miner container (see [hm-miner](https://github.com/NebraLtd/hm-miner)) pulls in the most up to date config file for the miner every time the container starts as you can see [here](https://github.com/NebraLtd/hm-miner/blob/70dbc27b98c233e969001f8e3bb91371a3ef7bdb/start-miner.sh#L7-L9). This means that if a hotspot is being turned on for the first time it will automatically pull in a config and snapshot that are, at most, 240 blocks behind the current block. Additionally, if a hotspot miner has been turned off for some time it will automatically pull in the latest config and snapshot the next time it is turned on. Lastly, if your miner falls behind sync by more than ~240 blocks for whatever reason, you can manually trigger it to pull down the latest config file and snapshot using either the "Restart" or "Reboot" buttons on the individual device page of the [Nebra Dashboard](https://dashboard.nebra.com). Sync times will therefore be very fast.

In the future we plan to introduce a [watchdog container](https://github.com/NebraLtd/hm-watchdog) to our software which will periodically check the sync status of the miner and automatically pull down the latest config and snapshot if the miner sync gets behind by more than ~240 blocks, without any manual intervention.

## Other Vendors / DIY

For other manufacturers / DIY owners that wish to introduce an "instant sync" feature - you are more than welcome to use our snapshots for this purpose free of charge. We will publish some documentation on this shortly, but basically we have:

* sys.config file - https://helium-assets.nebra.com/docker.config (you may need to customise some parts of this for your device)
* latest snapshot info - https://helium-snapshots.nebra.com/latest.json
* snapshot itself - https://helium-snapshots.nebra.com/snap-1035148 (you can pull the snap-\<height\> parameter from the latest.json above)
* helium-miner-software (full nebra stack) - https://github.com/NebraLtd/helium-miner-software

## Notes

When updating the config.template and txt files in tests/fixtures make sure to remove any new line characters from the end of the file, or the python unit tests will fail.

## References

This repository deprecates the following repositories:
* https://github.com/NebraLtd/snapshot-bumper
* https://github.com/NebraLtd/vps-scripts
