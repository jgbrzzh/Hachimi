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

string FileName("../temp/out1.bin");
string FileNameOUT("../temp/hachimi.txt");

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
	hachimi(std::vector<char> content,string inFile);
	std::string process();
};

int main()
{
	std::vector<char> text;
	text.push_back(243);
	text.push_back(242);
	text.push_back(241);
	text.push_back(240);
	hachimi ha(text,FileName);
	ha.map();
	ha.remap();

	system("pause");
	return 0;
}

hachimi::hachimi(std::vector<char> content, string inFile)
	:InFileName(inFile)
{
	binContent.open(InFileName, ios::out);
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
	output.open(FileNameOUT,ios::out | ios::trunc);

	char lastNum = -1;//indicate last number
	for (int j = 0;j < msg.size();j++)
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
	hachimi.open(FileNameOUT,ios::in);
	if (!hachimi.is_open()){
		cout << "file£º" << FileNameOUT << " cant open" << endl;
	}
	string text;
	hachimi >> text;

	string word;
	for (int i = 0;i < text.size();i += 2)
	{
		word.clear();
		word += text[i];
		word += text[i+1];
		if (word == (string)"¹þ")
		{
			cout << '0';
		}
		if (word == (string)"»ù")
		{
			cout << '1';
		}
		if (word == (string)"ßä")
		{
			cout << '0' << '1';
		}
	}

	hachimi.close();
	return 0;
}

