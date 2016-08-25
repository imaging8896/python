/*************************************************************************
*
* Copyright © 2016 Hope Bay Technologies, Inc. All rights reserved.
*
* File Name: enc.c
* Abstract: This c source file for some encryption helper.
*
* Revision History
* 2016/5/27 Modified after first code review.
*
**************************************************************************/

#include "enc.h"

#include <inttypes.h>

#include "logger.h"

/************************************************************************
 * *
 * * Function name: generate_random_bytes
 * *        Inputs: uint8_t* bytes: points to a buffer which
 *		    length should equals length
 *		    uint32_t length
 * *       Summary: generate some random bytes
 * *
 * *
 * *  Return value: 0 if successful.
 *                  -1 if length <= 0.
 *                  -2 if openssl RAND not supported
 *                  -3 if some openssl error occurs, use ERR_get_error to get
 *                  error code
 * *
 * *************************************************************************/
int32_t generate_random_bytes(uint8_t *bytes, uint32_t length)
{
	if (length <= 0)
		return -1;

	memset(bytes, 0, length);
	int32_t rand_success = RAND_bytes(bytes, length);
	/* RAND_bytes() returns 1 on success, 0 otherwise. The error code can
	 * be obtained by ERR_get_error.
	 * return -1 if not supported by the current RAND method.
	 * https://wiki.openssl.org/index.php/Manual:RAND_bytes%283%29
	 */
	switch (rand_success) {
	case 1:
		return 0;
	case -1:
		write_log(0, "In %s, RAND_bytes not supported", __func__);
		return -2;
	default:
		write_log("In %s, RAND_bytes: some openssl error may occurs: %ld",
			  __func__, ERR_peek_last_error());
		return -3;
	}
}

/************************************************************************
 * *
 * * Function name: generate_random_aes_key
 * *        Inputs: uint8_t* key: points to a buffer which
 *		    length should equals KEY_SIZE
 * *       Summary: generate a random key for encryption
 * *
 * *  Return value: See get_random_bytes
 * *
 * *************************************************************************/
int32_t generate_random_aes_key(uint8_t *key)
{
	return generate_random_bytes(key, KEY_SIZE);
}

/************************************************************************
 * *
 * * Function name: aes_gcm_encrypt_core
 * *        Inputs: uint8_t* output: points to a buffer which
 *		                           length should equals
 *		                           input_length + TAG_SIZE
 *		    uint8_t* input
 *		    uint32_t input_length
 *		    uint8_t* key: must be KEY_SIZE length
 *		    uint8_t* iv: must be IV_SIZE length
 * *       Summary: Use aes gcm mode to encrypt input
 * *
 * *  Return value: 0 if successful.
 *                  1 if Encrypt Update error
 *                  2 if Encrypt Final error
 *                  3 if extract TAG error
 * *
 * *************************************************************************/
int32_t aes_gcm_encrypt_core(uint8_t *output, uint8_t *input,
			 uint32_t input_length, uint8_t *key,
			 uint8_t *iv)
{
	int32_t tmp_length = 0;
	int32_t output_length = 0;
	int32_t retcode = 0;
	const int32_t output_preserve_size = TAG_SIZE;
	uint8_t tag[TAG_SIZE] = {0};
	/* clear output */
	memset(output, 0, input_length + TAG_SIZE);
	EVP_CIPHER_CTX ctx;

	EVP_CIPHER_CTX_init(&ctx);
	EVP_EncryptInit_ex(&ctx, EVP_aes_256_gcm(), NULL, key, iv);
	if (!EVP_EncryptUpdate(&ctx, output + output_preserve_size, &tmp_length,
			       input, input_length)) {
		retcode = 1;
		goto final;
	}
	if (!EVP_EncryptFinal_ex(&ctx, output + output_preserve_size + tmp_length,
			      &output_length)) {
		retcode = 2;
		goto final;
	}
	if (!EVP_CIPHER_CTX_ctrl(&ctx, EVP_CTRL_GCM_GET_TAG, TAG_SIZE, tag)) {
		retcode = 3;
		goto final;
	}
	memcpy(output, tag, TAG_SIZE);
	memset(tag, 0, TAG_SIZE);
final:
	EVP_CIPHER_CTX_cleanup(&ctx);
	return retcode;
}

/************************************************************************
 * *
 * * Function name: aes_gcm_decrypt_core
 * *        Inputs: uint8_t* output:  points to a buffer which
 *		    length should equals input_length - TAG_SIZE
 *		    uint8_t* input
 *		    uint32_t input_length
 *		    uint8_t* key: must KEY_SIZE length
 *		    uint8_t* iv: must IV_SIZE length
 * *       Summary: Use aes gcm mode to decrypt input
 * *
 * *  Return value: 0 if successful.
 *                  3 if set reference TAG error
 *                  1 if Decrypt update error
 *                  2 if Decrypr final error (TAG wrong)
 * *
 * *************************************************************************/
int32_t aes_gcm_decrypt_core(uint8_t *output, uint8_t *input,
			 uint32_t input_length, uint8_t *key,
			 uint8_t *iv)
{
	int32_t tmp_length = 0;
	int32_t output_length = 0;
	int32_t retcode = 0;
	uint8_t tag[TAG_SIZE] = {0};
	const int32_t preserve_size = TAG_SIZE;

	/* clear output */
	memset(output, 0, input_length - TAG_SIZE);

	EVP_CIPHER_CTX ctx;

	EVP_CIPHER_CTX_init(&ctx);
	EVP_DecryptInit_ex(&ctx, EVP_aes_256_gcm(), NULL, key, iv);
	if (!EVP_CIPHER_CTX_ctrl(&ctx, EVP_CTRL_GCM_SET_TAG, TAG_SIZE, input)) {
		retcode = 3;
		goto decrypt_final;
	}
	if (!EVP_DecryptUpdate(&ctx, output, &tmp_length, input + preserve_size,
			       input_length - TAG_SIZE)) {
		retcode = 1;
		goto decrypt_final;
	}
	if (!EVP_DecryptFinal_ex(&ctx, tag, &output_length)) {
		retcode = 2;
		goto decrypt_final;
	}
decrypt_final:
	EVP_CIPHER_CTX_cleanup(&ctx);
	return retcode;
}

/*
 * This function only for developing "upload to cloud".
 * In the future, it should be reimplemented considering
 * key management specs
 */
uint8_t *get_key(char *keywords)
{
	const char *user_pass = keywords;
	uint8_t md_value[EVP_MAX_MD_SIZE];
	uint32_t md_len;
	uint8_t *ret =
	    (uint8_t *)calloc(KEY_SIZE, sizeof(uint8_t));
	if (!ret)
		return NULL;
	const EVP_MD *m;
	EVP_MD_CTX ctx;

	m = EVP_sha256();

	if (!m)
		return NULL;
	EVP_DigestInit(&ctx, m);
	uint8_t *salt = (uint8_t *)"oluik.354jhmnk,";

	PKCS5_PBKDF2_HMAC(user_pass, strlen(user_pass), salt,
			  strlen((char *)salt), 3, m, KEY_SIZE, ret);
	EVP_DigestFinal(&ctx, md_value, &md_len);
	return ret;
}
