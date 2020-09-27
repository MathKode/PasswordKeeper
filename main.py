import sqlite3
import sys
import os
from Crypto.Cipher import AES
import base64
import struct
import glob
from fernet_custom import *
from hash_lib import Hash
from tkinter.messagebox import *
from tkinter import *



logo="""
 _____  _____ _       _____                       _       ______                                   _ 
/  ___||  _  | |     /  __ \                     | |      | ___ \                                 | |
\ `--. | | | | |     | /  \/ ___  _ __  ___  ___ | | ___  | |_/ /_ _ ___ _____      _____  _ __ __| |
 `--. \| | | | |     | |    / _ \| '_ \/ __|/ _ \| |/ _ \ |  __/ _` / __/ __\ \ /\ / / _ \| '__/ _` |
/\__/ /\ \/' / |____ | \__/\ (_) | | | \__ \ (_) | |  __/ | | | (_| \__ \__ \\ V  V / (_) | | | (_| |
\____/  \_/\_\_____/  \____/\___/|_| |_|___/\___/|_|\___| \_|  \__,_|___/___/ \_/\_/ \___/|_|  \__,_|
                                                                                                     
                                                                                                     
 _   __ _____ ___________ ___________                                                                
| | / /|  ___|  ___| ___ \  ___| ___ \                                                               
| |/ / | |__ | |__ | |_/ / |__ | |_/ /                                                               
|    \ |  __||  __||  __/|  __||    /                                                                
| |\  \| |___| |___| |   | |___| |\ \                                                                
\_| \_/\____/\____/\_|   \____/\_| \_|           \n\n"""                                                    
                                                                                                     
                                                                                                     

print(logo)
def flush():
    try:
        os.remove("log.log")
    except:
        print("files dont exist")
    try:
        os.remove('gestionnaire.db.encrypted')
    except:
        print("files dont exist")
    try:
        os.remove('gestionnaire.db')
    except:
        print("files dont exist")
    try:
        os.remove('gestionnaire_encrypted.db')
    except:
        print("files dont exist")
    try:
        os.remove('accounthash.hash')
    except:
        print("files dont exist")
def create():
    if not 'gestionnaire.db' in glob.glob('*.db'):
        conn = sqlite3.connect('gestionnaire.db')
        conn.close()
    if not 'log.log' in glob.glob('*.log'):
        with open('log.log',"w") as file:
            file.write("")
    print('Creating or Changing password ...')
        



def encrypt(passwd):

    conn = sqlite3.connect('gestionnaire.db')
    conn2 = sqlite3.connect('gestionnaire_encrypted.db')

    cur2=conn2.cursor()
    cur = conn.cursor()

    cmd2='CREATE TABLE IF NOT EXISTS gestionnaire(user TEXT, password TEXT, site TEXT);'
    cmd="SELECT * FROM gestionnaire;"

    cur2.execute(cmd2)
    cur.execute(cmd)

    conn2.commit()
    conn.commit()

    retour = cur.fetchall()

    for elements in retour:
        liste_encrypt=[]
        #print(elements)
        for element in elements:
            #print(element)
            element_encrypted=password_encrypt(element.encode(),passwd) #from fernet custom
            #print(element_encrypted)
            liste_encrypt.append(element_encrypted.decode("utf-8"))
        #print(liste_encrypt)
        
        try:
            cmd2=f"INSERT INTO gestionnaire(user, password, site) VALUES ('{liste_encrypt[0]}','{liste_encrypt[1]}','{liste_encrypt[2]}');"
            cur2.execute(cmd2)
            conn2.commit()
        except:
            print('Out of range: In Insertion')

        retour2 = cur2.fetchall()
        #print(retour2)

    cur2.close()
    conn2.close()
    cur.close()
    conn.close()
    os.remove('gestionnaire.db')
    with open('log.log','a') as filename:
        filename.write('Encrypted\n')
def decrypt(passwd):

    conn = sqlite3.connect('gestionnaire_encrypted.db')
    conn2 = sqlite3.connect('gestionnaire.db')

    cur2=conn2.cursor()
    cur = conn.cursor()

    cmd2='CREATE TABLE IF NOT EXISTS gestionnaire(user TEXT, password TEXT, site TEXT);'
    cmd="SELECT * FROM gestionnaire;"

    cur2.execute(cmd2)
    cur.execute(cmd)

    conn2.commit()
    conn.commit()

    retour = cur.fetchall()

    for elements in retour:
        liste_decrypt=[]
        #print(elements)
        for element in elements:
            #print(element)
            element_decrypted=password_decrypt(element.encode(),passwd) #from fernet custom
            #print(element_encrypted)
            liste_decrypt.append(element_decrypted.decode("utf-8"))
        #print(liste_decrypt)
        
        try:
            cmd2=f"INSERT INTO gestionnaire(user, password, site) VALUES ('{liste_decrypt[0]}','{liste_decrypt[1]}','{liste_decrypt[2]}');"
            cur2.execute(cmd2)
            conn2.commit()
        except:
            print('Out of range: In Insertion')
            with open('log.log','a') as logfile:
                logfile.write('[_] SQL Does not accept Bytes types objects')

        retour2 = cur2.fetchall()
        #print(retour2)

    cur2.close()
    conn2.close()
    cur.close()
    conn.close()
    os.remove('gestionnaire_encrypted.db')
    with open('log.log','a') as filename:
        filename.write('Decrypted\n')





