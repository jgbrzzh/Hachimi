#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cstdio>

//openssl
#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/rand.h>
#include <openssl/err.h>

//ha 0  ¹þ
//ji 1	»ù
//mi 01	ßä

using namespace std;

int aesEncode(char* _pPassword, char* _pInput, int _InLen, char* _pOutBuf, int* _pOutLen);
int aesDecode(char* _pPassword, char* _pInput, int _InLen, char* _pOutBuf, int* _pOutLen);

string FileName;
string EncodeOutFile("../temp/encode.txt");
string DeEncodeOutFile("../temp/decode.bin");

class hachimi {
private:
	std::vector<unsigned char> msg;
	ifstream binContent;
	string  InFileName;
	
public:
	int readBin();
	int map();
	int remap();

public:
	hachimi(string inFile);
	std::string process();
};

int main(int argc, char* argv[])
{
	int codeFlag = 1;//0:encode 1:decode
#if false
	switch (argc)
	{
	case 1:
		cout << "name.exe [encode/decode] filepath" << endl;
		return 1;
		break;
	case 2://0 filepath   default:encode
		FileName = string(argv[1]);
		break;
	case 3://0 <encode/decode> filepath
		FileName = string(argv[2]);
		if (argv[1] == "encode")
		{
			codeFlag = 0;
		}
		else if (argv[2] == "decode")
		{
			codeFlag = 1;
		}
		break;
	default:
		break;
	}
#endif

	FileName = EncodeOutFile;

	hachimi ha(FileName);
	if (codeFlag == 0)//encode
	{
		ha.map();
	}
	else {
		ha.remap();//decode
	}

	system("pause");
	return 0;
}

hachimi::hachimi(string inFile)
	:InFileName(inFile)
{
	binContent.open(InFileName, ios::in);
	readBin();
	binContent.close();
}

int hachimi::readBin()
{
	char tmp;
	while (true)
	{
		if (binContent.eof()){
			break;
		}
		binContent >> tmp;
		msg.push_back(tmp);
	}
	return 0;
}

int hachimi::map() 
{
	if (msg.empty())
	{
		std::cerr << "empty content" << std::endl;
		return 1;
	}
	
	ofstream output;
	output.open(EncodeOutFile,ios::out | ios::trunc);
	if (!output.is_open()) {
		cout << "file£º" << EncodeOutFile << " cant open" << endl;
	}

	char lastNum = -1;//indicate last number
	for (int j = 0;j < msg.size() - 1;j++)
	{
		unsigned char a = msg[j];
		unsigned char tmp = 0;
		lastNum = -1;
		for (int i = 0;i < 8;i++)
		{
			tmp = a;
			tmp <<= i;
			tmp >>= 7;
			if (tmp == 1) {
				if (lastNum == 1 || lastNum == -1)
				{
					output << "»ù";
				}
				if (lastNum == 0)
				{
					output << "ßä";
				}
				lastNum = 1;
			}
			else{
				if (lastNum == 0)
				{
					output << "¹þ";
				}
				if(i==7)
				{
					output << "¹þ";
				}
				lastNum = 0;
			}
		} 
	}
	output.close();
	return 0;
}

int hachimi::remap()
{
	vector<unsigned char>text = msg;

	ofstream out1;
	out1.open(DeEncodeOutFile, ios::out | ios::trunc | ios::binary);
	if (!out1.is_open()) {
		cout << "file£º" << DeEncodeOutFile << " cant open" << endl;
	}

	string word;
	unsigned char tt = 0, ttNum = 0;
	for (int i = 0;i < text.size()-1;i += 2)
	{
		word.clear();
		word += text[i];
		word += text[i+1];
		if (word == (string)"¹þ")
		{
			cout << '0';
			tt <<= 1;
			ttNum++;
		}
		if (word == (string)"»ù")
		{
			cout << '1';
			tt <<= 1;
			tt++;
			ttNum++;
		}
		if (word == (string)"ßä")
		{
			cout << '0' << '1';
			tt <<= 2;
			tt++;
			ttNum++;
			ttNum++;
		}
		if (ttNum == 8)
		{
			ttNum = 0;
			out1 << tt;
			tt = 0;
		}
	}
	out1.close();
	return 0;
}

