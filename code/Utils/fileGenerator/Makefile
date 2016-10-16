SYSROOT=$(ANDROID_NDK)/platforms/android-21/arch-arm64/
CC=$(ANDROID_NDK)/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/bin/aarch64-linux-android-gcc
 
CFLAGS=--sysroot=$(SYSROOT) -fPIE -pie -Wall

all: FileGen SingleFileGen

FileGen: FileGenerator.c
	$(CC) $(CFLAGS) -pthread -o FileGen FileGenerator.c

SingleFileGen: SingleFileGenerator.c
	$(CC) $(CFLAGS)  -o SingleFileGen SingleFileGenerator.c


clean:
	rm FileGen
	rm SingleFileGen
