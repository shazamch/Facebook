import sqlite3
from tkinter import messagebox
import tkinter
import customtkinter
from PIL import Image, ImageTk
import os

class Facebook:
    def __init__(self):
        self.user = 'shazam'
    def open_sql(self):
        connection = sqlite3.connect('Facebook.db'); access = connection.cursor()
        return connection,access
    def close_sql(self,connection):
        connection.commit();connection.close()
    def create_database(self):
        connection,access = Facebook.open_sql(self)
        access.execute('''CREATE TABLE Sigup (Name string, Bio string, City string, Current City string, Work string, Username string, Pin string, Login string)''')
        access.execute('''CREATE TABLE request(Username string, request string )''')
        access.execute('''CREATE TABLE Friends(Username string, friends string )''')
        access.execute('''CREATE TABLE Notifications(Username string, notifications string, new string )''')
        access.execute('''CREATE TABLE Messeges(Username string, sender string, messege string, reply string)''')
        access.execute('''CREATE TABLE Block(Username string, blocked string)''')
        access.execute('''CREATE TABLE R_posts(Username string,sender string,post string)''')
        access.execute('''CREATE TABLE all_posts(Username string,P_N string,post string,commonts string,private string,blocked list)''')
        access.execute('''CREATE TABLE R_comments(Username string,post string, comment string)''')
        access.execute('''CREATE TABLE all_pages(name string,owner string,likes string)''')
        access.execute('''CREATE TABLE liked_pages(Username string, page string)''')
        access.execute('''CREATE TABLE R_page_posts(Username string, receiver string ,page string,post string)''')
        access.execute('''CREATE TABLE all_page_posts(Username string,page string,post string,comments string)''')
        access.execute('''CREATE TABLE R_page_comments(Username string,sender string,post string, comment string,page string)''')
        Facebook.close_sql(self,connection)
    def signup(self,root,info):
        connection,access = Facebook.open_sql(self)
        col_name,header,all_users = Facebook.data_manager(self)
        if info[5] in all_users:
            messagebox.showerror('Error','Username already taken.')
            root.destroy()
            return 1
        access.execute('INSERT INTO Sigup VALUES(?,?,?,?,?,?,?,?)',info); Facebook.close_sql(self,connection)
        root.destroy();messagebox.showinfo('','Account Created.')
    def login(self,username,pin,root):
        connection,access = Facebook.open_sql(self)
        access.execute('SELECT * FROM Sigup WHERE Username = ?',(username,)); user_info = access.fetchall()
        if len(user_info) > 0:
            if str(user_info[0][6]) == pin:
                if str(user_info[0][7]) == 'Yes':
                    root.destroy();GUI.home(self,username)
                else:
                    access.execute("""UPDATE 'Sigup' SET Login = 'Yes' WHERE Username = ?""",(username,))
                    Facebook.close_sql(self,connection)
                    root.destroy();GUI.home(self,username)
            else:
                messagebox.showerror('Error','Wrong Username or Pin.')
        else:
            messagebox.showerror('Error','Wrong Username or Pin.')
    def logout(self,root):
        connection = sqlite3.connect('Facebook.db'); access = connection.cursor()
        access.execute("""UPDATE 'Sigup' SET Login = 'No'""")
        Facebook.close_sql(self,connection);root.destroy();GUI.login_signup(self)
    def data_manager(self):
        connection,access = Facebook.open_sql(self)
        col_name = ['Username','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] 
        header = ['Name','Bio','City','Current City','Work','Username','Pin','Login']
        access.execute('SELECT Username FROM Sigup'); all = access.fetchall(); all_users = []
        for x in all:
            all_users.append(x[0])
        return col_name,header,all_users
class manage_friends:
    def send_request(self,username,receiver,root):
        connection,access = Facebook.open_sql(self)
        col_name,header,all_users = Facebook.data_manager(self); all_users.remove(username)
        access.execute('SELECT request FROM request WHERE Username = ? AND request = ?',(username,receiver,)); requests = access.fetchall()
        access.execute('SELECT request FROM request WHERE Username = ? AND request = ?',(receiver,username)); sent = access.fetchall()
        if len(requests) == 0 and len(sent) == 0:
            access.execute("""INSERT INTO Request VALUES(?,?)""",(receiver,username)); print('Request sent.\n')
            messagebox.showinfo('','Request Sent')
        elif len(sent) != 0:
            messagebox.showinfo('','You have already sent\nThis user a friend request.')
        else:
            messagebox.showinfo('','This user has already \nsent you a friend request')
        Facebook.close_sql(self,connection);root.destroy()
    def __delete_request(self,root,username,request):
        connection,access = Facebook.open_sql(self);r = 1;c= 0 
        access.execute("DELETE FROM Request WHERE request = ? AND Username = ?",(request,username,))
        Facebook.close_sql(self,connection)
    def __accept_helper(self,username,request):
        connection,access = Facebook.open_sql(self);r = 1;c= 0 
        access.execute("""INSERT INTO Friends VALUES(?,?)""",(username,request,))
        access.execute("""INSERT INTO Friends VALUES(?,?)""",(request,username,))
        access.execute("""INSERT INTO Notifications VALUES(?,?,?)""",(request,'1',username))
        access.execute("DELETE FROM Request WHERE request = ? AND Username = ?",(request,username,))
        Facebook.close_sql(self,connection)
    def accept_requests(self,root,username,noti = 0):
        connection,access = Facebook.open_sql(self);r = 1;c= 0 
        access.execute("SELECT request FROM Request WHERE Username = ?",(username,)); lst = access.fetchall()
        Facebook.close_sql(self,connection)
        if noti != 0:
            return int(len(lst))
        if len(lst) != 0:
            for a in lst:
                request ='From: '+ a[0] 
                GUI.create_label(root,request,r,c)
                customtkinter.CTkButton(master=root, text="Accept", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:manage_friends.__accept_helper(self,username,a[0])).grid(row=r, column=c+1)
                customtkinter.CTkButton(master=root, text="Delete", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:manage_friends.__delete_request(self,root,username,a[0])).grid(row=r, column=c+2)
                r += 1
            customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.D_CR_R_M(self,root,username)).grid(row=r, column=c+1)
        else:
            messagebox.showinfo('','No Requests Received');root.destroy();GUI.home(self,username)      
    def all_friends(self,username):
        connection,access = Facebook.open_sql(self)
        access.execute("SELECT friends FROM Friends WHERE Username = ?",(username,)); lst = access.fetchall(); friend_list = []
        for a in lst:
            friend_list.append(a[0])
        return friend_list
