#pragma once
#include <string>
#include <vector>

//TEMP STRUCT
struct PointXYZ {
	float x;
	float y;
	float z;
	
};
//TEMP STRUCT 
struct PointXYZS
{
	std::string x;
	std::string y;
	std::string z;
};

//  They will be remove after link with PCL main core

namespace pcl {

	std::istream& operator>> (std::istream &input, PointXYZ & point);
	std::ostream& operator<<(std::ostream & out, const PointXYZ &p);

	class TXTFile
	{
	
	public:
		TXTFile();
		~TXTFile();
		std::vector<PointXYZ> loadTxtFile(std::string &file_name );


	private:
		std::vector<PointXYZ> points;
		int loadFile(std::string &file_name,  std::ifstream & file);
		friend std::istream& operator>> (std::istream & input, PointXYZ & point);
		friend std::ostream& operator<<(std::ostream & out, const PointXYZ &p);
	};

	
}

