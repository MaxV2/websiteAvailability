# Website availability & performance monitoring
Coding assignment.

## How to launch the console program

1. Install the libraries if needed (os, time, requests, numpy, collections)
1. Run the programm from your console

## How to use the program
To deploy FirebaseUI to Bintray

  1. Set `BINTRAY_USER` and `BINTRAY_KEY` in your environment. You must be a member of the firebaseui Bintray organization.
  1. Run `./gradlew clean :library:prepareArtifacts :library:bintrayUploadAll`
  1. Go to the Bintray dashboard and click 'Publish'.
    1. In Bintray click the 'Maven Central' tab and publish the release.
