#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <numeric>
#include <algorithm>
#include <math.h>

using namespace std;

class Task
{
public:
    int arrival;
    int capacity;
    int deadline;
    int period;

int diff(int time){
    return deadline-time;
}

};
int lcm(int a, int b)
{
    int max = a>b?a:b;

while(true)
{
    if(max%a==0 && max%b==0)
     {
         return max;
     }
    max++;
}
return 0;
}

vector<string> split(string s, string delimiter){
    vector<string> list;
    size_t pos = 0;
    string token;
    while ((pos = s.find(delimiter)) != string::npos) {
        token = s.substr(0, pos);
        list.push_back(token);
        s.erase(0, pos + delimiter.length());
    }
    return list;
}

int preform()
{
    int energy=0;
	string line,temp="";
	ifstream infile ("input.txt");
	ofstream outfile;
    outfile.open ("final.txt",std::ofstream::out | std::ofstream::app);
    outfile<<endl;
    outfile<<"Only EDF"<<endl;
    std::vector<Task> listoftask;

	if(infile.is_open())
	{
		while (getline (infile,line)){
            Task task_obj;
			int count=0;
			for (int i = 0; i < line.size(); i++)
			{
				if(line[i]==','){
                    int temp1=atoi(temp.c_str());
					switch (count){
						case 0: task_obj.arrival=temp1;
								count++;
								break;

						case 1: task_obj.capacity=temp1;
								count++;
								break;

						case 2: task_obj.deadline=temp1;
								count++;
								break;

						case 3: task_obj.period=temp1;
								count++;
                                listoftask.push_back(task_obj);
								break;
					}
					temp="";
				}else{
					temp+=line[i];
					}
				}
                int temp1=atoi(temp.c_str());
                    switch (count){
                        case 0: task_obj.arrival=temp1;
                                count++;
                                break;

                        case 1: task_obj.capacity=temp1;
                                count++;
                                break;

                        case 2: task_obj.deadline=temp1;
                                count++;
                                break;

                        case 3: task_obj.period=temp1;
                                count++;
                                listoftask.push_back(task_obj);
                                break;
                    }
                    temp="";
		}
	}


	int hyperperiod=1;
	for (int i = 0; i < listoftask.size(); i++)
	{
		cout<<listoftask[i].arrival<<" "<<listoftask[i].capacity<<" "<<listoftask[i].deadline<<" "<<listoftask[i].period<<endl;
		hyperperiod=lcm(hyperperiod,listoftask[i].period);
	}
    int time=0,position=NULL;
    std::vector<int>check_list;
    int min_diff=NULL,perform=-1;

    for(int time=0;time<hyperperiod;){
        perform=-1;
        min_diff=NULL;
        for(int j=0;j<listoftask.size();j++){
            if(listoftask[j].arrival==time){
                if(check_list.size()==0){
                    check_list.push_back(j);
                }
                else{
                    bool flag=false;
                    for (int i = 0; i <check_list.size() ; ++i){
                        if(j==check_list[i]){
                            flag=true;
                            break;
                        }
                    }
                    if (!flag){
                        check_list.push_back(j);
                    }
                }
            }
        }
        for (int i = 0; i < check_list.size(); ++i)
        {
            if(min_diff==NULL){
                min_diff=listoftask[check_list[i]].diff(time);
                perform=check_list[i];
            }
            else{
                if(listoftask[check_list[i]].diff(time)<min_diff){
                    min_diff=listoftask[check_list[i]].diff(time);
                    perform=check_list[i];
                }
            }
        }
        if(perform==-1){

        outfile<<time<<"--";
        time=time+1;
        outfile<<time<<" idle"<<endl;
        energy+=40;

        }else{
        outfile<<time<<"--";
        int a=time;
        int t=time;
        for(time+1;time<t+listoftask[perform].capacity;time++){
        for(int j=0;j<listoftask.size();j++){
            if(listoftask[j].arrival==time){
                bool flag=false;
                for (int i = 0; i <check_list.size() ; ++i){
                    if(j==check_list[i]){
                        flag=true;
                        break;
                    }
                }
                if (!flag){
                    check_list.push_back(j);
                    //cout<<j;
                }
            }
        }
        }
        outfile<<time<<" Do Task "<<perform+1<<endl;
        energy+=100*(time-a);
        listoftask[perform].arrival+=listoftask[perform].period;

        listoftask[perform].deadline+=listoftask[perform].period;

        std::vector<int>::iterator position = std::find(check_list.begin(), check_list.end(), perform);
        if (position != check_list.end()) // == myVector.end() means the element was not found
            check_list.erase(position);
        }

    }
    //cout<<"Output has been generated in output file"<<endl;
    outfile.close();
	return energy;
}