class post_comment:
    def my_posts(self,username,root):
        customtkinter.CTkLabel(root, text = 'My Posts',text_color="green",text_font=('BOLD',12),width=100, height=30,corner_radius=20,fg_color=("gray70", "gray25")).grid(row=1, column=3, padx=20, pady=20)
        connection,access = Facebook.open_sql(self);counter = 0; column = 1;row = 1;comments1 = []
        access.execute("SELECT P_N,post,commonts FROM all_posts WHERE Username = ?",(username,)); lst = access.fetchall()
        for a in lst:
            post = 'Post '+str(a[0])+' : '+ a[1]
            comments = a[2].split('::')
            comment = ''
            for x in comments:
                comment = comment +'\n'+ x.split(':')[0]+' Commented  : '+x.split(':')[1]
            post = post+comment
            GUI.create_label(root,post,row+1,column);counter += 1 ; row += 1
        Facebook.close_sql(self,connection)          
    def post(self,root,root1,username,post,private,hide):
        hide = hide.split(',')
        connection = sqlite3.connect('Facebook.db'); access = connection.cursor()
        blocked = FB_setting.blocked_users('as',username) ; friend_list = manage_friends.all_friends(self,username)
        blo = ''
        if private != 1:
            blocked = blocked + hide
        if username in blocked:
            messagebox.showerror('Error',"You can't hide post from yourself")
        access.execute("SELECT P_N FROM all_posts WHERE Username = ?",(username,)); lst = access.fetchall()
        if len(lst) != 0:
            last_P_N = len(lst)+1
        else: 
            last_P_N = 1
        for block in blocked:
            blo = str(blo)+ str(':') + str(block)
        connection = sqlite3.connect('Facebook.db'); access = connection.cursor()
        access.execute('''INSERT INTO all_posts Values(?,?,?,?,?,?)''',(username,last_P_N,post,'',private,blo))
        if private != 1:
            for receiver in friend_list:
                if receiver not in blocked:
                    access.execute('''INSERT INTO R_posts Values(?,?,?)''',(receiver,username,post))
        Facebook.close_sql(self,connection);messagebox.showinfo('','Your post has been successfully uploaded.')
        root.destroy();root1.destroy();GUI.home(self,username)
    def check_post(self,root,username,a,noti = 0):
        connection,access = Facebook.open_sql(self);row1 = 1; column1 = 1
        access.execute('SELECT sender,post FROM R_posts WHERE Username = ?',(username,));lst = access.fetchall() 
        Facebook.close_sql(self,connection)
        if noti != 0:
            return int(len(lst))
        if len(lst) == 0:
            GUI.create_label(root,'No new Posts',row1,column1)
            customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command= lambda:GUI.D_CR_R_M(self,root,username)).grid(row=row1+1, column=2, padx=20, pady=20)
            Facebook.close_sql(self,connection)
        else:
            post = 'From: '+str(lst[a][0])+'\nPost: ' + str(lst[a][1])
            GUI.create_label(root,post,row1,column1)
            comment = customtkinter.CTkEntry(master=root, placeholder_text='Comment')
            comment.grid(row=row1+1, column=1, padx=20, pady=20)
            customtkinter.CTkButton(master=root, text="Comment", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command= lambda:post_comment.comment(self,root,username,comment.get(),a,lst,lst[a][1])).grid(row=row1+1, column=2, padx=20, pady=20)
    def comment(self,root,username,comment,a,lst,post):
        connection,access = Facebook.open_sql(self)
        access.execute("SELECT commonts FROM all_posts WHERE Username  = ? AND post = ? ",(lst[a][0],post)); O_comment = access.fetchall()[0][0]
        if O_comment != '':
            comment1 = O_comment + '::' +username+':'+ comment
        else:
            comment1 = username + ':' + comment
        access.execute("""UPDATE 'all_posts' SET commonts = ? WHERE Username  = ? AND post = ? """,(comment1,lst[a][0],post))
        access.execute('INSERT INTO R_comments VALUES(?,?,?,?)',(lst[a][0],username,post,str(comment)))
        Facebook.close_sql(self,connection);a += 1
        if a > len(lst)-1:
            connection,access = Facebook.open_sql(self)
            for x in range(len(lst)):
                access.execute("DELETE FROM R_posts WHERE Username  = ? AND sender = ? AND post = ?",(username,lst[x][0],lst[x][1]))
            Facebook.close_sql(self,connection)
            root.destroy();GUI.home(self,username)
        else:
            post_comment.check_post(self,root,username,a,0)
    def check_comment(self,root,username,noti = 0):
        connection,access = Facebook.open_sql(self);r = 0
        access.execute('SELECT post,sender,comment FROM R_comments WHERE Username = ?',(username,));comments = access.fetchall() 
        if noti != 0:
            return int(len(comments))
        if len(comments) != 0:
            for a in range(len(comments)):
                post = comments[a][0];sender = comments[a][1]; comment =comments[a][2]
                x = 'On posts: '+ post + '\nFrom: '+ sender+ '\nComment: '+comment
                GUI.create_label(root,x,r,0);r +=1
                access.execute("DELETE FROM R_comments WHERE Username  = ? AND sender = ? AND post = ? AND comment = ?",(username,sender,post,comment))
        else:
            GUI.create_label(root,'No new Comments',3,3)
        customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                    corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                    command= lambda:GUI.D_CR_R_M(self,root,username)).grid(row=r, column=2, padx=20, pady=20)
        Facebook.close_sql(self,connection)    
