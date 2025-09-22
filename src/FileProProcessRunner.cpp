#include <cstdlib>
int main() {
    int r = std::system("python src/python/FilePreProcessRunner.py");
    return r;
}
