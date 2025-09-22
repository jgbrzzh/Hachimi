#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>

std::string FileName("../temp/out1.bin");

class hachimi {
private:

public:
	std::vector<char> msg;
	int map();
	int remap();

public:
	hachimi(std::vector<char> content);
	std::string process();
};

int main()
{
	//std::ifstream file(FileName,std::ios::binary);
	//if (!file.is_open())
	//{
	//	std::cerr << "open "<< FileName<<" failed" << std::endl;
	//	return 1;
	//}
	//std::cout << "open " << FileName << std::endl;
	//std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
	//std::cout << "===ÎÄ¼þÄÚÈÝ===" << std::endl;
	//std::cout << content << std::endl;

	//file.close();

	std::vector<char> text;
	text.push_back(243);
	text.push_back(242);
	text.push_back(241);
	text.push_back(240);
	hachimi ha(text);
	ha.map();


	system("pause");
	return 0;
}

hachimi::hachimi(std::vector<char> content)
	:msg(content)
{

}

int hachimi::map() 
{
	if (msg.empty())
	{
		std::cerr << "empty content" << std::endl;
		return 1;
	}
	

	for (int j = 0;j < msg.size();j++)
	{
		char a = msg[j], tmp = 0;
		for (int i = 0;i < 8;i++)
		{
			tmp = a;
			tmp << i;
			tmp >> (7 - i);
			std::cout << tmp << " \n";
		}
		std::cout << std::endl;
	}


	return 0;
}