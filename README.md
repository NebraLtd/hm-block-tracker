# Helium Block Tracker

This repository contains the tools required for achieving very quick syncing of Helium Miners (typically called "instant sync" by many vendors).

This is facilitated using the following steps:
* Use our snapshotter tool ([more info in the README](./snapshotter/README.md)) on GCP to generate miner snapshots every 4 hours (approx 240 blocks) along with a [JSON file](https://helium-snapshots.nebra.com/latest.json) containing information on the snapshot height and snapshot hash for the latest generated snapshot
* Periodically (hourly) generate the `docker.config` for the Helium miner with a blessed block following that of the latest snapshot mentioned above

These files (config and snapshot) are stored on GCP and cached by Cloudflare for quick and reliable retrieval by hotspots worldwide.

Our miner container (see [hm-miner](https://github.com/NebraLtd/hm-miner)) pulls in the most up to date config file for the miner every time the container starts as you can see [here](https://github.com/NebraLtd/hm-miner/blob/70dbc27b98c233e969001f8e3bb91371a3ef7bdb/start-miner.sh#L7-L9). This means that if a hotspot is being turned on for the first time it will automatically pull in a config and snapshot that are, at most, 240 blocks behind the current block. Additionally, if a hotspot miner has been turned off for some time it will automatically pull in the latest config and snapshot the next time it is turned on. Lastly, if your miner falls behind sync by more than ~240 blocks for whatever reason, you can manually trigger it to pull down the latest config file and snapshot using either the "Restart" or "Reboot" buttons on the individual device page of the [Nebra Dashboard](https://dashboard.nebra.com). Sync times will therefore be very fast.

In the future we plan to introduce a [watchdog container](https://github.com/NebraLtd/hm-watchdog) to our software which will periodically check the sync status of the miner and automatically pull down the latest config and snapshot if the miner sync gets behind by more than ~240 blocks, without any manual intervention.

## Testing

After making any changes, make sure you run the unit tests:
```
$ pytest
```

With that done, then run the integration test manually (i.e. load the file in Erlang to check syntax).

```
$ python miner_config/generate_config.py
$ docker run \
    --rm -ti \
    -v $(pwd):/foobar \
    erlang:24-alpine \
    erl -config /foobar/docker
```

If the config file is valid, you'll get something like this:

```
Erlang/OTP 24 [erts-12.2.1] [source] [64-bit] [smp:6:6] [ds:6:6:10] [async-threads:1] [jit:no-native-stack]

Eshell V12.2.1  (abort with ^G)
1>
BREAK: (a)bort (A)bort with dump (c)ontinue (p)roc info (i)nfo
       (l)oaded (v)ersion (k)ill (D)b-tables (d)istribution
       ^C
```

But if the config file is broken, you'll instead get something like this:

```
{"could not start kernel pid",application_controller,"error in config file \"/foobar/test.config\" (52): syntax error before: HERE"}
could not start kernel pid (application_controller) (error in config file "/foobar/test.config" (52): syntax error before: HERE)
```

## Production vs Staging

* The master branch is mapped against the staging environment (helium-snapshots-stage.nebra.com and helium-assets-stage.nebra.com)
* The production branch is mapped against the production environment (helium-snapshots.nebra.com and helium-assets.nebra.com)

The template is then automatically built and copied in based on this.

## Variants of config file

We currently build two different configs:
- Raspberry Pi config, named docker.config and uses i2c-1 bus
- RockPi config, named docker.config.rockpi and uses i2c-7 bus

This is done by passing a ROCKPI=1 env variable to the python command in the GitHub Actions workflow when building the RockPi config.

## Other Vendors / DIY

For other manufacturers / DIY owners that wish to introduce an "instant sync" feature - you are more than welcome to use our snapshots for this purpose free of charge. We will publish some documentation on this shortly, but basically we have:

* sys.config file - https://helium-assets.nebra.com/docker.config (you may need to customise some parts of this for your device)
* latest snapshot info - https://helium-snapshots.nebra.com/latest.json
* snapshot itself - https://helium-snapshots.nebra.com/snap-1035148 (you can pull the snap-\<height\> parameter from the latest.json above)
* helium-miner-software (full nebra stack) - https://github.com/NebraLtd/helium-miner-software

## Notes

When updating the config.template and txt files in tests/fixtures make sure to remove any new line characters from the end of the file, or the python unit tests will fail. You can do this using something like `truncate -s -1 miner_config/tests/fixtures/sample_output.txt`. If on macOS you may need to first `brew install truncate`.

## References

This repository deprecates the following repositories:
* https://github.com/NebraLtd/snapshot-bumper
* https://github.com/NebraLtd/vps-scripts