def log(status):
    test=True
    if status=='in':
        try:
            #if log_data_splitted[0]=="Encrypted":
            if "gestionnaire_encrypted.db" in glob.glob('*.db'):
                todo=False
            else:
                todo=True
        except:
            todo=True
        with open('log.log','a') as logfile:
            if todo==True:
                print("Please Create a database First")

            elif todo==False:
                allow=False
                logfile.write('[+] Starting Database \n')
                if allow==False:
                    database_pass=password_login.get()
                    if database_pass=="q":
                        with open('var.txt','w') as varfile:
                            varfile.write('out')
                        sys.exit()
                    hash2=Hash(database_pass)
                    allow=hash2.verify()
                    if allow==False:
                        messagebox.showwarning("Warning","Incorrect Password")
                        logfile.write(f"[_] Connexion Attempt with Password :{database_pass}")
                    else:
                        print("Login Successfully")
                        with open('var.txt','w') as varfile:
                            varfile.write('in')
                try:
                    decrypt(database_pass)
                except:
                    #print("error in decryption")
                    logfile.write('[_] Error in Decryption')


                global password_temp
                password_temp=database_pass

    elif status=='out':
        with open('log.log','a') as logfile:
            logfile.write("[*] Shuting Down Database\n")
            try:
                if password_temp==None:
                    password_temp=input("Type Your Password Please :")
            except:
                sys.exit()
            if "gestionnaire.db" in glob.glob('*.db'):
                try:
                    encrypt(password_temp)
                except:
                    pass
                with open('var.txt','w') as varfile:
                    varfile.write('out')
                sys.exit()

def verif():
    if 'gestionnaire.db' in glob.glob("*.db"):
        conn = sqlite3.connect('gestionnaire.db')
    else:
        print('Connecting To Encrypted Database')
        conn = sqlite3.connect('gestionnaire_encrypted.db')
    cur = conn.cursor()
    cmd=f"SELECT * FROM gestionnaire;"
    cur.execute(cmd)
    conn.commit()

    retour = cur.fetchall()
    for elem in retour:
        liste_mots=[]
        for element in elem:
            liste_mots.append(element)
        try:
            if liste_mots[0]!='0' and liste_mots[1]!='0' and liste_mots[2]!='Values_Init':
                print(f"User: {liste_mots[0]} Password: {liste_mots[1]} site : {liste_mots[2]}")
        except:
            pass
def verif_encrypt():
    conn = sqlite3.connect('gestionnaire_encrypted.db')
    cur = conn.cursor()
    cmd="SELECT* FROM gestionnaire;"
    cur.execute(cmd)
    conn.commit()

    retour = cur.fetchall()
    print(retour)
    cur.close()
    conn.close()

