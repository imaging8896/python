SYSROOT=$(ANDROID_NDK)/platforms/android-21/arch-arm64/
CC=$(ANDROID_NDK)/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/bin/aarch64-linux-android-gcc
 
CFLAGS=--sysroot=$(SYSROOT) -fPIE -pie  -ldl
adapter: API_adapter.c libHCFS_api.so 
	$(CC) $(CFLAGS) -LlibHCFS_api.so -Wall -o adapter API_adapter.c

clean:
	rm adapter