class messenger:
    def send_message(self,username,receiver,messege,root1,root):
        connection,access = Facebook.open_sql(self); col_name,header,all_users = Facebook.data_manager(self)
        blocked = FB_setting.blocked_users('as',username)
        # friend_list = manage_friends.all_friends(self,username)
        if receiver not in all_users or receiver == username or receiver in blocked:
            messagebox.showerror("Error","No User Found.")  
        else:
            access.execute('''INSERT INTO Messeges Values(?,?,?)''',(receiver,username,messege,))
            Facebook.close_sql(self,connection);messagebox.showinfo('','Messenge Sent')
            root.destroy();GUI.home(self,username)
    def check_messege(self,username,a,noti = 0):
        connection,access = Facebook.open_sql(self)
        access.execute("SELECT sender,messege FROM Messeges WHERE Username = ?",(username,)); lst = access.fetchall()
        Facebook.close_sql(self,connection)
        if noti != 0:
            return int(len(lst))
        if len(lst) != 0:
            root = GUI.create_window(self,'300x200','New Messeges')
            if len(lst[a][1].split(':'))  == 1:
                messege = 'From: '+str(lst[a][0])+'\nMessege: ' + str(lst[a][1])
            else:
                messege = 'From: '+str(lst[a][0])+'\nReply: ' + str(lst[a][1].split(':')[0]) + '\nOn Messege: '+ str(lst[a][1].split(':')[1])
            GUI.create_label(root,messege,0,0)
            reply = customtkinter.CTkEntry(master=root, placeholder_text='Reply')
            reply.grid(row=1, column=0, padx=20, pady=20)
            customtkinter.CTkButton(master=root, text="Reply", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command= lambda:messenger.reply(self,root,username,reply.get(),a,lst)).grid(row=1, column=1, padx=20, pady=20)
            root.mainloop()
        else:
            messagebox.showinfo('','No New Messges')
    def reply(self,root,username,reply,a,lst):
        connection,access = Facebook.open_sql(self)
        if reply != '':
            if len(lst[a][1].split(':')) == 1:
                messege = reply+':'+ str(lst[a][1])
            else:
                messege = reply +':'+ str(lst[a][1].split(':')[1])
            access.execute('''INSERT INTO Messeges Values(?,?,?)''',(lst[a][0],username,messege))
        Facebook.close_sql(self,connection);a += 1
        if a > len(lst)-1:
            connection,access = Facebook.open_sql(self)
            for x in range(len(lst)):
                access.execute('DELETE FROM Messeges WHERE Username = ? AND sender = ? AND messege = ?',(username,lst[x][0],lst[x][1],))
            Facebook.close_sql(self,connection)
            root.destroy()
        else:
            root.destroy();messenger.check_messege(self,username,a)  
class FB_setting:
    def update_info(self,username,Category,New_info):
        connection,access = Facebook.open_sql(self); col_name,header,all_users = Facebook.data_manager(self); header1 = header.copy(); conter = 3
        while conter > 0:
            header1.pop(len(header1)-1); conter -=1
        if Category in header1:
            access.execute("""UPDATE 'Sigup' SET """+str(Category)+""" = ? WHERE Username = ?""",(New_info,username,))
            Facebook.close_sql(self,connection); messagebox.showinfo('','Category updated.')
        else:
            messagebox.showerror('Error','No Category with is name\nthat you can update.')
    def block(self,username,block):
        blocked = FB_setting.blocked_users('as',username)
        connection,access = Facebook.open_sql(self)
        col_name,header,all_users = Facebook.data_manager(self)
        if block not in all_users or block == username:
            messagebox.showerror('Error','User not available.')
        elif block in blocked:
            messagebox.showerror('Error','User Already Blocked.')
        else:
            access.execute("""INSERT INTO Block VALUES(?,?)""",(username,block))
            messagebox.showinfo('','User Blocked')
        Facebook.close_sql(self,connection)
    def unblock(self,username,unblock):
        connection,access = Facebook.open_sql(self); blocked = FB_setting.blocked_users('as',username)
        if unblock not in blocked:
            messagebox.showerror('Error','The given user is not blocked.') 
        else:
            access.execute("DELETE FROM Block WHERE blocked = ?",(unblock,))
            Facebook.close_sql(self,connection);messagebox.showinfo('','User Unblocked')
    def blocked_users(self,username,b = 0):
        connection,access = Facebook.open_sql(self);r = 0;c = 0
        access.execute("SELECT blocked FROM Block WHERE Username = ?",(username,)); lst = access.fetchall(); blocked = []
        for a in lst:
            blocked.append(a[0]) 
        Facebook.close_sql(self,connection)
        if b == 0:
            return blocked
        else:
            if len(blocked) == 0:
                root = GUI.create_window(self,"200x100",'Blocked')
                customtkinter.CTkLabel(root,text='No User Blocked').grid(row = r,column = c)
                customtkinter.CTkLabel(root,text='').grid(row = r+1,column = c)
            else:
                root = GUI.create_window(self,"400x400",'Blocked')
                for x in blocked:
                    customtkinter.CTkLabel(root,text=x).grid(row = r,column = c);r += 1
            customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:root.destroy()).grid(row=r+1, column=c)
            root.mainloop()
