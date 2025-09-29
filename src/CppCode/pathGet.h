#ifndef _PATHGET_H_
#define _PATHGET_H_
#include <string>
#include <limits>
#include <iostream>

using namespace std;

class pathGet
{
private:
	string rawPath;
	string rootDirName;
	string workRootDir;
	string fileName;
public:
	pathGet(string _myPath,string _rootDirName);
	~pathGet() = default;
	string getRootDir() { return workRootDir; }
};


#endif // !_PATHGET_H_




