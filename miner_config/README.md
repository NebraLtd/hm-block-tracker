# Miner snapshot generator

#### Set up helium-assets buckets

```
$ gsutil mb \
    -p nebra-production \
    -c standard \
    -l us \
    gs://{helium-assets,helium-assets-stage}.nebracdn.com

$ gsutil iam ch allUsers:objectViewer \
    gs://{helium-assets,helium-assets-stage}.nebracdn.com

$ gsutil iam ch \
    serviceAccount:gh-actions-production-images@nebra-production.iam.gserviceaccount.com:objectCreator \
    gs://{helium-assets,helium-assets-stage}.nebracdn.com

$ gsutil iam ch \
    serviceAccount:githubactions-copytobucket@nebra-production.iam.gserviceaccount.com:admin \
    gs://{helium-assets,helium-assets-stage}.nebracdn.com
```