class FB_search:    
    def search(self,username,Find):
        connection,access = Facebook.open_sql(self); lst = [0,1,2,4];r = 0
        col_name,header,all_users = Facebook.data_manager(self)
        friend_list = manage_friends.all_friends(self,username)
        if Find not in all_users or Find == username:
            messagebox.showerror('Error','No User Found')
        else:
            blocked = FB_setting.blocked_users('as',Find)
            if username in blocked:
                messagebox.showerror('Error','No User Found')
            else:
                access.execute('SELECT * FROM Sigup WHERE Username = ?',(Find,))
                user_info = list(access.fetchall()[0]); all_users.remove(username)
                root = GUI.create_window(self,"400x300",'User Found')
                for i in lst:
                    x = header[i]+'  :  '+user_info[i]
                    customtkinter.CTkLabel(root,text=x,text_font = ('ITALIC',15)).grid(row = r,column = 0);r += 1
                customtkinter.CTkButton(master=root, text="Posts", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:FB_search.show_post(self,username,Find,root)).grid(row=r +1 , column=0)
            if Find in friend_list:
                    customtkinter.CTkLabel(root,text='You are friends.',text_font = ('ITALIC',15)).grid(row = r,column = 0);r += 1
            else:
                customtkinter.CTkButton(master=root, text="Send Request", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:manage_friends.send_request(self,username,Find,root)).grid(row=r, column=0)    
            customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:root.destroy()).grid(row=r + 2, column=0)
                
            root.mainloop()       
        Facebook.close_sql(self,connection)  
    def search_post(self,root1,username,query):
        query = str('"')+ query+ str('%')+ str('"');r =0
        connection,access = Facebook.open_sql(self)
        access.execute("SELECT Username,post,private,blocked FROM all_posts WHERE post LIKE " + str(query))
        lst = access.fetchall()
        if len(lst) == 0:
            messagebox.showinfo('','No Post Found.')
        else:
            root = GUI.create_window(self,"700x500",'User Found')
            count = 1
            for a in range(len(lst)):
                if 0 in lst[a]:
                    if username not in lst[a][3].split(':'):
                        x = '\nPost'+str(count)+'from: '+lst[a][0]+'\nPost: '+lst[a][1];count += 1
                        customtkinter.CTkLabel(root,text=x).grid(row = r,column = 0);r += 1
            customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:root.destroy()).grid(row=r, column=2)
            root.mainloop()
        Facebook.close_sql(self,connection)   
    def show_post(self,username,Find,root1):
        root1.destroy()
        connection,access = Facebook.open_sql(self);r = 0
        access.execute('SELECT post,blocked FROM all_posts WHERE Username = ? AND private = ?',(Find,0,));posts = access.fetchall()
        if len(posts) == 0:
            messagebox.showinfo('','No posts available from this user.')
        else:
            root = GUI.create_window(self,"700x500",'User Found');count = 1
            for a in range(len(posts)):
                if username not in posts[a][1].split(':'):
                    x = '\nPost'+str(count)+'from: '+posts[a][0]+'\nPost: '+posts[a][1];count += 1
                    customtkinter.CTkLabel(root,text=x).grid(row = r,column = 0);r += 1
            customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:root.destroy()).grid(row=r, column=2)
            root.mainloop()
        Facebook.close_sql(self,connection)
