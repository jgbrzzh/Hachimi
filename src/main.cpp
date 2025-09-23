#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cstdio>

//ha 0  ¹þ
//ji 1	»ù
//mi 01	ßä

using namespace std;

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
	int codeFlag = 0;//0:encode 1:decode
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
		}
		else if (argv[2] == "decode")
		{
			codeFlag = 1;
		}
		break;
	default:
		break;
	}

	hachimi ha(FileName);
	if (codeFlag == 0)
	{
		ha.map();
	}
	else {
		ha.remap();
	}
	//ha.map();
	//ha.remap();

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
	ifstream hachimi;
	hachimi.open(FileName,ios::in);
	if (!hachimi.is_open()){
		cout << "file£º" << FileName << " cant open" << endl;
	}
	string text;
	hachimi >> text;
	hachimi.close();

	ofstream out1;
	out1.open(DeEncodeOutFile, ios::out | ios::trunc | ios::binary);
	if (!out1.is_open()) {
		cout << "file£º" << DeEncodeOutFile << " cant open" << endl;
	}

	string word;
	unsigned char tt = 0, ttNum = 0;
	for (int i = 0;i < text.size();i += 2)
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

