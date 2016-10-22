#include <iostream>
#include "TXTFile.h"

int validArgs(int argc, char** argv) {

	if (argc != 1) {
		return 0;
	}
	return 1;
}

int
main(int argc, char** argv)
{
	std::cout << "Txt praser to PCL \n";
	if (validArgs(argc,argv)) {
		pcl::TXTFile file;
		file.loadTxtFile( (std::string)argv[0]);
	}
	system("pause");
	return (0);
}