def gestionnaire():
    conn = sqlite3.connect('gestionnaire.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS gestionnaire(user TEXT, password TEXT, site TEXT);")
    cur.execute("INSERT INTO gestionnaire(user, password, site) VALUES ('0','0','Values_Init');")
    conn.commit()

    retour = cur.fetchall()
    #print(retour)

    cur.close()
    conn.close()

def add_mdp():
    user=useradd.get()
    password=userpass.get()
    site=usersite.get()
    data=(user,password,site)
    conn = sqlite3.connect('gestionnaire.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO gestionnaire(user, password, site) VALUES (?,?,?);",data)
    conn.commit()

    retour = cur.fetchall()
    #print(retour)
    cur.close()
    conn.close()



with open('var.txt','w') as varfile:
        varfile.write('out')

def verify():
    with open('var.txt','r') as varfile:
        data=varfile.read()
        if data=="in":
            loginstatus='Logged'
        else:
            loginstatus='Not Logged'


    text="Status: "+str(loginstatus)
    l6=LabelFrame(root,text="LOGIN STATUS")
    l6.pack()
    textbox3=Label(l6,text=text).pack(side="left")
    l6.place(relx=0.5, relheight=0.12, relwidth=0.5,rely=0.55)
    
    root.after(3000,verify)

def choix(choix):
    #choix=int(input(f"[--] - 1.Flush 2.Create/Change Pass (if logged) 3.Login 4.Add 5.Content 6.Logout   :"))
    if choix==1:
        flush()
    elif choix==2:
        choix_2=check_var.get()
        password_user=password_create.get()
        if 'gestionnaire_encrypted.db' in glob.glob("*.db"):
            if choix_2=="1":
                flush()
            else:
                with open('var.txt','w') as varfile:
                    varfile.write('out')
                sys.exit()
        create()
        gestionnaire()
        

        hash_user=Hash(password_user)
        with open('accounthash.hash','w') as hashwrite:
            hash_user.hasher()
            hashwrite.write(hash_user.hash)

        encrypt(password_user)
        sys.exit()
    elif choix==3:
        log('in')
    elif choix==4:
        add_mdp()
    elif choix==5:
        verif()
    elif choix==6:
        log('out')

    #################################### DEV TOOLS
    elif choix==8:                     # DEV TOOLS
        encrypt('password')            # DEV TOOLS
    elif choix==9:                     # DEV TOOLS
        verif_encrypt()                # DEV TOOLS
    elif choix==10:                    # DEV TOOLS
        decrypt('password')            # DEV TOOLS
    #################################### DEV TOOLS
    print('\n')

def refresh():
    if 'gestionnaire.db' in glob.glob("*.db"):
            conn = sqlite3.connect('gestionnaire.db')
    else:
        print('Connecting To Encrypted Database')
        conn = sqlite3.connect('gestionnaire_encrypted.db')
    cur = conn.cursor()
    cmd=f"SELECT * FROM gestionnaire;"
    cur.execute(cmd)
    conn.commit()

    retour = cur.fetchall()
    for elem_remove in retour:
        listNodes.delete("0")
    for elem in retour:
        liste_mots=[]
        for element in elem:
            liste_mots.append(element)
        try:
            if liste_mots[0]!='0' and liste_mots[1]!='0' and liste_mots[2]!='Values_Init':
                text=f"  User: {liste_mots[0]}   Password: {liste_mots[1]}   site : {liste_mots[2]}"
                listNodes.insert(END,text)
        except:
            pass

def remove():
    pass

def start_server():
    print('starting server')

root = Tk()
root.title("PasswordKeeper")
root.geometry("550x550")
password_create=StringVar()
check_var=IntVar()
password_login=StringVar()
useradd=StringVar()
userpass=StringVar()
usersite=StringVar()

l=LabelFrame(root, text="LOG OPTIONS")
l.pack(side=RIGHT)

l2=LabelFrame(root,text='ACTIONS')
l2.pack(side=LEFT)

l3=LabelFrame(root,text="CONTENT")
l3.pack()

l4=LabelFrame(root,text="ADD")
l4.pack()

l5=LabelFrame(root,text="SERVER")
l5.pack()

l6=LabelFrame(root,text="LOGIN STATUS")
l6.pack()

flushing = Button(l2, text='Flush',command=lambda: choix(1)).pack()


text=Label(l2,text="Password For New db :").pack()
password_creation= Entry(l2, textvariable=password_create).pack() 
creation = Button(l2, text='Create Or Change Password',command=lambda: choix(2)).pack()
check=Checkbutton(l2, text="Destroy previous", variable=check_var).pack()

text2=Label(l,text="Database Password (q to quit):").pack()
password_entry = Entry(l, textvariable=password_login).pack() 
submit = Button(l, text='Connect',command=lambda: choix(3)).pack(side=LEFT)
submit2 = Button(l, text='Disconnect',command=lambda:choix(6)).pack(side=RIGHT)

text3=Label(l4,text="User :").pack()
User_Entry = Entry(l4, textvariable=useradd).pack() 
text3=Label(l4,text="Password :").pack()
Password_User_Entry = Entry(l4, textvariable=userpass).pack() 
text4=Label(l4,text="Site :").pack()
site_user_entry = Entry(l4, textvariable=usersite).pack()
submit21 = Button(l4, text='Add',command=lambda: choix(4)).pack()

serverbutton=Button(l5,text='Start Server', command=start_server).pack()

listNodes=Listbox(l3, width=75, heigh=10)
listNodes.pack(side=RIGHT)

scrollbar=Scrollbar(l3, orient="vertical")
scrollbar.config(command=listNodes.yview)
scrollbar.pack(side="right", fill='y')

listNodes.config(yscrollcommand=scrollbar.set)

refresh_button=Button(l3,text="Refresh",command=refresh).pack()
remove_button=Button(l3,text="Remove", command=remove).pack()


l.place(relx=0, relheight=0.25, relwidth=0.5)
l2.place(relx=0.5, relheight=0.55, relwidth=1.0 - 0.5)
l3.place(relheight=0.3, relwidth=1.0,rely=0.68)
l4.place(relx=0, relheight=0.30, relwidth=0.5,rely=0.25)
l5.place(relx=0, relheight=0.12, relwidth=0.5,rely=0.55)
l6.place(relx=0.5, relheight=0.12, relwidth=0.5,rely=0.55)
root.after(2000,verify)
root.mainloop()
if 'gestionnaire.db' in glob.glob("*.db"):
    encrypt(password_temp)