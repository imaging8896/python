FROM ubuntu:14.04

ENV ANDROID_NDK /opt/android-ndk-r13b

RUN apt-get update
RUN apt-get install -y wget zip unzip make

RUN mkdir /opt/android-ndk-tmp
RUN cd /opt/android-ndk-tmp && wget -q https://dl.google.com/android/repository/android-ndk-r13b-linux-x86_64.zip
RUN cd /opt/android-ndk-tmp && unzip -q android-ndk-r13b-linux-x86_64.zip
RUN cd /opt/android-ndk-tmp && mv ./android-ndk-r13b ${ANDROID_NDK}
RUN rm -rf /opt/android-ndk-tmp

ENV PATH ${PATH}:${ANDROID_NDK}

RUN apt-get install -y python2.7
RUN ln /usr/bin/python2.7 /usr/bin/python

# ------------------------------------------------------
# --- Cleanup

# Cleaning
RUN apt-get clean
