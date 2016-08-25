CC = gcc
CPPFLAGS =
CFLAGS = -g -pthread -Wall -Wextra
LFLAGS = -lsqlite3 -ljansson -lcrypto

# [Autodependencies with GNU make]
# http://scottmcpeak.com/autodepend/autodepend.html

OBJS_DIR = obj/

hcfsapid_OBJS = $(addprefix $(OBJS_DIR), \
		   socket_serv.o pin_ops.o hcfs_stat.o hcfs_sys.o enc.o socket_util.o logger.o)

test_OBJS = $(addprefix $(OBJS_DIR), \
	    test.o HCFS_api.o)

hcfsconf_OBJS = $(addprefix $(OBJS_DIR), \
	    hcfsconf.o enc.o logger.o)

OBJS := $(hcfsapid_OBJS) $(test_OBJS)

hcfsapid: $(hcfsapid_OBJS)
	$(CC) $(CPPFLAGS) $(CFLAGS) -g $(hcfsapid_OBJS) -o $@ $(LFLAGS)

test: $(test_OBJS)
	$(CC) $(CPPFLAGS) $(CFLAGS) -g $(test_OBJS) -o $@ $(LFLAGS)

hcfsconf: $(hcfsconf_OBJS)
	$(CC) $(CPPFLAGS) $(CFLAGS) -g $(hcfsconf_OBJS) -o $@ $(LFLAGS)

publish: doc
	sudo cp -r doc /mnt/nas/CloudDataSolution/Gateway_2.0/

doc: HCFS_api.c HCFS_api.h
	cldoc generate -c -- --basedir . --type html --merge docs --output doc HCFS_api.h

clean:
	rm -rf $(OBJS_DIR) $(OBJS_DIR) hcfsapid test hcfsconf

# pull in dependency info for *existing* .o files
-include $(OBJS:.o=.d)

# compile and generate dependency info
$(OBJS_DIR)%.o: %.c | $(OBJS_DIR)
	$(CC) -c $(CPPFLAGS) $(CFLAGS) $*.c -o $(OBJS_DIR)$*.o
	@$(CC) -MM $(CPPFLAGS) $(CFLAGS) $*.c > $(OBJS_DIR)$*.d
	@sed -i"" -r -e ':a;$$!N;$$!ba;s# \\\n##g' -e 'p;s/\\ //g' -e 's/.*: //' -e '$$s/ |$$/:\n/g' $(OBJS_DIR)$*.d

$(OBJS_DIR):
	mkdir $@
