#include <iostream>
#include <ctime>
#include <iomanip>
#include <windows.h>
using namespace std;

//https://www.ionos.com/digitalguide/server/configuration/shutdown-commands-via-cmd/
//https://en.cppreference.com/w/cpp/chrono/c/tm

time_t getRemainingTime(int hour, int min, int sec);

int main() {
    
    int ore, minuti;
    cout << "Inserire l'orario (formato ore.minuti) di spegnimento: ";
    char separator;
    cin >> ore >> separator >> minuti;
    bool exit = false;
    string sec_value = to_string(getRemainingTime(ore, minuti, 0));
    
    
    const string COMMAND = "shutdown /s /t " + sec_value;
    system(COMMAND.c_str());
    
    cout<<"Tempo rimanente allo spegnimento, premi piu' volte CTR+ALT+X per annullare"<<endl;
    for (int i = getRemainingTime(ore, minuti, 0) - 2; i > 0; i--) {
        cout << "\r";
        cout << "Ore: " << i / 3600 << " ";
        cout << "Minuti: " << (i % 3600) / 60 << " ";
        cout << "Secondi: " << i % 60 << " ";
        cout.flush();
        if ((GetAsyncKeyState(VK_CONTROL) & 0x8000) && (GetAsyncKeyState(VK_MENU) & 0x8000) && (GetAsyncKeyState(0x58) & 0x8000)) {//Ctrl+Alt+X
            system("shutdown /a");
            break;
            exit = true;
        }
         Sleep(1000);   
        }
        if (exit){
            cout <<"Spegnimento annullato"<<endl;
        }
  
    
    system("pause");
    return 0;
}

time_t getRemainingTime(int hour, int min, int sec) {
    time_t now = time(0);
    tm* ltm = localtime(&now);
    tm input_time = *ltm; 
    input_time.tm_hour = hour;
    input_time.tm_min = min;
    input_time.tm_sec = sec;
    time_t diff = difftime(mktime(&input_time), now);
    return diff;
}
