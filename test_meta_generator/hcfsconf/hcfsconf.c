/*************************************************************************
*
* Copyright © 2016 Hope Bay Technologies, Inc. All rights reserved.
*
* File Name: hcfsconf.c
* Abstract: This c source file for hcfsconf binary.
*
* Revision History
* 2016/5/27 Modified after first code review.
*
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <inttypes.h>

#include "global.h"
#include "hcfs_sys.h"
#include "enc.h"

void usage()
{

	printf("***Usage - hcfsconf <enc|dec> <source_path> <config_path>***\n");
	printf("***Usage - hcfsconf <enc> <source_path> <config_path>***\n");
}

int32_t _check_file_existed(char *pathname)
{

	if (access(pathname, F_OK) == -1)
		return -1;
	else
		return 0;
}

int32_t __enc_config(uint8_t *output, uint8_t *input,
		 int64_t input_len)
{

	int32_t ret;
	uint8_t iv[IV_SIZE] = {0};
	uint8_t *enc_key;
	uint8_t *enc_data = NULL;

	/* Key and iv */
	enc_key = get_key(PASSPHRASE);
	generate_random_bytes(iv, IV_SIZE);

	enc_data =
		(uint8_t*)malloc(sizeof(uint8_t) * (input_len + TAG_SIZE));
	if (enc_data == NULL)
		return -1;

	ret = aes_gcm_encrypt_core(enc_data, input, input_len, enc_key, iv);
	if (ret != 0) {
	        free(enc_data);
	        return -1;
	}

	memcpy(output, iv, IV_SIZE);
	memcpy(output + IV_SIZE, enc_data, input_len + TAG_SIZE);

	free(enc_data);
	return 0;
}

int32_t _enc_config(char *source_path, char *out_path)
{

	char buf[300];
	uint8_t data_buf[1024];
	int32_t data_size = 0;
	int32_t enc_data_size = 0;
	int32_t str_len, ret_size;
	FILE *config = NULL;
	FILE *enc_config = NULL;

	config = fopen(source_path, "r");
	if (config == NULL)
		return errno;

	while (fgets(buf, sizeof(buf), config) != NULL) {
	        str_len = strlen(buf);
	        memcpy(&(data_buf[data_size]), buf, str_len + 1);
	        data_size += str_len;
	}
	fclose(config);

	enc_data_size = data_size + IV_SIZE + TAG_SIZE;
	uint8_t enc_data[enc_data_size];
	if (__enc_config(enc_data, data_buf, data_size) != 0)
		return errno;

	enc_config = fopen(out_path, "w");
	if (enc_config == NULL)
		return errno;

	ret_size = fwrite(enc_data, sizeof(uint8_t),
			  enc_data_size, enc_config);
	if ((ssize_t)ret_size < (ssize_t)enc_data_size) {
		fclose(enc_config);
		return EIO;
	}

	fclose(enc_config);
	return 0;
}

int32_t enc_config(char *source_path, char *out_path)
{

	if (_check_file_existed(source_path) == -1)
		return ENOENT;

	if (_check_file_existed(out_path) == 0)
		return EEXIST;

	return _enc_config(source_path, out_path);
}

int32_t _dec_config(char *source_path, char *out_path)
{

	int32_t ret_code = 0;
	int32_t ret_size = 0;
        int64_t file_size, enc_size, data_size;
        FILE *config = NULL;
        FILE *dec_config = NULL;
        uint8_t *iv_buf = NULL;
        uint8_t *enc_buf = NULL;
        uint8_t *data_buf = NULL;
        uint8_t *enc_key;


        config = fopen(source_path, "r");
        if (config == NULL)
                goto error;

        fseek(config, 0, SEEK_END);
        file_size = ftell(config);
        rewind(config);

        enc_size = file_size - IV_SIZE;
        data_size = enc_size - TAG_SIZE;

        iv_buf = (uint8_t*)malloc(sizeof(char)*IV_SIZE);
        enc_buf = (uint8_t*)malloc(sizeof(char)*(enc_size));
        data_buf = (uint8_t*)malloc(sizeof(char)*(data_size));

        if (!iv_buf || !enc_buf || !data_buf)
                goto error;

        enc_key = get_key(PASSPHRASE);
        fread(iv_buf, sizeof(uint8_t), IV_SIZE, config);
        fread(enc_buf, sizeof(uint8_t), enc_size, config);

        if (aes_gcm_decrypt_core(data_buf, enc_buf, enc_size,
                                 enc_key, iv_buf) != 0) {
		ret_code = EIO;
		goto end;
	}

        dec_config = fopen(out_path, "w");
        if (dec_config == NULL)
                goto error;

        ret_size = fwrite(data_buf, sizeof(uint8_t), data_size,
			  dec_config);
	if ((ssize_t)ret_size < (ssize_t)data_size) {
		ret_code = EIO;
		goto end;
	}


	goto end;

error:
	ret_code = errno;

end:
	if (config)
		fclose(config);
	if (dec_config)
		fclose(dec_config);
	if (data_buf)
		free(data_buf);
	if (enc_buf)
		free(enc_buf);
	if (iv_buf)
		free(iv_buf);

        return ret_code;
}

int32_t dec_config(char *source_path, char *out_path)
{

	if (_check_file_existed(source_path) == -1)
		return ENOENT;

	if (_check_file_existed(out_path) == 0)
		return EEXIST;

	return _dec_config(source_path, out_path);
}

typedef struct {
	const char *name;
	int32_t (*cmd_fn)(char *source_path, char *out_path);
} CMD_INFO;

CMD_INFO cmds[] = {
	{"enc", enc_config},
	{"dec", dec_config},
};

int32_t main(int32_t argc, char **argv)
{

	int32_t ret_code = 0;
	uint32_t i;

	if (argc != 4) {
		printf("Error - Invalid args\n");
		usage();
		return EINVAL;
	}

	for (i = 0; i < sizeof(cmds) / sizeof(cmds[0]); i++) {
		if (strcmp(cmds[i].name, argv[1]) == 0) {
			ret_code = cmds[i].cmd_fn(argv[2], argv[3]);
			goto done;
		}
	}
	printf("Action %s not supported\n", argv[1]);
	usage();
	return EINVAL;

done:
	if (ret_code != 0) {
		printf("Failed to %s config with path %s\n", argv[1], argv[2]);
		usage();
		return ret_code;
	}

	return 0;
}
