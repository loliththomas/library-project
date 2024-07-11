#PYTHON-SQL CONNECTOR MENU DRIVEN

from datetime import date
import smtplib
import random
import time
import arrow
import pickle
import mysql.connector as mycon
con=mycon.connect(host='localhost',user='root',password='lolu',database='library')
con2=mycon.connect(host='localhost',user='root',password='lolu',database='library',buffered=True)


#-----FUNCTIONS-----#

def date_diff(start,end):     
     f=start
     s=end    
     diff=(s-f) 
     return diff.days

def datenow():
    
    date=arrow.now().format('YYYY-MM-DD')
    return date


def c_lister(coloumn_name,table_name,feild_name=None,codition=None):
     if feild_name==None:
        cur=con.cursor()
        cur.execute("select {} from {};".format(coloumn_name,table_name))
        row=cur.fetchall()
        con.commit()
        cur.close()
        return row  #returns list of tuples (elements of given coloumn name)
     else:
        cur=con.cursor()
        cur.execute("select {} from {} where {}={}".format(coloumn_name,table_name,feild_name,codition))
        row=cur.fetchall()
        con.commit()
        cur.close()

        return row  #returns list of tuples 


def new_book(c=None,b=None): #to add a new book detail into book table    
     print()
     a=prim_key_creator('book_no','books')
     if c!=3:     #if choice 3..bname already accepted
         b=input('Enter book\'s name :')
     c=input('Enter authors name :')
     d=input('Enter type of book :')
     print()
    
     blist=c_lister('book_name','book_count') #to get the names of book already included
        
     cur=con.cursor()
     cur.execute("insert into books values({},'{}','{}','{}')".format(a,b,c,d))
     con.commit()
     cur.close() 
     if (b,) not in blist:   #checking for a tuple in the list(book name tuple which consist of no. of copies of a book)             
         cur1=con.cursor()
         cur1.execute('insert into book_count values("{}",{})'.format(b,1)) #inserts new rec if book name is not present
         con.commit()
         cur1.close()             
     else:
         cur1=con.cursor()
         cur1.execute('update book_count set no_of_copies=no_of_copies+1 where book_name="{}"'.format(b))#  increases no of copies by 1 if name already exists
         con.commit()
         cur1.close()


def prim_key_creator(cname,tname):
     pri_list=c_lister(cname,tname)
     if cname=='slno' and len(pri_list)==0:
         last_pri=1
         return last_pri
     elif cname=='admno' and len(pri_list)==0:
         last_pri=1001
         return last_pri
     elif cname=='book_no' and len(pri_list)==0:
         last_pri=101
         return last_pri
     elif cname=='staff_id' and len(pri_list)==0:
         last_pri=1001
         return last_pri
     else:   
         last_pri=pri_list[-1][0]
         return (last_pri+1)


def otp_emailer(otp,rec_email):        
    f=open('email.dat','rb')
    data=pickle.load(f)
    f.close()

    mail_list=data.keys()
    for i in mail_list:
        sender_email=i  
    passw=data[sender_email]

    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sender_email,passw)

        subject='Password Recovery OTP'
        body_1=str(otp)+' is the otp to recover the password'
        body_2='Please do not share this OTP with anyone'

        msg=f'Subject:{subject}\n\n{body_1}\n\n{body_2}'

        smtp.sendmail(sender_email,rec_email,msg)



def forgot_password():
    print()
    print('---------------------------------------------------------------------')
    sid=int(input('Enter staff id : '))

    cur=con.cursor()
    cur.execute('select * from staff_table where staff_id={}'.format(sid))
    row=cur.fetchall()
    con.commit()
    cur.close()

    name=row[0][1]
    email=row[0][2]
    
    print()
    sid_list=c_lister('staff_id','staff_table')

    if (sid,) in sid_list:
        f=open('Reset.txt','w')
        otp=random.randrange(123456,999999)
        otp_str=str(otp)
        f.write(otp_str)
        f.close()
        print()
        print('An otp is send to your mail.Please use it to reset the password')
        print('---------------------------------------------------------------------')

        reset_password(email)
        return 
    else:
        print('Staff not found ')
        print()
        print('Security breach detected')
        print()
        print('Going back to main menu in ',end=' ')
        for i in range(5,0,-1):
            print(i,end='  ')
            time.sleep(1)
        print()
        print()

        return 


