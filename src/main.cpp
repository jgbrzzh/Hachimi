#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cstdio>

//ha 0  Ήώ
//ji 1	»ω
//mi 01	ίδ

using namespace std;

string FileName("../temp/out1.bin");
string FileNameOUT("../temp/hachimi.txt");

class hachimi {
private:
	std::vector<char> msg;
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
					output << "»ω";
				}
				if (lastNum == 0)
				{
					output << "ίδ";
				}
				lastNum = 1;
			}
			else{
				if (lastNum == 0)
				{
					output << "Ήώ";
				}
				if(i==7)
				{
					output << "Ήώ";
				}

				lastNum = 0;
			}
		} 
		std::cout << std::endl;
	}

	output.close();
	return 0;
}