#include <iostream>  
#include <string>

#include <sys/stat.h>
#include <filesystem>

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace cv;
using namespace std;


string Modes[5] = {
    "Ñ@#W$9876543210?!abc;:+=-,._ "
};

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


Mat resizeImage(Mat img){
    Mat resizedImg;
    resize(img, resizedImg, Size((img.size[0]/100)*params.renderQuality, (img.size[1]/100)*params.renderQuality), INTER_LINEAR);
    return resizedImg;
}

int map_(int x, int in_min, int in_max, int out_min, int out_max){
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void loadCharSet(Mat img){
    int tmp;
    string* charset = new string[img.rows];

    for(int i=0; i<img.rows; i++){
        for(int j=0; j<img.cols; j++){
            tmp = img.at<uchar>(i,j);
            tmp = map_(tmp,0,255,0,Modes[0].length()-1);
            charset[i]+=Modes[0][tmp];
        }
        cout<<charset[i]<<endl;
    }
}


//commandline: *.exe "Location/To/Image-Video.{extension}" [quality 1-100] [rendermode 1-3] [outputLocation "Location/To/Output"]
int main(int argc, char **argv){
    if(argc <=1 ) return -1;

    if(isParamsValid(argc,argv)){
        readParameter(argc,argv);
        
        Mat Image = imread(params.inputFileLocation,0);
        //cvtColor(Image, Image, cv::COLOR_BGR2GRAY);
        Image = resizeImage(Image);
        loadCharSet(Image);

        /*
        imshow("Image",img);
        waitKey(0);
        */
    }else{

    }

    return 0;
}
//g++ ascii.cpp -o ascii.exe -lopencv_core460 -lopencv_imgproc460 -lopencv_highgui460 -lopencv_ml460 -lopencv_video460 -lopencv_features2d460 -lopencv_calib3d460 -lopencv_objdetect460 -lopencv_flann460 -lopencv_videoio460 -lopencv_dnn460 -lopencv_gapi460 -lopencv_imgcodecs460 -lopencv_stitching460 -lopencv_photo460