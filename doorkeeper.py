import os,time

import sqlite3

while True:
    os.system("clear")
    print("+----------MENU-----------------------------------------------------------------+")
    print("| 1. Upload all changes to the lock                                             |")
    print("| 2. Add card                                                                   |")
    print("| 3. Delete card                                                                |")
    print("| 4. Show active cards                                                          |")
    print("| 5. Show deleted cards                                                         |")
    print("| 8. Emergency open (60s)                                                       |")
    print("| 9. Exit to shell                                                              |")
    print("+-------------------------------------------------------------------------------+")
    f = open("output.txt", "r")
    output="| Last output: "
    output+=f.read().rstrip()
    while(len(output) < 80):
        output += " "
    output+= "|"
    print output
    print("+-------------------------------------------------------------------------------+")
    time.sleep(0.2) 
    print("Choose item or enter to refresh")
    command = str(raw_input(">> "))

    if command == "1": 
        
        conn = sqlite3.connect("doorkeeper.db")
        cursor = conn.execute("SELECT * FROM cards WHERE card_deleted = '0'")
        results = cursor.fetchall()
        keys = 'String goodKeys[40] = {'
        for row in results:
            keys += '"'
            keys += str(row[1])
            keys += '",'
        keys += '"FUCKTRAILINGCOMMASNOTGONNADOTHIS"};'
        
        f = open("src_keys.cpp", "w")
        f.write(keys)
        f.close()
        
        filenames = ['src_top.cpp', 'src_keys.cpp', 'src_bottom.cpp']
        with open('src/main.cpp', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)
        
        time.sleep(5)
        os.system("screen -S 'doorkeeper_serial' -X quit")
        os.system('platformio run -e uno -t upload')
        os.system("screen -S 'doorkeeper_serial' -d -m")
        os.system("screen -r 'doorkeeper_serial' -X stuff $'\npython serial_listener.py\n'")
        print("\n\n\n")
        command = str(raw_input("Press enter to continue to menu..."))
    elif command == "2":
        print("+-ADD CARD----------------------------------------------------------------------+")
        uid = str(raw_input("uid: "))
        user = str(raw_input("owner: "))
        conn = sqlite3.connect("doorkeeper.db")
        cursor = conn.execute("SELECT * FROM cards WHERE card_uid = '"+uid+"' AND card_deleted = '0'")
        results = cursor.fetchall()
        if(len(uid) != 14):
            print("Uid's should always be 14 characters, dont use spaces and append 0's if needed")
        elif(len(user) < 3 or len(user) > 30):
            print("Owner name is too short or long!")
        elif(len(results) > 0):
            print("That uid already exists in the whitelist!")
            for row in results:
                print(str(row[1])+" : "+str(row[2]))
        else:
            conn.execute("INSERT INTO cards (card_uid,card_owner,card_added) VALUES ('"+uid+"','"+user+"','"+str(int(time.time()))+"')")
            conn.commit()
            print("Card added succesfully!")
            print("DO NOT FORGET TO UPLOAD THE CHANGES!")
        conn.close()
        print("+-------------------------------------------------------------------------------+")
        command = str(raw_input("Press enter to continue to menu..."))
    elif command == "3":
        print("+-DELETE CARD-------------------------------------------------------------------+")
        uid = str(raw_input("uid: "))
        conn = sqlite3.connect("doorkeeper.db")
        cursor = conn.execute("UPDATE cards SET card_deleted = '"+str(int(time.time()))+"' WHERE card_uid = '"+uid+"' and card_deleted = '0'")
        
        conn.commit()
        if(cursor.rowcount > 0):
            print("Card deleted succesfully!")
            print("DO NOT FORGET TO UPLOAD THE CHANGES!")
        else:
            print("No active cards found with that uid!")
        conn.close()
        print("+-------------------------------------------------------------------------------+")
        command = str(raw_input("Press enter to continue to menu..."))
    
    elif command == "4":
        conn = sqlite3.connect("doorkeeper.db")
        cursor = conn.execute("SELECT * FROM cards WHERE card_deleted = '0'")
        results = cursor.fetchall()
        print("+-ACTIVE CARDS------------------------------------------------------------------+")
        for row in results:
            print(str(row[1])+" : "+str(row[2]))
        conn.close()
        print("+-------------------------------------------------------------------------------+")
        command = str(raw_input("Press enter to continue to menu..."))
    elif command == "5":
        conn = sqlite3.connect("doorkeeper.db")
        cursor = conn.execute("SELECT * FROM cards WHERE card_deleted != '0'")
        results = cursor.fetchall()
        print("+-DELETED CARDS-----------------------------------------------------------------+")
        for row in results:
            print(str(row[1])+" : "+str(row[2]))
        conn.close()
        print("+-------------------------------------------------------------------------------+")
        command = str(raw_input("Press enter to continue to menu..."))
    elif command == "8":
        os.system("screen -S 'doorkeeper_serial' -X quit")
        print("Uploading emergency open script...\n\n\n")
        os.system('platformio run -e uno -t upload -c emergency.ini')
        print("\n\n\nWaiting 60 seconds..") 
        time.sleep(60)
        
        print("\n\n\nPreparing upload usual script...\n\n\n")
        os.system('platformio run -e uno -t upload')
        os.system("screen -S 'doorkeeper_serial' -d -m")
        os.system("screen -r 'doorkeeper_serial' -X stuff $'\npython serial_listener.py\n'")
        print("\n\n\n")
        command = str(raw_input("Press enter to continue to menu..."))
    elif command == "9":
        os.system("clear")
        exit()
    else:
        print("command not recognised")
