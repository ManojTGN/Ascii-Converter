#include <iostream>  
#include <string>

#include <sys/stat.h>
#include <filesystem>

using namespace std;

struct {

    int renderStringMode = 1;
    int renderQuality = 80;

    string inputFileLocation;
    string inputFileName;

    string outputFileLocation;
    string outputFileName;

}params;

void readParameter(int count,char **argv){
    params.inputFileLocation = argv[1];
    params.inputFileName = params.inputFileLocation.substr(params.inputFileLocation.find_last_of('\\')+1,params.inputFileLocation.length());
    
    if(count < 3) return;
    params.renderQuality = stoi(argv[2]);
    if(params.renderQuality > 100) params.renderQuality = 100;
    else if(params.renderQuality <= 0 ) params.renderQuality = 1;

    if(count < 4) return;
    params.renderStringMode = stoi(argv[3]);
    if(params.renderStringMode > 3) params.renderStringMode = 3;
    else if(params.renderStringMode <= 0 ) params.renderStringMode = 1;
    
    if(count < 5) params.outputFileLocation = filesystem::current_path().string();
    else params.outputFileLocation = argv[4];

}

bool isParamsValid(int count,char **argv){
    if(count < 2) return false;

    struct stat buffer;  
    if(stat (argv[1], &buffer) != 0) return false;

    if(count >= 3)
    for(int i = 0; i < strlen(argv[2]); i++ ) if(!isdigit(argv[2][i])) return false;

    if(count >= 4)
    for(int i = 0; i < strlen(argv[3]); i++ ) if(!isdigit(argv[3][i])) return false;

    if(count >= 5)
    if(stat (argv[4], &buffer) != 0) return false;
    
    return true;
}

//commandline: *.exe "Location/To/Image-Video.{extension}" [quality 1-100] [rendermode 1-3] [outputLocation "Location/To/Output"]
int main(int argc, char **argv){
    if(isParamsValid(argc,argv)){
        readParameter(argc,argv);
        
        cout<<params.inputFileLocation<<endl<<params.inputFileName<<endl<<params.outputFileLocation<<endl<<params.renderQuality<<endl<<params.renderStringMode<<endl;

    }else{

    }

    return 0;
}