int main()
{
	string line,temp="";
	ifstream infile ("input.txt");
	ofstream outfile;
    outfile.open ("output.txt");
    outfile.clear();
    std::vector<Task> listoftask;

	if(infile.is_open())
	{
		while (getline (infile,line)){
            Task task_obj;
			int count=0;
			for (int i = 0; i < line.size(); i++)
			{
				if(line[i]==','){
                    int temp1=atoi(temp.c_str());
					switch (count){
						case 0: task_obj.arrival=temp1;
								count++;
								break;

						case 1: task_obj.capacity=temp1;
								count++;
								break;

						case 2: task_obj.deadline=temp1;
								count++;
								break;

						case 3: task_obj.period=temp1;
								count++;
                                listoftask.push_back(task_obj);
								break;
					}
					temp="";
				}else{
					temp+=line[i];
					}
				}
                int temp1=atoi(temp.c_str());
                    switch (count){
                        case 0: task_obj.arrival=temp1;
                                count++;
                                break;

                        case 1: task_obj.capacity=temp1;
                                count++;
                                break;

                        case 2: task_obj.deadline=temp1;
                                count++;
                                break;

                        case 3: task_obj.period=temp1;
                                count++;
                                listoftask.push_back(task_obj);
                                break;
                    }
                    temp="";
		}
	}
    infile.close();

	int hyperperiod=1;
	for (int i = 0; i < listoftask.size(); i++)
	{
		cout<<listoftask[i].arrival<<" "<<listoftask[i].capacity<<" "<<listoftask[i].deadline<<" "<<listoftask[i].period<<endl;
		hyperperiod=lcm(hyperperiod,listoftask[i].period);
	}
    cout<<"Hyperperiod: "<<hyperperiod<<endl;
    int time=0,position=NULL;
    std::vector<int>check_list;
    int min_diff=NULL,perform=-1;

    for(int time=0;time<hyperperiod;){
        perform=-1;
        min_diff=NULL;
        for(int j=0;j<listoftask.size();j++){
            if(listoftask[j].arrival==time){
                if(check_list.size()==0){
                    check_list.push_back(j);
                }
                else{
                    bool flag=false;
                    for (int i = 0; i <check_list.size() ; ++i){
                        if(j==check_list[i]){
                            flag=true;
                            break;
                        }
                    }
                    if (!flag){
                        check_list.push_back(j);
                    }
                }
            }
        }
        for (int i = 0; i < check_list.size(); ++i)
        {
            if(min_diff==NULL){
                min_diff=listoftask[check_list[i]].diff(time);
                perform=check_list[i];
            }
            else{
                if(listoftask[check_list[i]].diff(time)<min_diff){
                    min_diff=listoftask[check_list[i]].diff(time);
                    perform=check_list[i];
                }
            }
        }
        if(perform==-1){

        outfile<<time<<",";
        time=time+1;
        outfile<<time<<",i,"<<endl;

        }else{
        outfile<<time<<",";
        int t=time;
        for(time+1;time<t+listoftask[perform].capacity;time++){
        for(int j=0;j<listoftask.size();j++){
            if(listoftask[j].arrival==time){
                bool flag=false;
                for (int i = 0; i <check_list.size() ; ++i){
                    if(j==check_list[i]){
                        flag=true;
                        break;
                    }
                }
                if (!flag){
                    check_list.push_back(j);
                    //cout<<j;
                }
            }
        }
        }
        outfile<<time<<","<<perform+1<<","<<endl;
        listoftask[perform].arrival+=listoftask[perform].period;

        listoftask[perform].deadline+=listoftask[perform].period;

        std::vector<int>::iterator position = std::find(check_list.begin(), check_list.end(), perform);
        if (position != check_list.end()) // == myVector.end() means the element was not found
            check_list.erase(position);
        }

    }
    outfile.close();

    temp="";
    string prev_line,t_start="";
    ifstream infile2("output.txt");
    ofstream f_out;
    f_out.open ("final.txt");
    f_out.clear();
    int ideal_time=0,t_task=NULL;
    float total_E=0;
    bool prev_change=true;
    if(infile2.is_open())
	{
	    getline(infile2,prev_line);
		while (getline (infile2,line)){

            if(line[line.length()-2]!='i' && prev_line[prev_line.length()-2]!='i'){
                    vector<string> p = split(prev_line, ",");
                    int E = 100;
                    total_E+=(float)((atoi(p[1].c_str()))-(float)(atoi(p[0].c_str())))*100;
                    f_out<<p[0]<<"--"<<p[1]<<" Do task "<<p[2]<<" with Energy "<<E<<"%"<<endl;
            }else if(line[line.length()-2]=='i' && prev_line[prev_line.length()-2]=='i'){
                     //cout<<"case 2"<<endl;
                     ideal_time+=1;
            }else if(line[line.length()-2]=='i' && prev_line[prev_line.length()-2]!='i'){
                vector<string> p = split(prev_line, ",");
                t_start=p[0];
                t_task = atoi(p[2].c_str());
                ideal_time=1;
            }
            else if(line[line.length()-2]!='i' && prev_line[prev_line.length()-2]=='i'){

                    vector<string> p = split(prev_line, ",");
                    float E = 100*(listoftask[atoi(p[2].c_str())].capacity)/(listoftask[atoi(p[2].c_str())].capacity+ideal_time);
                    ideal_time=0;
                    if(E<60)E=60.0;
                    else if(E<75)E=75.0;
                    else if(E<80)E=80.0;
                    if(t_start.empty()){t_start=p[0];}
                    if(t_task==NULL){t_task=atoi(p[2].c_str());}
                    float mid_time = E*(float)(listoftask[atoi(p[2].c_str())].capacity)/100 + (float)atoi(t_start.c_str());
                    if(mid_time==0){
                    f_out<<t_start<<"--"<<p[1]<<" Do task "<<t_task<<" with Energy "<<E<<"%"<<endl;
                    total_E+=E*(atoi(p[1].c_str())-atoi(t_start.c_str()));
                    }
                    else{
                            total_E+=E*(mid_time-atoi(t_start.c_str()));
                        f_out<<t_start<<"--"<<mid_time<<" Do task "<<t_task<<" with Energy "<<E<<"%"<<endl;
                        f_out<<mid_time<<"--"<<p[1]<<" Idle with Energy 40%"<<endl;
                        total_E+=40*(atoi(p[1].c_str())-mid_time);//ideal energy
                    }
                    t_start="";
            }
            if(prev_change){
                prev_line=line;
            }else{
            prev_change=true;
            }
		}
    }
    if(ideal_time!=0){
            vector<string> p = split(prev_line, ",");
            float E = 100*(listoftask[atoi(p[2].c_str())].capacity)/(listoftask[atoi(p[2].c_str())].capacity+ideal_time);
            ideal_time=0;
            if(E<60)E=60.0;
            else if(E<75)E=75.0;
            else if(E<80)E=80.0;
            if(t_start.empty()){t_start=p[0];}
            if(t_task==NULL){t_task=atoi(p[2].c_str());}
            float mid_time = E*(float)(listoftask[atoi(p[2].c_str())].capacity)/100 + (float)atoi(t_start.c_str());
            if(mid_time==0){
            f_out<<t_start<<"--"<<p[1]<<" Do task "<<t_task<<" with Energy "<<E<<"%"<<endl;
            total_E+=E*(atoi(p[1].c_str())-atoi(t_start.c_str()));
            }
            else{
                total_E+=E*(mid_time-atoi(t_start.c_str()));
                f_out<<t_start<<"--"<<mid_time<<" Do task "<<t_task<<" with Energy "<<E<<"%"<<endl;
                f_out<<mid_time<<"--"<<p[1]<<" Idle with Energy 40%"<<endl;
                total_E+=40*(atoi(p[1].c_str())-mid_time);//ideal energy
            }
            t_start="";
    }

    cout<<"Output has been generated in output file"<<endl;
    cout<<"Total Energy Used is: "<<total_E<<endl;
    f_out.close();
    cout<<"EDF only energy: "<<preform()<<endl;
	return 0;
}