def reset_password(email):
    f=open('Reset.txt')
    otp=f.read()
    f.close()

    otp_emailer(otp,email)
    
    w_count=0
    print()
    print()
    print('--------------------')
    otp_1=input('Enter otp : ')
    print('--------------------')
    print()
    if otp_1==otp:
        new_pass=input('Enter new password : ')
        print()
        print()
        f=open('lib pass.dat','wb')
        l=[new_pass]
        pickle.dump(l,f)
        f.close()
        print('''
+-----------------------------------+
|   Password changed successfully   |
+-----------------------------------+''')
        print()
        return
    
    else:
        w_count+=1
        print('INVALID OTP.TRY AGAIN')
        if w_count==3:
            print('Too many invalid attempts ')
            print()
            print()
            print('Security Breach')
            print()
            print()
            print('Closing program in',end='')
            for i in range(5,0,-1):
                print(i,end='  ')
                time.sleep(1)
            exit()
            return 
        reset_password(email)


#-----MAIN PROGRAM STARTS HERE-----#
     
t=input('''Press Enter to continue\nPress any other key to exit :''')
print()
incorrect_pass_count=0
print('Enter \'user\' if you are a student.Enter \'admin\' if you are a staff ')
while t=='':
     
     print()
     print('==============================')
     role=input('user or admin : ')
     print('==============================')
     print()
     if role=='admin':
        print()
        print('=====================================')
        print(' Press 1 if you forgot the password')
        print()
        print(' Press 0 to continue')
        print('=====================================')
        pass_choice=int(input(': '))
        print()
        print()
        if pass_choice==1:
            forgot_password()

        print('----------------------------------------')
        password=input('   Enter password : ')
        print('----------------------------------------')
        print()
        f=open('lib pass.dat','rb')
        data=pickle.load(f)
        passw=data[0]
        f.close()
        if password==passw:
            admn_while=''
            while admn_while=='':

                print('''
+------------------------------------------+
|1- To add detail of staff                 |
|2- To make updation in staff table        |
|3- To add detail of newly purchased book  |
|4- To donate a book                       |
|5- To change the password                 |
|6- To print details in a table            |
|7- To come out of admin                   |
|8- To clear the screen                    |
+------------------------------------------+
        ''')
                print()
   
                choice=int(input('Enter choice : '))
                
                if choice==1:
                    print()
                    print('----------------------------------------------------------')
                    
                    sid=prim_key_creator('staff_id','staff_table')
                    name=input('Enter name :')
                    email=input('Enter email id : ')

                    cur=con.cursor()
                    cur.execute('insert into staff_table values({},"{}","{}")'.format(sid,name,email))
                    con.commit()
                    cur.close() 
                    print()
                    admn_while=input('''Press Enter to continue\nPress any other key to exit :''')
            
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print()

                elif choice==2:
                    print()
                    print('----------------------------------------------------------')
                    
                    
                    field=input('Enter field name [name,email_id] : ')    
                    sid=int(input('Enter staff id : '))
                    new=input('Enter new value : ')

                    cur=con.cursor()
                    cur.execute('update staff_table set {}="{}" where staff_id={}'.format(field,new,sid))
                    con.commit()
                    cur.close()
                    print()
                    admn_while=input('''Press Enter to continue\nPress any other key to exit :''')
                    
                    
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print()

                elif choice==3:
                    print()
                    print('----------------------------------------------------------')
                   


                    slno=prim_key_creator('slno','purchase')
                    bname=input('Enter book name : ')
                    cost=eval(input('Enter amount : '))
                    dop=input('Enter date of purchase [yyyymmdd]: ')
                    seller=input('Enter name of supplier : ')
                    print()
               
                    cur=con.cursor()
                    cur.execute('insert into purchase values({},"{}",{},"{}","{}")'.format(slno,bname,cost,dop,seller))
                    con.commit()
                    cur.close()
                    new_book(choice,bname)
            
                
                    print()
                    admn_while=input('''Press Enter to continue\nPress any other key to exit :''')
                    
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print()

                elif choice==4:
                    print()
                    print('----------------------------------------------------------')
                    

                    new_book()
                    
                    admn_while=input('''Press Enter to continue\nPress any other key to exit :''')
                    
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print()

                elif choice==5:
                    print()
                    print('----------------------------------------------------------')
                    
                    cpass=input('Enter current password : ')
                    if cpass==passw:
                        print('-----------------------------------------')
                        npass=input(' Enter new password : ')
                        print('-----------------------------------------')
                        f=open('lib pass.dat','wb')
                        l=[npass]
                        pickle.dump(l,f)
                        f.close()
                        print('Password changed successfully')
                        print()                    
                        print()
                        admn_while=input('''Press Enter to continue\nPress any other key to exit :''')
                        
                        print('----------------------------------------------------------')
                        print()
                        print()
                        print()
                    else:
                        print()
                        print('Wrong password')
                        print('Access denied')
                        print()
                        break

                elif choice==6:
                    print()
                    print('----------------------------------------------------------')
                    
                    cur=con.cursor()
                    cur.execute('show tables')
                    row=cur.fetchall()
                    print('[',end='')
                    for i in row:
                        print(i,end=',')
                    print(']')
                    con.commit()
                    cur.close()

                    tname=input('Enter table name : ')
                    print()
                    cur=con.cursor()
                    cur.execute('select * from {}'.format(tname))
                    row=cur.fetchall()
                    for i in row:
                        print(i)
                    print()
                    con.commit()
                    cur.close()
                    print()
                    admn_while=input('''Press Enter to continue\nPress any other key to exit :''')
                    
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print()

                elif choice==7:
                    break
                elif choice==8:
                    print('\n'*25)
                    
                else:
                    print('''
                    +--------------------+
                    | Enter valid choice |
                    +--------------------+''')
                print()
                print()

        else:
            print('Wrong password.Try again')
            incorrect_pass_count+=1

            if incorrect_pass_count==5:
                print()
                print('Too many incorrect password ')
                print('Please try again after 30 sec',end='')
                incorrect_pass_count=0
                for i in range(15):
                    print('.',end=' ')
                    time.sleep(2)
                print()
            print()
            print()
            print()



     elif role=='user':

            user_while=''
            while user_while=='':
                print('''
+------------------------------------------+
|1- To print details of all books          |
|2- To search for a book details           |
|3- To take a book                         | 
|4- To return a book                       |
|5- To clear the screen                    |
|6- To come out of user                    |
|7- Exit                                   |
+------------------------------------------+
 ''')

                print()
                print('----------------------------')
                choice=int(input('Enter choice : '))
                print('----------------------------')
                print()
                if choice==1:         
                    cur=con.cursor()
                    cur.execute('select books.*,book_count.no_of_copies from books,book_count where books.book_name=book_count.book_name')
                    row=cur.fetchall()
                    print('[Book_no,book_name,author,type,book_count] ')
                    for i in row:
                        print(i)
                    con.commit()
                    cur.close()
                    print()
                    print()
                    user_while=input('''Press Enter to continue\nPress any other key to exit :''')
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print()
                           
                elif choice==2:           
                    search_type=int(input('''
+----------------------------------+
|On which basis you need to search |
|1. Name                           |
|2. Type of book                   |
|3. Author                         | 
|4. Type and author                | 
+----------------------------------+
Enter choice Number : '''))

                    print('----------------------------------------------------------')
                    print()
                    if search_type==1:
        
                        cname='book_name'
                        search_for='%'+input('Enter any character in the name :')+'%'
                        coloumn_list=c_lister('book_name','books')

                        cur=con.cursor()
                        cur.execute('select * from books where book_name like "{}"'.format(search_for))             
                        row=cur.fetchall()
                        con.commit()
                        cur.close()

                        if len(row)==0:
                            print('No such book')
                            print()
                            print('----------------------------------------------------------')
                            print()
                            continue
                        
                    elif search_type==2:
                        cname='type'
                        search_for=input('Enter book type :')
                        print()
                        coloumn_list=c_lister('type','books')

                        if (search_for,) not in coloumn_list:
                            print('No such book')
                            print()
                            print('----------------------------------------------------------')
                            print()
                            continue             
                    
                    elif search_type==3:
                        cname='author'
                        search_for=input('Enter name of author :')
                        print()
                        coloumn_list=c_lister('author','books')
                        if (search_for,) not in coloumn_list:
                            print('No such book')
                            print()
                            print('----------------------------------------------------------')
                            print()
                            continue

                    elif search_type==4:
                        btype=input('Enter type of book :')
                        auth=input('Enter name of author :')
                        
                        cur=con.cursor()
                        cur.execute('select * from books where type="{}"and author="{}" '.format(btype,auth))
                        row=cur.fetchall()
                        con.commit()
                        cur.close()

                        if len(row)==0:
                            print('No such book')
                            print()
                            print('----------------------------------------------------------')
                            print()
                            continue
                    
                    if search_type>1 and search_type<4: #ee if details print cheyyanayitt aan...meelilollathokke angane orannam ondon noku...ee if indenki print cheyanaytt edukkum            
                        cur=con.cursor()
                        cur.execute('select * from books where {}="{}"'.format(cname,search_for))
                        row=cur.fetchall()
                        con.commit()
                        cur.close()
            
                    print()

                    print('(book_no,book_name,author,type)')
                    for i in row:
                        print(i)
                    
                    print()
                    print('----------------------------------------------------------')
                    print()
                    user_while=input('''Press Enter to continue\nPress any other key to exit :''')
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print()
            
                elif choice==3:

                    print('----------------------------------------------------------')
                    
                    cur=con.cursor()
                    cur.execute('select books.*,book_count.no_of_copies from books,book_count where books.book_name=book_count.book_name')
                    row=cur.fetchall()
                    con.commit()
                    cur.close()

                    print('[Book_no,book_name,author,type,book_count] ')
                    for i in row:
                        print(i)
                    
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print('----------------------------------------------------------')
                    
                    bno=int(input('Enter book number : '))
                    bname=c_lister('book_name','books','book_no',bno)[0][0]
                    bnolist=c_lister('book_no','books')
                        
                    if (bno,) in bnolist: #ingane oru book library il ondoonn check cheyyunnu            
                        cur1=con.cursor()
                        cur1.execute('select no_of_copies from book_count,books where book_no={} and book_count.book_name=books.book_name'.format(bno)) # aa prticular bno ulla book ethra copy indenn nookkan
                        ncopy=cur1.fetchall()
                        #print(ncopy)
                        con.commit()
                        cur1.close()
                        
                        if ncopy[0][0]==0: #book inte no of copy 0 aanonn check cheyunnu
                            print('---------------------------------')
                            print('  Book is currently unavailable')
                            print('---------------------------------')
                            continue  
                        else:                
                            admno=int(input('Enter admission number : '))
                            print()
                            amnlist=c_lister('admno','stdbook')
                            
                            if (admno,) not in amnlist: # ayal veere book edthittindonn check cheyyan enn veenel parayaam....illankil stdbook table ileekk admno add cheyyum
                                cur=con.cursor()
                                cur.execute("insert into stdbook values('{}',{})".format(admno,1))
                                con.commit()
                                cur.close()  
                            else:
                                cur=con.cursor()
                                cur.execute("select no_of_books from stdbook where admno='{}'".format(admno)) #book edthittundenkil ethrayennam tot edthittindenn nokkkum
                                nob=cur.fetchall()
                                con.commit()
                                cur.close() 
                                if nob[0][0]==3: # max  at a tym edkkan pattanath 3 books
                                   
                                    print()
                                    print('You have taken maximum...Please return any book to explore more')
                                    print()
                                    print('Thank You')
                                    print('----------------------------------------------------------')
                                    print()
                                    continue# 3 book edthittundeel break                         
                                else: # illenkil existing no of books +1   
                                                     
                                    cur=con.cursor()
                                    cur.execute("update stdbook set no_of_books=no_of_books+1 where admno={}".format(admno))
                                    con.commit()
                                    cur.close()

                                cur1=con.cursor()
                                cur1.execute("update book_count set no_of_copies=no_of_copies-1 where book_name='{}'".format(bname))
                                con.commit()
                                cur1.close()


            
                                    
                            sname=input('Enter student\'s name : ')
                            cls=int(input('Enter class [in numbers] :'))
                            div=input('Enter division :')
                            bdate=datenow() #returns current date or todays date
                            rdate='NULL'
                            print()
            
                
                            cur=con.cursor()
                            cur.execute("insert into students values({},'{}',{},'{}',{},'{}',{})".format(admno,sname,cls,div,bno,bdate,rdate))  
                            con.commit()
                            cur.close()
                            
                            print('Please return the book on or before the seventh day')
                            print()
                            print('-------- Fine will be deducted for late returning--------')               
                    else: 
                        print('No such book')

                    print()
                    user_while=input('''Press Enter to continue\nPress any other key to exit :''')
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print()

                elif choice==4:   
                    print()
                    print('----------------------------------------------------------')
                            
                    admno=int(input('Enter Admission Number : '))
                    name=c_lister('Name','students','admno',admno)[0][0]
                    bno=int(input('Enter Book.No : '))
                    bname=c_lister('book_name','books','book_no',bno)[0][0]
                    rdate=input('Enter Date of returning [yyyymmdd]: ')
            
                    cur1=con.cursor()
                    cur1.execute('update students set returned_on="{}" where admno={} and book_no={}'.format(rdate,admno,bno))
                    cur1.close()
                    con.commit()

                    cur2=con.cursor()
                    cur2.execute('update stdbook set no_of_books=no_of_books-1 where admno={}'.format(admno))
                    cur2.close()
                    con.commit()

                    cur3=con.cursor()
                    cur3.execute('update book_count set no_of_copies=no_of_copies+1 where book_name="{}"'.format(bname))
                    cur3.close()
                    con.commit()

                    #taking the date of borrowing
                    cur=con2.cursor()
                    cur.execute("select taken_on from students where admno={} and book_no={}".format(admno,bno))
                    t_date_row=cur.fetchone() 
                    con2.commit()
                    cur.close() 
                    

                    #taking the date of returning
                    cur=con2.cursor()
                    cur.execute("select returned_on from students where admno={} and book_no={}".format(admno,bno))
                    r_date_row=cur.fetchone() 
                    con2.commit()
                    cur.close()

                    taken_date=t_date_row[0] 
                    returned_date=r_date_row[0]                   
                    day_diff=date_diff(taken_date,returned_date)
                    
                    if day_diff>7:
                        print()

                        print('+------------+')
                        print('| Fine - 30/-|')
                        print('+------------+')
            
                        admno_list=c_lister('admno','fine_table')
            
                        if (admno,) not in admno_list:
                            cur=con.cursor()
                            cur.execute('insert into fine_table values({},"{}",{})'.format(admno,name,30))
                            con.commit()
                            cur.close()
                        else: 
                            cur=con.cursor()
                            cur.execute('update fine_table set tot_fine=tot_fine+30 where admno={}'.format(admno))
                            con.commit()
                            cur.close()
                            
                    print()
                    
                    user_while=input('''Press Enter to continue\nPress any other key to exit :''')
                    print('----------------------------------------------------------')
                    print()
                    print()
                    print()
                    
                elif choice==5:
                    print('\n'*25)
                    user_while=''
                elif choice==6:
                    break
                elif choice==7:
                    print('------------THANK YOU----------')
                    exit()                   
                else:
                    print('''
                    +------------------------+
                    |   Enter valid choice   |
                    +------------------------+''')
                    print()
                    continue
                    
