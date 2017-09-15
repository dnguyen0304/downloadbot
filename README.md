# Download Bot
A Pokemon Showdown web scraper.

## Advanced
### Managing the base buildtime image.
1. Change the working directory to the package root directory.
2. Build the image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker build \
    --file docker/buildtime/base/Dockerfile \
    --tag dnguyen0304/downloadbot-buildtime-base:<tag> \
    --build-arg SHARED_VOLUME="/tmp/build" \
    .
```
3. Push the image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/downloadbot-buildtime-base:<tag>
```
