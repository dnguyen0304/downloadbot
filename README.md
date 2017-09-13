# Room List Watcher
A Pokemon Showdown web scraper.

## Getting Started
### Building
```
sudo ./build.sh
```

### Running
Update the configuration files in the `configuration` directory first.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker run \
    --rm \
    --volume $(pwd)/configuration:/etc/opt/roomlistwatcher \
    --volume $(pwd):/var/opt/roomlistwatcher/log \
    dnguyen0304/roomlistwatcher:<tag>
```

### Pushing
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/roomlistwatcher-buildtime:<tag>
sudo docker push dnguyen0304/roomlistwatcher:<tag>
```

### Pulling
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/roomlistwatcher:<tag>
```

## Advanced
### Deploying the application.
1. Install `docker`.
2. Install `git`.
3. Clone the repository.
```
git clone https://github.com/dnguyen0304/room-list-watcher.git
```
4. Change the working directory.
```
cd room-list-watcher
```
5. Build the application. See the notes on _Building_ in the _Getting Started_ section.
6. Update the configuration files.
7. Run the application. See the notes on _Running_ in the _Getting Started_ section.

### Managing the base buildtime image.
1. Change the working directory to the package root directory.
2. Build the image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker build \
    --file docker/buildtime/base/Dockerfile \
    --tag dnguyen0304/roomlistwatcher-buildtime-base:<tag> \
    --build-arg SHARED_VOLUME="/tmp/build" \
    .
```
3. Push the image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/roomlistwatcher-buildtime-base:<tag>
```

### Managing the runtime image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker build \
    --file docker/runtime/Dockerfile \
    --tag dnguyen0304/roomlistwatcher-runtime:<tag> \
    --build-arg NAMESPACE=roomlistwatcher \
    --build-arg CONFIGURATION_FILE_NAME="application.config" \
    --build-arg AWS_CONFIGURATION_FILE_NAME="aws.config" \
    --build-arg AWS_CREDENTIALS_FILE_NAME="aws.credentials" \
    .

sudo docker push dnguyen0304/roomlistwatcher-runtime:<tag>
```