class pages:
    def create_page(self,username,name):
        connection,access = Facebook.open_sql(self)
        access.execute('SELECT name FROM all_pages');all_pages = access.fetchall();run = 0
        for page in all_pages:
            if name in all_pages[0]:
                run = 1
        if run == 0:
            access.execute('INSERT INTO all_pages VALUES(?,?,?)',(name,username,'0',))
            messagebox.showinfo('','Page Created')
        else:
            messagebox.showerror('Error','Name already taken.') 
        Facebook.close_sql(self,connection);pages.like_page(self,username,name) 
    def like_page(self,username,name):
        connection,access = Facebook.open_sql(self);liked = True
        access.execute('SELECT owner,name,likes FROM all_pages Where name = ?',(name,)); lst = access.fetchall()
        access.execute('SELECT page FROM liked_pages WHERE Username = ?',(username,)); liked_pages = access.fetchall()
        if len(lst) == 0:
            messagebox.showerror('Error','No page with this name exists.')
        else:
            for x in liked_pages:
                if name in x[0]:
                    messagebox.showinfo('','Page Aleady Liked');return 1
        likes = lst[0][2] + 1
        access.execute("""UPDATE 'all_pages' SET likes = ? WHERE name = ? AND owner = ?""",(likes,name,lst[0][0],))
        access.execute('INSERT INTO liked_pages VALUES(?,?)',(username,name));Facebook.close_sql(self,connection)
        messagebox.showinfo('','Page Liked.')
    def del_page(self,username,name):
        connection,access = Facebook.open_sql(self)
        access.execute('SELECT owner,name FROM all_pages WHERE owner =? AND name = ?',(username,name)); lst = access.fetchall()
        if len(lst) != 0:
            access.execute("DELETE FROM all_pages WHERE name = ? AND owner = ? ",(name,username,))
            access.execute("DELETE FROM liked_pages WHERE page = ?",(name,))
            messagebox.showinfo('','Page Deleted')
        else:
            messagebox.showerror('','No page with this \nname is owned by you\nOnly page owners can delete their pages.')
        Facebook.close_sql(self,connection)
    def post(self,username,name,post):
        connection,access = Facebook.open_sql(self)
        access.execute('SELECT page FROM liked_pages WHERE Username = ? AND page = ?',(username,name,)); liked = access.fetchall()
        access.execute('SELECT Username FROM liked_pages WHERE page = ?',(name,)) ;receivers = access.fetchall()
        if len(liked) != 0:
            for receiver in receivers:
                if receiver[0] != username:
                    access.execute('INSERT INTO R_page_posts VALUES(?,?,?,?)',(username,receiver[0],name,post,))
            access.execute('INSERT INTO all_page_posts VALUES(?,?,?,?)',(username,name,post,''))
            messagebox.showinfo('','Post Uploaded.')
        else:
            messagebox.showerror('Error','No page with this \nname is liked by you.')
        Facebook.close_sql(self,connection)
    def check_post(self,username,a,noti = 0):
        root = GUI.create_window(self,'300x200','New Posts')
        connection,access = Facebook.open_sql(self)
        access.execute('SELECT page FROM liked_pages WHERE Username = ?',(username,)); liked_pages = access.fetchall()
        all_posts = [];P_Ns = 0; row1 = 0; column1 = 0;lst = []
        for page in liked_pages:
            access.execute('SELECT Username,post,page FROM R_page_posts WHERE page = ? AND receiver = ?',(page[0],username,)); posts = access.fetchall()
            if len(posts) != 0:
                all_posts.append(posts)   
        Facebook.close_sql(self,connection)
        for p in all_posts:
                    for post in p:
                        P_Ns += 1
        if noti != 0:
            return P_Ns
        for x in all_posts:
            for y in x:
                lst.append(y)
        if len(lst) != 0:
            post = 'From: '+str(lst[a][0])+'\nPost: ' + str(lst[a][1]) +'\nOn page: '+str(lst[a][2])
            GUI.create_label(root,post,row1,column1)
            comment = customtkinter.CTkEntry(master=root, placeholder_text='Comment')
            comment.grid(row=row1+1, column=0, padx=20, pady=20)
            customtkinter.CTkButton(master=root, text="Comment", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command= lambda:pages.comment(self,root,username,comment.get(),a,lst,lst[a][1],lst[a][2])).grid(row=row1+1, column=1, padx=20, pady=20)
            root.mainloop()
        else:
            messagebox.showinfo('','No Recent Posts') 
    def comment(self,root,username,comment,a,lst,post,page):
        connection,access = Facebook.open_sql(self)
        access.execute("SELECT comments FROM all_page_posts WHERE Username  = ? AND post = ? AND page = ?",(lst[a][0],post,page)); O_comment = access.fetchall()[0][0]
        if O_comment != '':
            comment1 = O_comment + '::' +username+':'+ comment
        else:
            comment1 = username + ':' + comment
        if comment != '':
            access.execute("""UPDATE 'all_page_posts' SET comments = ? WHERE Username  = ? AND post = ? AND page = ?""",(comment1,lst[a][0],post,page))
            access.execute('INSERT INTO R_page_comments VALUES(?,?,?,?,?)',(lst[a][0],username,post,str(comment),page))
        Facebook.close_sql(self,connection);a += 1
        if a > len(lst)-1:
            connection,access = Facebook.open_sql(self)
            for x in range(len(lst)):
                access.execute("DELETE FROM R_page_posts WHERE receiver  = ? AND post = ? AND page = ?",(username,lst[x][1],lst[x][2]))
            Facebook.close_sql(self,connection)
            root.destroy()
        else:
            root.destroy();pages.check_post(self,username,a,0)  
    def check_comment(self,username,noti = 0):
        root = GUI.create_window(self,'500x700','New Posts')
        connection,access = Facebook.open_sql(self);r = 0
        access.execute('SELECT post,sender,comment,page FROM R_page_comments WHERE Username = ?',(username,));comments = access.fetchall() 
        if noti != 0:
            return int(len(comments))
        if len(comments) != 0:
            for a in range(len(comments)):
                post = comments[a][0];sender = comments[a][1]; comment =comments[a][2]
                x = 'On Posts : '+ post+'\nFrom Page :'+comments[a][3] + '\nFrom : '+ sender+ '\nComment : '+comment
                GUI.create_label(root,x,r,0);r +=1
                access.execute("DELETE FROM R_page_comments WHERE Username  = ? AND sender = ? AND post = ? AND comment = ? AND page = ?",(username,sender,post,comment,comments[a][3]))
            customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:root.destroy()).grid(row=r, column=3)
        else:
            messagebox.showinfo('','No New Comments');root.destroy()
        root.mainloop()
        Facebook.close_sql(self,connection)    
    def my_posts(self,username):
        root = GUI.create_window(self,'700x500','My Posts')
        customtkinter.CTkLabel(root, text = 'My Posts',text_color="green",text_font=('BOLD',12),width=100, height=30,corner_radius=20,fg_color=("gray70", "gray25")).grid(row=1, column=3, padx=20, pady=20)
        connection,access = Facebook.open_sql(self);counter = 0; column1 = 1;row1 = 1;comments1 = [];posts = []
        access.execute("SELECT post,comments,page FROM all_page_posts WHERE Username = ?",(username,)); lst = access.fetchall()
        for a in lst:
            post = 'On Post : '+a[0]+'\nFrom Page: '+a[2]
            comments = a[1].split('::')
            comment = ''
            for x in comments:
                comment = comment +'\n'+ x.split(':')[0]+' Commented  : '+x.split(':')[1]
            post = post+comment
            GUI.create_label(root,post,row1+1,column1);counter += 1 ; row1 += 1  
        customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:root.destroy()).grid(row=row1+1, column=3)
        root.mainloop()
        Facebook.close_sql(self,connection)          
    def show_page(self,username,page,a):
        connection,access = Facebook.open_sql(self)
        access.execute("SELECT post,comments,Username FROM all_page_posts WHERE page = ?",(page,)); lst = access.fetchall()
        if len(lst) != 0:
            post = 'From : '+lst[a][2]+'\nPost : '+lst[a][0]
            comments = lst[a][1].split('::')
            comment = ''
            for x in comments:
                comment = comment +'\n'+ x.split(':')[0]+' Commented  : '+x.split(':')[1]
            post = post+comment
            root = GUI.create_window(self,'400x300',page)
            GUI.create_label(root,post,0,0)
            N_comment = customtkinter.CTkEntry(master=root, placeholder_text='Comment')
            N_comment.grid(row=1, column=0, padx=20, pady=20)
            customtkinter.CTkButton(master=root, text="Comment", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command= lambda:pages.P_comment(self,root,username,N_comment.get(),a,lst,lst[a][0],page)).grid(row=1, column=1, padx=20, pady=20)
            customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command= lambda:root.destroy()).grid(row=2, column=1, padx=20, pady=20)
            root.mainloop()
        else:
            messagebox.showerror('Error',"Page doesn't exist")
        Facebook.close_sql(self,connection)
    def P_comment(self,root,username,comment,a,lst,post,page):
        connection,access = Facebook.open_sql(self)
        access.execute("SELECT comments FROM all_page_posts WHERE Username  = ? AND post = ? AND page = ?",(lst[a][2],post,page)); O_comment = access.fetchall()[0][0]
        if O_comment != '':
            comment1 = O_comment + '::' +username+':'+ comment
        else:
            comment1 = username + ':' + comment
        if comment != '':
            access.execute("""UPDATE 'all_page_posts' SET comments = ? WHERE Username  = ? AND post = ? AND page = ?""",(comment1,lst[a][2],post,page))
            access.execute('INSERT INTO R_page_comments VALUES(?,?,?,?,?)',(lst[a][2],username,post,str(comment),page))
        Facebook.close_sql(self,connection) ;a -= 1
        if a == -1:
            root.destroy()
        else:
            root.destroy()
            pages.show_page(self,username,page,a)
