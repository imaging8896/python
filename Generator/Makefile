SYSROOT=$(ANDROID_NDK)/platforms/android-21/arch-arm64/
CC=$(ANDROID_NDK)/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/bin/aarch64-linux-android-gcc
 
CFLAGS=--sysroot=$(SYSROOT) -fPIE -pie -pthread
FGen: FileGenerator.c
	$(CC) $(CFLAGS) -Wall -o FGen FileGenerator.c

clean:
	rm FGen
