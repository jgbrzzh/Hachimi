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

//ha 0  Ήώ
//ji 1	»ω
//mi 01	ίδ

using namespace std;

int aesEncode(char* _pPassword, char* _pInput, int _InLen, char* _pOutBuf, int* _pOutLen);
int aesDecode(char* _pPassword, char* _pInput, int _InLen, char* _pOutBuf, int* _pOutLen);

string FileName;
string EncodeOutFile("../temp/encode.txt");
string DeEncodeOutFile("../temp/decode.bin");


class hachimi {
private:
	vector<unsigned char> msg;
	string outTXT;					//for map
	vector<unsigned char> outBin;	//for remap
	ifstream binContent;
	string  InFileName;
	bool _Encode;

	// aescryp
	int _aesEncode();
	int _aesDecode();
	// in/out
	int readBin();
	int write();
	// map/remap to/from hachimi
	int map();
	int remap();
	
public:
	static char pass[];
	hachimi(string inFile,bool _ifEncode);
	int encode() { _aesEncode(); map(); write(); return 0; }
	int decode() { remap(); _aesDecode(); write(); return 0; }
};

//aes password
char hachimi::pass[] = "aabbcc";

int main(int argc, char* argv[])
{
	bool ifEncode = true;//true:encode ; false:decode
	ifEncode = false;
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

	if(ifEncode)
		FileName = DeEncodeOutFile;
	else
		FileName = EncodeOutFile;

	hachimi ha(FileName, ifEncode);
	if (ifEncode){
		ha.encode();		//encode
	}
	else {
		ha.decode();		//decode
	}

	system("pause");
	return 0;
}

int hachimi::_aesEncode()
{
	unsigned char* in = new unsigned char[msg.size()];
	unsigned char* out = new unsigned char[msg.size() + 16];
	int outLen = msg.size() + 16;
	copy(msg.begin(), msg.end(), in);
	aesEncode(pass, (char*)in, msg.size(), (char*)out, &outLen);
	msg.clear();
	for (int i = 0;i < outLen;i++)
	{
		msg.push_back(out[i]);
	}
	return 0;
}

int hachimi::_aesDecode()
{
	unsigned char* in = new unsigned char[outBin.size()];
	unsigned char* out = new unsigned char[outBin.size() + 16];
	int inLen = outBin.size();
	int outLen = outBin.size() + 16;
	copy(outBin.begin(), outBin.end(), in);
	aesDecode(pass, (char*)in, inLen, (char*)out, &outLen);
	outBin.clear();
	for (int i = 0;i < outLen;i++)
	{
		outBin.push_back(out[i]);
	}
	return 0;
}

hachimi::hachimi(string inFile, bool _ifEncode)
	:InFileName(inFile), _Encode(_ifEncode)
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
		binContent >> tmp;
		if (binContent.eof()){
			break;
		}
		msg.push_back(tmp);
	}
	return 0;
}

int hachimi::write()
{
	int a = outBin.size();

	ofstream write_out;
	string _File;
	if (_Encode)
		_File = EncodeOutFile;
	else
		_File = DeEncodeOutFile;

	write_out.open(_File,ios::trunc);
	if (!write_out.is_open()) {
		cerr << "file: " << _File << " cant open" << endl;
		return -1;
	}

	if (_Encode){
		write_out << outTXT;
	}
	else{
		for (int i = 0;i < outBin.size();i++)
		{
			write_out << outBin[i];
		}
	}
	write_out.close();
	return 0;
}

int hachimi::map() 
{
	if (msg.empty()){
		std::cerr << "empty content" << std::endl;
		return -1;
	}

	char lastNum = -1;//indicate last number
	unsigned char a = 0, tmp = 0;
	for (int j = 0;j < msg.size();j++)
	{
		a = msg[j];
		cout << (int)a << " ";
		tmp = 0;
		lastNum = -1;
		for (int i = 0;i < 8;i++)
		{
			tmp = a;
			tmp <<= i;
			tmp >>= 7;
			if (tmp == 1) {
				if (lastNum == 1 || lastNum == -1)
				{
					outTXT.append("»ω");
				}
				if (lastNum == 0)
				{
					outTXT.append("ίδ");
				}
				lastNum = 1;
			}
			else{
				if (lastNum == 0)
				{
					outTXT.append("Ήώ");
				}
				if(i==7)
				{
					outTXT.append("Ήώ");
				}
				lastNum = 0;
			}
		} 
	}
	return 0;
}

int hachimi::remap()
{
	vector<unsigned char>text = msg;

	string word;
	unsigned char tt = 0, ttNum = 0;
	for (int i = 0;i < text.size() - 1;i += 2)
	{
		word.clear();
		word += text[i];
		word += text[i+1];
		if (word == (string)"Ήώ"){
			tt <<= 1;				//+  0
			ttNum++;
		}
		else if (word == (string)"»ω"){
			++(tt <<= 1);			//+  1
			ttNum++;
		}
		else if (word == (string)"ίδ"){
			++(tt <<= 2);			//+ 01
			ttNum+=2;
		}
		else {
			cerr << "undecodeable file" << endl;
			return -1;
		}
		
		if (ttNum == 8){
			outBin.push_back(tt);
			ttNum = tt = 0;
		}
	}
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

	if (EVP_DecryptFinal_ex(pDe_ctx, (unsigned char*)(_pOutBuf + outlen), &flen) != 1) {
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