class notifications:
    def notification(self,root,username):
        connection,access = Facebook.open_sql(self)
        access.execute('SELECT * FROM Notifications WHERE Username = ?',(username,));R_A_L = access.fetchall()
        request_accepted = 0
        for x in R_A_L:
            access.execute('DELETE FROM Notifications WHERE Username = ? AND new = ?',(str(x[0]),str(x[2])))
            request_accepted += int(x[1]) 
        requests = manage_friends.accept_requests(self,root,username,1)
        posts = post_comment.check_post(self,root,username,0,1)
        comments = post_comment.check_comment(self,root,username,1)
        page_comments = pages.check_comment(self,username,1)
        page_posts = pages.check_post(self,username,0,1)
        messeges = messenger.check_messege(self,username,0,1);row  = 2
        total = str(requests+posts+comments+messeges+request_accepted+page_comments+page_posts)+' new notifocations.'
        customtkinter.CTkLabel(root, text = total,text_color="green",text_font=('BOLD',12),width=100, height=30,corner_radius=20,fg_color=("gray70", "gray25")).grid(row=1, column=0, padx=20, pady=20)          
        if requests+posts+comments+messeges+request_accepted != 0:
            lst = [requests,request_accepted,posts,comments,messeges,page_posts,page_comments]
            lst1 = [' New Requests',' Request Accepted',' New Posts',' New Comments',' New Messeges',' New post on\nliked page,','New comment on\npost from page.']
            for a in range(len(lst)):
                if lst[a] != 0:
                    GUI.create_label(root,str(lst[a])+lst1[a],row,0);row += 1  
        Facebook.close_sql(self,connection)
