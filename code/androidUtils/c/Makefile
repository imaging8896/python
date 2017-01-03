USER_DIR = .

SYSROOT=$(ANDROID_NDK)/platforms/android-21/arch-arm64/
CC=$(ANDROID_NDK)/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/bin/aarch64-linux-android-gcc
CFLAGS=--sysroot=$(SYSROOT) -fPIE -pie -ldl -std=gnu99  -I $(USER_DIR)/include

all : alias

UTILS_HEADERS = $(wildcard $(USER_DIR)/include/*.h) \
			$(wildcard $(USER_DIR)/include/*/*.h)
UTILS_SRCS = $(wildcard $(USER_DIR)/utils/*.c) \
			$(wildcard $(USER_DIR)/utils/*/*.c)
UTILS_OBJS = $(subst command/,, \
				$(subst $(USER_DIR)/utils/,, \
					$(subst .c,.o, $(UTILS_SRCS))))

$(UTILS_OBJS): $(UTILS_SRCS) $(UTILS_HEADERS)
	$(CC) $(CFLAGS) -pthread -c -g $(UTILS_SRCS)

filegen: filegen.c $(UTILS_HEADERS) $(UTILS_OBJS)
	$(CC) $(CFLAGS) -Wall -lm  $^ -o $@

clean:
	rm -f filegen *.o
