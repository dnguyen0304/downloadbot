# Download Bot
A Pokemon Showdown web scraper.

## Advanced
### Managing the base buildtime image.
1. Change the working directory to the package root directory.
2. Build the image.
```
sudo ./scripts/build-buildtime-base.sh
```
3. Push the image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/downloadbot-buildtime-base:<tag>
```

### Managing the base runtime image.
1. Change the working directory to the package root directory.
2. Build the image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker build \
    --file docker/runtime/base/Dockerfile \
    --tag dnguyen0304/downloadbot-runtime-base:<tag> \
    --build-arg NAMESPACE="downloadbot" \
    .
```
3. Push the image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/downloadbot-runtime-base:<tag>
```