class GUI:
    def __init__(self):
        self.IF = 'Shazam'
    def create_window(self,size,name):
        customtkinter.set_appearance_mode("System")  
        customtkinter.set_default_color_theme("blue")
        root = customtkinter.CTk()
        root.geometry(size)
        root.title(name)
        return root
    def create_frame(self,root):
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1, minsize=200)
        frame = customtkinter.CTkFrame(master=root, width=250, height=240, corner_radius=15)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, minsize=10)
        return frame
    def entry(self,label,frame):
        name = customtkinter.CTkEntry(master=frame, placeholder_text=label)
        name.pack();return name 
    def create_label(root,name,r,c):
        customtkinter.CTkLabel(root, text = name,text_font = ('ITALIC',12),text_color= ('lightblue')).grid(row=r, column=c, padx=20, pady=20)
    def login_signup(self):
        PATH = os.path.dirname(os.path.realpath(__file__))
        root = GUI.create_window(self,"450x260",'Facebook')
        image_size = 20
        add_user_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/add-user.png").resize((image_size, image_size), Image.ANTIALIAS))
        login_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/login.png").resize((image_size, image_size), Image.ANTIALIAS))
        frame = GUI.create_frame(self,root)
        customtkinter.CTkLabel(frame, text = "Welcome to Facebook",text_font = ('BOLD',13),text_color= ('lightblue')).pack()
        customtkinter.CTkLabel(frame, text = "By Shazam Razzaq").pack()
        username = GUI.entry(self,'Username',frame)
        pin = GUI.entry(self,'Pin',frame)
        customtkinter.CTkButton(master=root, image = login_image, text="Login", width=130, height=70, border_width=3,
                                        corner_radius=10, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:Facebook.login(self,username.get(),pin.get(),root)).place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)
        customtkinter.CTkButton(master=root, image=add_user_image, text="Create Account", width=130, height=70, border_width=3,
                                        corner_radius=10, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.signup(self)).grid(row=0, column=1, padx=20, pady=20)
        root.mainloop()
    def signup(self):
        root = GUI.create_window(self,"300x400",'Sign_up')
        frame = GUI.create_frame(self,root)
        customtkinter.CTkLabel(frame, text = "Enter Info").pack()
        name = GUI.entry(self,'Your Name:',frame)
        bio = GUI.entry(self,'Create Bio:',frame)
        hometown = GUI.entry(self,'Enter Hometown:',frame)
        current_city = GUI.entry(self,'Enter Current City:',frame)
        work = GUI.entry(self,'Work:',frame)
        username = GUI.entry(self,'Create Username:',frame)
        pin = GUI.entry(self,'Craete Pin',frame)
        customtkinter.CTkButton(master=root,text="Sign_up", width=130, height=70, border_width=3,
                                        corner_radius=10, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:Facebook.signup(self,root,[name.get(),bio.get(),hometown.get(),current_city.get(),work.get(),username.get(),pin.get(),'NO'])).place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        root.mainloop()
    def post(self,root1,username):
        root = GUI.create_window(self,"500x400",'New Post')
        frame = GUI.create_frame(self,root)
        post = GUI.entry(self,'Whats on you mind:',frame)
        private = customtkinter.CTkCheckBox(master = frame ,text ='Would You like to make this post private?' ,hover_color="#C77C78",border_color='gray25',border_width=1,corner_radius=2)
        private.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        hide = GUI.entry(self,'Hide Post From:',frame)
        customtkinter.CTkButton(master=root, text="Upload", width=70, height=40, border_width=3,
                                corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                command=lambda:post_comment.post(self,root,root1,username,post.get(),private.get(),hide.get())).grid(row=0, column=3, padx=20, pady=20)
        root.mainloop()
    def check_posts(self,root1,username):
        root1.destroy()
        root = GUI.create_window(self,"300x200",'New Posts')
        post_comment.check_post(self,root,username,0,0)
        root.mainloop()
    def D_CR_R_M(self,root,username):
        root.destroy()
        GUI.home(self,username)
    def messenger(self,root1,username):
        root1.destroy()
        root = GUI.create_window(self,"500x450",'Messenger')
        GUI.create_label(root,'Welocme to messenger',0,1)
        receiver = customtkinter.CTkEntry(master = root, placeholder_text='Receiver')
        receiver.grid(row=1, column=1, padx=20, pady=20)
        messege = customtkinter.CTkEntry(master = root, placeholder_text='Messege')
        messege.grid(row=2, column=1, padx=20, pady=20)
        customtkinter.CTkButton(master=root, text="Send Messege", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:messenger.send_message(self,username,receiver.get(),messege.get(),root1,root)).grid(row=3, column=1, padx=20, pady=20)
        customtkinter.CTkButton(master=root, text="Check and reply messeges", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:messenger.check_messege(self,username,0)).grid(row=4, column=1, padx=20, pady=20)
        customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.D_CR_R_M(self,root,username)).grid(row=5, column=0, padx=20, pady=20)
        root.mainloop()
    def check_comments(self,root1,username):
        root1.destroy()
        root = GUI.create_window(self,"500x400",'Comments')
        post_comment.check_comment(self,root,username)
        root.mainloop()
    def setting(self,root1,username):
        root1.destroy()
        root = GUI.create_window(self,"700x250",'Setting');r = 0;c = 0
        lst = ['Update Info','Block','Unblock']
        for a in lst:
            GUI.create_label(root,a,r,c);c += 1
        Category = customtkinter.CTkEntry(master = root, placeholder_text='Category')
        Category.grid(row = 1,column = 0)
        New_info = customtkinter.CTkEntry(master = root, placeholder_text='New Info')
        New_info.grid(row = 2,column = 0)
        customtkinter.CTkButton(master=root, text="Update", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:FB_setting.update_info(self,username,Category.get(),New_info.get())).grid(row=3, column=0)
        customtkinter.CTkLabel(root,text='').grid(row = 2,column = 1)
        block = customtkinter.CTkEntry(master = root, placeholder_text='Username')
        block.grid(row = 1,column = 1)
        customtkinter.CTkButton(master=root, text="Block", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:FB_setting.block(self,username,block.get())).grid(row=3, column=1)
        customtkinter.CTkLabel(root,text='').grid(row = 2,column = 2)
        unblock = customtkinter.CTkEntry(master = root, placeholder_text='Username')
        unblock.grid(row = 1,column = 2)
        customtkinter.CTkButton(master=root, text="Unblock", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:FB_setting.unblock(self,username,unblock.get())).grid(row=3, column=2)
        customtkinter.CTkLabel(root,text='').grid(row = 0,column = 3)
        customtkinter.CTkLabel(root,text='').grid(row = 2,column = 3)
        customtkinter.CTkButton(master=root, text="Blocked Users", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:FB_setting.blocked_users(self,username,1)).grid(row=1, column=3)
        customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.D_CR_R_M(self,root,username)).grid(row=3, column=3)
        root.mainloop()
    def search(self,root1,username):
        root1.destroy()
        root = GUI.create_window(self,"500x200",'Search');r = 0;c = 0
        lst = ['search User','Search Post']
        for a in lst:
            GUI.create_label(root,a,r,c);c += 1
        Find = customtkinter.CTkEntry(master = root, placeholder_text='Username')
        Find.grid(row = 1,column = 0)
        customtkinter.CTkButton(master=root, text="Find", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:FB_search.search(self,username,Find.get())).grid(row=3, column=0)
        query = customtkinter.CTkEntry(master = root, placeholder_text='Query')
        query.grid(row = 1,column = 1)
        customtkinter.CTkButton(master=root, text="Find", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:FB_search.search_post(self,root,username,query.get())).grid(row=3, column=1)
        customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.D_CR_R_M(self,root,username)).grid(row=0, column=3)
        root.mainloop()
    def friend_requests(self,root1,username):
        root1.destroy()
        root = GUI.create_window(self,"500x600",'Requests Received')
        manage_friends.accept_requests(self,root,username)
        root.mainloop()
    def pages(self,root1,username):
        root1.destroy()
        root = GUI.create_window(self,"1620x1350",'Pages');c = 0
        labels = ['Create Page','Delete Page','Like Page','Post on Page','Recent Posts','Visit Page']
        for title in labels:
            GUI.create_label(root,title,0,c);c += 1    
        name = customtkinter.CTkEntry(master = root, placeholder_text='Page Name')
        name.grid(row = 1 ,column = 2)
        p_post = customtkinter.CTkEntry(master = root, placeholder_text='Post')
        p_post.grid(row = 1 ,column = 3)
        customtkinter.CTkButton(master=root, text="Create", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:pages.create_page(self,username,name.get())).grid(row=2, column=0)
        customtkinter.CTkButton(master=root, text="Delete", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:pages.del_page(self,username,name.get())).grid(row=2, column=1)
        customtkinter.CTkButton(master=root, text="Like", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:pages.like_page(self,username,name.get())).grid(row=2, column=2)
        customtkinter.CTkButton(master=root, text="Post", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:pages.post(self,username,name.get(),p_post.get())).grid(row=2, column=3)
        customtkinter.CTkButton(master=root, text="View", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:pages.check_post(self,username,0)).grid(row=2, column=4)
        connection,access = Facebook.open_sql(self)
        access.execute("SELECT post,comments,Username FROM all_page_posts WHERE page = ?",(name.get(),)); lst = access.fetchall()
        Facebook.close_sql(self,connection);a = len(lst) - 1
        customtkinter.CTkButton(master=root, text="Visit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:pages.show_page(self,username,name.get(),a)).grid(row=2, column=5)
        GUI.create_label(root,'',3,3);GUI.create_label(root,'',3,3)
        GUI.create_label(root,'Comments',4,2);GUI.create_label(root,'My posts',4,3)
        customtkinter.CTkButton(master=root, text="View", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:pages.check_comment(self,username,0)).grid(row=5, column=2)
        customtkinter.CTkButton(master=root, text="View", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:pages.my_posts('self','shazam')).grid(row=5, column=3)
        customtkinter.CTkButton(master=root, text="Exit", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.D_CR_R_M(self,root,username)).grid(row=6, column=7)
        root.mainloop()
    def home(self,username):
        root = GUI.create_window(self,"1620x1350",'Home')
        customtkinter.CTkButton(master=root, text="Post", width=70, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.post(self,root,username)).grid(row=0, column=0)
        customtkinter.CTkButton(master=root, text="Recent Posts", width=50, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.friend_requests(self,root,username)).grid(row=0, column=1)
        customtkinter.CTkButton(master=root, text="Recent Comments", width=50, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.check_comments(self,root,username)).grid(row=0, column=2)
        customtkinter.CTkButton(master=root, text="Friend Request", width=50, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.friend_requests(self,root,username)).grid(row=0, column=3)
        customtkinter.CTkButton(master=root, text="Messenger",width=50, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.messenger(self,root,username)).grid(row=0, column=4)
        customtkinter.CTkButton(master=root, text="Pages",width=50, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.pages(self,root,username)).grid(row=0, column=5)
        customtkinter.CTkButton(master=root, text="Setting", width=50, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.setting(self,root,username)).grid(row=0, column=6)
        customtkinter.CTkButton(master=root, text="Search", width=50, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:GUI.search(self,root,username)).grid(row=0, column=7)
        customtkinter.CTkButton(master=root, text="Log-out", width=50, height=40, border_width=3,
                                        corner_radius=7, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=lambda:Facebook.logout(self,root)).grid(row=0, column=8)
        post_comment.my_posts(self,username,root)
        notifications.notification(self,root,username)
        root.mainloop()
facebook = GUI()
facebook.login_signup()