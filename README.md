# Download Bot
A Pokemon Showdown web scraper.

## Advanced
### Testing the application.
1. Build the image.
```
sudo ./build.sh test
```
2. Update the configuration files in the `configuration` directory.
3. Run the test suite.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker run \
    --rm \
    --volume $(pwd)/configuration:/etc/opt/downloadbot \
    --volume $(pwd):/var/opt/downloadbot/log \
    dnguyen0304/downloadbot-runtime:<tag>
```

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
sudo ./scripts/build-runtime-base.sh
```
3. Push the image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/downloadbot-runtime-base:<tag>
```
