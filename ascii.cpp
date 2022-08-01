#include <string>
using namespace std;

struct {
    int renderStringType;
    int renderQuality;

    string inputFileLocation;
    string inputFileName;
    string inputType;

    string outputFileLocation;
    string outputFileName;
    string outputType;
}params;

void readParameter(int count,char **argv){
    
}

bool isParamsValid(int count,char **argv){
    return false;
}

int main(int argc, char **argv){
    if(isParamsValid(argc,argv)){
        readParameter(argc,argv);
        //todo: convert the image/video to ascii with the parameter specified
    }else{

    }

    return 0;
}