int aesEncode(char* _pPassword, char* _pInput, int _InLen, char* _pOutBuf, int* _pOutLen)
{
	EVP_CIPHER_CTX* pEn_ctx = NULL;

	int ret = -1;
	int flen = 0, outlen = 0;
	int i, nrounds = 1;

	unsigned char key[32] = { 0 };
	unsigned char iv[32] = { 0 };

	if (!_pPassword || !_pInput || !_pOutBuf || !_pOutLen) {
		return ret;
	}

	const EVP_CIPHER* cipherType = EVP_aes_256_cbc();
	if (cipherType == NULL) {
		goto clean;
	}

	i = EVP_BytesToKey(cipherType, EVP_md5(), NULL, (unsigned char*)_pPassword, strlen(_pPassword), nrounds, key, iv);
	if (i != 32) {
		printf("Key size is %d bits - should be 256 bits\n", i);
		goto clean;
	}

	pEn_ctx = EVP_CIPHER_CTX_new();
	EVP_CIPHER_CTX_init(pEn_ctx);
	EVP_EncryptInit_ex(pEn_ctx, cipherType, NULL, key, iv);

	if (!EVP_EncryptUpdate(pEn_ctx, (unsigned char*)_pOutBuf, &outlen, (unsigned char*)_pInput, _InLen)) {
		perror("\n Error,ENCRYPR_UPDATE:");
		goto clean;
	}

	if (!EVP_EncryptFinal_ex(pEn_ctx, (unsigned char*)(_pOutBuf + outlen), &flen)) {
		perror("\n Error,ENCRYPT_FINAL:");
		goto clean;
	}

	*_pOutLen = outlen + flen;
	ret = 0;

clean:
	if (pEn_ctx) {
		EVP_CIPHER_CTX_cleanup(pEn_ctx);
	}
	if (pEn_ctx) {
		EVP_CIPHER_CTX_free(pEn_ctx);
	}

	return ret;
}


int aesDecode(char* _pPassword, char* _pInput, int _InLen, char* _pOutBuf, int* _pOutLen)
{
	EVP_CIPHER_CTX* pDe_ctx = NULL;

	int ret = -1;
	int flen = 0, outlen = 0;
	int i, nrounds = 1;

	unsigned char key[32] = { 0 };
	unsigned char iv[32] = { 0 };

	if (!_pPassword || !_pInput || !_pOutBuf || !_pOutLen) {
		return ret;
	}

	const EVP_CIPHER* cipherType = EVP_aes_256_cbc();
	if (cipherType == NULL) {
		goto clean;
	}

	i = EVP_BytesToKey(cipherType, EVP_md5(), NULL, (unsigned char*)_pPassword, strlen(_pPassword), nrounds, key, iv);
	if (i != 32) {
		printf("Key size is %d bits - should be 256 bits\n", i);
		goto clean;
	}

	pDe_ctx = EVP_CIPHER_CTX_new();
	EVP_CIPHER_CTX_init(pDe_ctx);
	EVP_DecryptInit_ex(pDe_ctx, cipherType, NULL, key, iv);

	if (!EVP_DecryptUpdate(pDe_ctx, (unsigned char*)_pOutBuf, &outlen, (unsigned char*)_pInput, _InLen)) {
		perror("\n Error,ENCRYPR_UPDATE:");
		goto clean;
	}

	if (!EVP_DecryptFinal_ex(pDe_ctx, (unsigned char*)(_pOutBuf + outlen), &flen)) {
		perror("\n Error,ENCRYPT_FINAL:");
		goto clean;
	}

	*_pOutLen = outlen + flen;
	ret = 0;

clean:
	if (pDe_ctx) {
		EVP_CIPHER_CTX_cleanup(pDe_ctx);
	}
	if (pDe_ctx) {
		EVP_CIPHER_CTX_free(pDe_ctx);
	}

	return ret;
}