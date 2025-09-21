#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>

std::string FileName("../temp/out1.bin");

class hachimi {
private:
	std::string msg;
	int map();
	int remap();

public:
	hachimi(std::string content);
	std::string process();
};

int main()
{
	std::ifstream file(FileName,std::ios::binary);
	if (!file.is_open())
	{
		std::cerr << "open "<< FileName<<" failed" << std::endl;
		return 1;
	}
	std::cout << "open " << FileName << std::endl;
	std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
	std::cout << "===ÎÄ¼þÄÚÈÝ===" << std::endl;
	std::cout << content << std::endl;

	file.close();
	system("pause");
	return 0;
}

hachimi::hachimi(std::string content) 
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
	


	return 0;
}