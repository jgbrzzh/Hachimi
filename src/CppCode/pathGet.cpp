#include "pathGet.h"


pathGet::pathGet(string _myPath, string _rootDirName = "Hachimi")
	:rawPath(_myPath), rootDirName(_rootDirName)
{
	size_t p, npos = -1;
	string tmp;
	while (1) {
		p = _myPath.find_last_of('\\');
		if (p == npos)
		{
			cout << "not find:" << _rootDirName << endl;
		}
		tmp = _myPath.substr(p + 1, _myPath.size() - p - 1);
		if (tmp._Equal(_rootDirName))
			break;
		_myPath = _myPath.substr(0, p);
		cout << _myPath << endl;
	}
	cout << "workdir:" << _myPath << endl;
	workRootDir = _myPath;
}

int pathGet::inFileName(string _inFilePath)
{
	size_t p = _inFilePath.find_last_of('\\');
	_inFilePath = _inFilePath.substr(p + 1, _inFilePath.size() - p - 1);
	fileName = _inFilePath.substr(_inFilePath.size() - _inFilePath.find_last_of('.') - 1);
	return 0;
}

string pathGet::getFileName()
{
	return fileName;
}