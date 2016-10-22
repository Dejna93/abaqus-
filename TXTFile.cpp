#include "TXTFile.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iomanip>
pcl::TXTFile::TXTFile() {

}

pcl::TXTFile::~TXTFile() {

}

std::vector<PointXYZ> pcl::TXTFile::loadTxtFile(std::string &file_name) {
	std::ifstream file;
	std::cout << "Loading from txt file \n";
	pcl::TXTFile::loadFile(file_name, file);

	return points;
	
}

int pcl::TXTFile::loadFile(std::string &file_name, std::ifstream & file) {

	//FOR DEBUG DELETE IN RELEASE VERSION
	file_name = "dane.txt";
	std::cout << "File to open :" << file_name <<"\n";
	file.open(file_name, std::ios::in);

	if (file.is_open()) {
			while(!file.eof()) {
				PointXYZ point;

				file >> point;
				points.push_back(point);
		}
	}
	return 1;

}

std::istream & pcl::operator >> (std::istream & input, PointXYZ & point)
{
	// Zczytywanie lini z pliku i prasowanie jej do structury PointXYZ
	PointXYZS points;

	std::string line;  std::getline(input, line);
	std::stringstream stream(line);

	stream >> points.x >> points.y >> points.z;

	point.x = stof(points.x);
	point.y = stof(points.y);
	point.z = stof(points.z);

	std::cout << point << "\n";
	return input;
}


std::ostream& pcl::operator<<(std::ostream & out, const PointXYZ &p) {
	using namespace std;
	out << "point	"
		<< setw(4) << left << p.x << " "
		<< setw(4) << left << p.y << " "
		<< setw(4) << left << p.z << " ";
	return out;
}