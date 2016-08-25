/*************************************************************************
*
* Copyright © 2016 Hope Bay Technologies, Inc. All rights reserved.
*
* File Name: enc.h
* Abstract: This c header file for some encryption helpers.
*
* Revision History
* 2016/5/27 Modified after first code review.
*
**************************************************************************/

#ifndef GW20_HCFSAPI_ENC_H_
#define GW20_HCFSAPI_ENC_H_

#include <string.h>
#include <inttypes.h>
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/err.h>
#ifdef OPENSSL_IS_BORINGSSL
#include <openssl/mem.h>
#endif

#define IV_SIZE 12
#define TAG_SIZE 16
#define KEY_SIZE 32


int32_t generate_random_aes_key(uint8_t *);

int32_t generate_random_bytes(uint8_t *, uint32_t);

int32_t aes_gcm_encrypt_core(uint8_t *, uint8_t *, uint32_t,
			 uint8_t *, uint8_t *);

int32_t aes_gcm_decrypt_core(uint8_t *, uint8_t *, uint32_t,
			 uint8_t *, uint8_t *);

uint8_t *get_key(char *);

#endif  /* GW20_HCFSAPI_ENC_H_ */
