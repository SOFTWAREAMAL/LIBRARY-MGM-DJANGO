from django.shortcuts import render, HttpResponse
from django.contrib import messages
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth import authenticate, login,logout
                               
from mysql.connector import *

mysql = connect(
    host = 'localhost',
    user = 'root',
    password = 'amalan',
    database = 'library_django'
)
cursor = mysql.cursor(dictionary = True)
print('MYSQL CONNECT - SUCCESS')

def login(request):
    if request.method == "POST":
        ad_name = request.POST.get("admin_name")
        ad_pw = request.POST.get("admin_password")
        if ad_name == 'admin' and ad_pw == '123':
            return render(request,'homepage.html')
        else:
            messages.error(request, 'Invalid user name or password')
            return render(request,'login.html')
    return render(request, 'login.html')  

def homepage(request):
    return render(request,'homepage.html')

def view_book_details(request):
    if request.method == "POST":
        ad_name = request.POST.get("admin_name")
        ad_pw = request.POST.get("admin_password")
        if ad_name == 'admin' and ad_pw == '123':
            cursor.execute('select * from library_books')
            r = cursor.fetchall()
            context = { 'r': r }
            print(context)
            return render(request,'viewloop.html',context)
        else:
            messages.error(request, 'Invalid user name or password')
            return render(request,'view_book_details.html')
    return render(request,'view_book_details.html')
 
def view_student_record(request):
    if request.method == "POST":
        ad_name = request.POST.get("admin_name")
        ad_pw = request.POST.get("admin_password")
        if ad_name == 'admin' and ad_pw == '123':
            cursor.execute('select * from student')
            r = cursor.fetchall()
            context = { 'r': r }
            print(context)
            return render(request,'view_student_loop.html',context)
        else:
            messages.error(request, 'Invalid user name or password')
            return render(request,'view_student_record.html')
    return render (request,'view_student_record.html')
    
def check_book_availability(request):
    if request.method == "POST":
        b_name = request.POST.get("book_name")
        ad_pw = request.POST.get("admin_password")
        
        if ad_pw == '123':
            with mysql.cursor() as cursor:
                cursor.execute('SELECT book_name FROM library_books WHERE book_name = %s', [b_name])
                r = cursor.fetchone()
                context = { 'r': r }
                print(context)
            if r :
                return HttpResponse(f"<h1>BOOK: '{b_name}' IS AVAILABLE!</h1>")
            else:
                
                return HttpResponse(f"<h1>SORRY, BOOK: '{b_name}' IS NOT AVAILABLE</h1>")    
        else:
            messages.error(request, 'Invalid admin password')
            return render(request, 'check_book_availability.html')
    return render (request,'check_book_availability.html')


def issue_book(request):
    if request.method == "POST":
        s_name = request.POST.get("student_name")
        is_dt = request.POST.get("issue_date")     
        b_name = request.POST.get("book_name")
        re_dt = request.POST.get("return_date")       
        ad_pw = request.POST.get("admin_password")           
        if ad_pw == '123':
            with mysql.cursor() as cursor:
                cursor.execute('SELECT book_name FROM library_books WHERE book_name = %s', [b_name])
                check = cursor.fetchone()
                context = { 'check': check }
                print(context)
            if check :
                with mysql.cursor() as cursor:  
                    insert = "INSERT INTO student(book_name,student_name,issue_date,return_date) values(%s,%s,%s,%s);"
                    cursor.execute(insert,[b_name,s_name,is_dt,re_dt])
                    result = cursor.fetchone()
                    print(result)
                    mysql.commit()
                    cursor.execute('DELETE FROM library_books where book_name = %s',[b_name])
                    mysql.commit()
                    return HttpResponse (f"<h1> BOOK: '{b_name}' issued to student ! </h1>" )
            else:
                return HttpResponse(f"<h1>SORRY, BOOK: '{b_name}' IS NOT AVAILABLE</h1>")  
        else:
            messages.error(request, 'Invalid admin password')
            return render(request,'issue.html')
    return render(request,'issue.html')

def return_book(request):
    if request.method == "POST":
        b_name = request.POST.get("book_name")
        ad_pw = request.POST.get("admin_password")     
        s_name = request.POST.get("student_name")
        re_dt = request.POST.get("return_date")
        s_re_dt = request.POST.get("student_return_date")   
        if ad_pw == '123':          
            with mysql.cursor() as cursor:   
                cursor.execute("update student set student_return_date = %s where book_name = %s and student_name = %s",[s_re_dt,b_name,s_name])
                insert = "insert into library_books (book_name) values(%s); "
                cursor.execute(insert,[b_name])
                mysql.commit()
                cursor.execute('select return_date from student where return_date > student_return_date and book_name = %s and student_name = %s',
                    [b_name,s_name])
                result = cursor.fetchone()
                print(result)
                if result:
                    return HttpResponse(f"<h1> BOOK: '{b_name}' , Student return the book successful! </h1>" )
                else:
                    return HttpResponse(f"<h1> Pay fine amount Rs.500 <h1>")
        else:
            messages.error(request, 'Invalid admin password')
            return render(request,'return_book.html')
    return render(request,'return_book.html')

# 
def fine(request):
    if request.method == "POST":
        s_name = request.POST.get("student_name")
        b_name = request.POST.get("book_name")    
        fine   = request.POST.get("fine")
        ad_pw  = request.POST.get("admin_password") 
        if ad_pw == '123': 
            if fine >= '500':          
                with mysql.cursor() as cursor:  
                    cursor.execute("update student set fine = %s where student_name = %s and book_name = %s",[fine,s_name,b_name])
                    mysql.commit()                
                    return HttpResponse(f"<h1> student : '{s_name}' , Successfully paid the Fine! </h1>" )
            else:
                return HttpResponse(f"<h1> student : '{s_name}' , 'Repay the Fine' <h1>")
        else:
            messages.error(request, 'Invalid admin password')
            return render(request,'fine.html')
    return render(request,'fine.html')
# 

def add_book(request):
    if request.method == "POST":
        b_name = request.POST.get("book_name")
        ad_pw = request.POST.get("admin_password")

        if ad_pw == '123':
            with mysql.cursor() as cursor:
                insert_query = "INSERT INTO library_books (book_name) VALUES (%s)"
                cursor.execute(insert_query, [b_name])
                mysql.commit()

                cursor.execute('SELECT book_name FROM library_books WHERE book_name = %s', [b_name])
                result = cursor.fetchone()

            if result:
                return HttpResponse(f"<h1>BOOK: {result} IS ADDED BY ADMIN!</h1>")
            else:
                return HttpResponse(f"<h1>SORRY, BOOK: {b_name} IS NOT ADDED</h1>")
        else:
            messages.error(request, 'Invalid admin password')
            return render(request, 'add_book.html')
    return render(request, 'add_book.html')

def logout(request):
    return render(request,'logout.html')


