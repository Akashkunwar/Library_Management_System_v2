from app import app, db
from flask import render_template, request, redirect, url_for, send_file, session, flash
from app.models import User, Section, Books, BookIssue, BookIssueMerge, BookSection
import seaborn as sns
import os
import datetime
from sqlalchemy import func, and_
import matplotlib.pyplot as plt

@app.route("/", methods = ["GET","POST"])
def home():
    return render_template("start.html")

@app.route("/user-login", methods = ["GET","POST"])
def userLogin():
    if 'user_id' in session:
        return redirect(url_for('allBooks', userid=session['user_id']))
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            user = User.query.filter_by(UserName=data['username']).first()
            if user:
                if user.Password == data["password"] and user.Role == 'user':
                    session['user_id'] = user.UserId
                    return redirect(url_for('myBooks'))
                else:
                    return render_template("user-login.html", error="Wrong Password")
            else:
                return render_template("user-login.html", error="No user with this Username")
        except:
            return render_template("user-login.html", error="No user with this Username")
    else:
        return render_template("user-login.html")

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return redirect(url_for('home'))
    elif 'admin_id' in session:
        session.pop('admin_id', None)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route("/register", methods = ["GET","POST"])
def userRegister():
    if 'user_id' in session:
        return redirect(url_for('myBooks'))
    if request.method =='POST':
        data = request.form.to_dict()
        user = User.query.filter_by(UserName=data['Username']).first()
        if user:
            return render_template("templates/user-login.html", error="User already registered please login!")
        else:
            user = User(UserName=data['Username'], Password=data['password'], Role='user')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('userLogin'))
    else:
        return render_template("user-register.html")

@app.route("/librarian-login", methods = ["GET","POST"])
def librarianLogin():
    if 'admin_id' in session:
        return redirect(url_for('requestedBooks'))
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            user = User.query.filter_by(UserName=data['username']).first()
            if user:
                if user.Password == data["password"]:
                    session['admin_id'] = user.UserId
                    return redirect(url_for('requestedBooks'))
                else:
                    return render_template("librarian-login.html", error="Wrong Password")
            else:
                return render_template("librarian-login.html", error="No user with this Username")
        except:
            return render_template("librarian-login.html", error="No user with this Username")
    else:
        return render_template("librarian-login.html")

@app.route("/add-section", methods = ["GET","POST"])
def addSection():
    if 'admin_id' not in session:
        return redirect(url_for('librarianLogin'))
    if request.method == 'POST':
        data = request.form.to_dict()
        section = Section(Title=data['section'], Description=data['text'])
        db.session.add(section)
        db.session.commit()
        section = Section.query.all()
        return render_template("add-section.html", section = section)
    else:
        section = Section.query.all()
        return render_template("add-section.html", section = section)

@app.route("/showBooks", methods = ["GET","POST"])
def showBooks():
    if 'admin_id' not in session:
        return redirect(url_for('librarianLogin'))
    if request.method == 'POST': 
        data = request.form.to_dict()
        f = request.files['file']
        new_filename = (data['Book-Title']+"_"+data['Author']+".pdf").replace(" ","_")
        file_path = os.path.join("app/books", new_filename)
        f.save(file_path) 
        books = Books(SectionId = data['book_section'],Title=data['Book-Title'],Author=data['Author'],Content=data['Content'], ImageLink=new_filename)
        db.session.add(books)
        db.session.commit()
        bookSec = BookSection.query.all()
        return render_template("showBooks.html", books=bookSec)
    else:
        bookSec = BookSection.query.all()
        return render_template("showBooks.html", books=bookSec)

@app.route("/deleteBook/<int:bookId>", methods=["GET", "POST"])
def deleteBook(bookId):
    book = Books.query.get(bookId)
    if book:
        file_path = os.path.join("books", book.ImageLink)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('showBooks'))

@app.route("/deleteSecion/<int:sectionId>", methods=["GET", "POST"])
def deleteSection(sectionId):
    section = Section.query.get(sectionId)
    if section:
        db.session.delete(section)
        db.session.commit()
    return redirect(url_for('addSection'))

@app.route("/updateBooks/<int:BooksId>", methods=["GET", "POST"])
def updateBooks(BooksId):
    book = Books.query.get(BooksId)
    if not book:
        return "Book not found", 404

    if request.method == 'POST':
        data = request.form.to_dict()
        book.Title = data['Title']
        book.Author = data['Author']
        book.Content = data['Content']

        db.session.commit()

        return redirect(url_for('showBooks'))
    else:
        books = Books.query.all()
        return render_template("showBooks.html", books=books)

@app.route("/allBooks", methods=["GET","POST"])
def allBooks():
    if 'user_id' not in session:
        return redirect(url_for('userLogin'))
    if request.method == 'POST':
        data = request.form.to_dict()
        requstBook = BookIssue(UserId=session['user_id'], BookId=data['bookid'], SectionId=data['sectionId'], Days=data['days'], IssueStatus = 'requested', IssueDate = datetime.datetime.today().date())
        db.session.add(requstBook)
        db.session.commit()

        bookSec = BookSection.query.all()
        userid = session['user_id']
        return render_template("allBooks.html", books=bookSec, userid = userid)
    else:
        bookSec = BookSection.query.all()
        userid = request.args.get('userid')
        return render_template("allBooks.html", books=bookSec, userid = userid)

@app.route("/myBooks", methods=["GET","POST"])
def myBooks():
    if 'user_id' not in session:
        return redirect(url_for('userLogin'))
    if request.method == "POST":
        data = request.form.to_dict()
        Issue_id = int(data["id"])
        Issue_status = data['status']

        book_issue = BookIssue.query.get(Issue_id)
        if book_issue:
            book_issue.IssueStatus = Issue_status
            db.session.commit()
            return redirect(url_for('myBooks'))

    BookIssueMergeTable = BookIssueMerge.query.filter(
        BookIssueMerge.UserId == session['user_id'],
        BookIssueMerge.Section_Title.isnot(None),
        BookIssueMerge.Author.isnot(None),
        BookIssueMerge.Book_Title.isnot(None),
        BookIssueMerge.IssueStatus == "requested",
        BookIssueMerge.UserName.isnot(None)).all()
    
    ApprovedBookIssueMergeTable = BookIssueMerge.query.filter(
        BookIssueMerge.UserId == session['user_id'],
        BookIssueMerge.Section_Title.isnot(None),
        BookIssueMerge.Author.isnot(None),
        BookIssueMerge.Book_Title.isnot(None),
        BookIssueMerge.IssueStatus == "Approved",
        BookIssueMerge.UserName.isnot(None)).all()
    
    RejectedBookIssueMergeTable = BookIssueMerge.query.filter(
        BookIssueMerge.UserId == session['user_id'],
        BookIssueMerge.Section_Title.isnot(None),
        BookIssueMerge.Author.isnot(None),
        BookIssueMerge.Book_Title.isnot(None),
        BookIssueMerge.IssueStatus == "Rejected",
        BookIssueMerge.UserName.isnot(None)).all()
    
    ExpiredBookIssueMergeTable = BookIssueMerge.query.filter(
        BookIssueMerge.UserId == session['user_id'],
        BookIssueMerge.Section_Title.isnot(None),
        BookIssueMerge.Author.isnot(None),
        BookIssueMerge.Book_Title.isnot(None),
        BookIssueMerge.IssueStatus == "Expired",
        BookIssueMerge.UserName.isnot(None)).all()
    
    return render_template("myBooks.html", approvedBooks = ApprovedBookIssueMergeTable, rejectedBooks = RejectedBookIssueMergeTable, issueBooks = BookIssueMergeTable,
    expiredBooks = ExpiredBookIssueMergeTable)

@app.route("/requestedBooks", methods=["GET","POST"])
def requestedBooks():
    if 'admin_id' not in session:
        return redirect(url_for('librarianLogin'))
    if request.method == "POST":
        data = request.form.to_dict()
        Issue_id = int(data["id"])
        Issue_status = data['status']

        book_issue = BookIssue.query.get(Issue_id)
        if book_issue:
            book_issue.IssueStatus = Issue_status
            db.session.commit()
            return redirect(url_for('requestedBooks'))
        

    BookIssueMergeTable = BookIssueMerge.query.filter(
        BookIssueMerge.Section_Title.isnot(None),
        BookIssueMerge.Author.isnot(None),
        BookIssueMerge.Book_Title.isnot(None),
        BookIssueMerge.IssueStatus == "requested",
        BookIssueMerge.UserName.isnot(None)).all()
    
    ApprovedBookIssueMergeTable = BookIssueMerge.query.filter(
        BookIssueMerge.Section_Title.isnot(None),
        BookIssueMerge.Author.isnot(None),
        BookIssueMerge.Book_Title.isnot(None),
        BookIssueMerge.IssueStatus == "Approved",
        BookIssueMerge.UserName.isnot(None)).all()
    
    RejectedBookIssueMergeTable = BookIssueMerge.query.filter(
        BookIssueMerge.Section_Title.isnot(None),
        BookIssueMerge.Author.isnot(None),
        BookIssueMerge.Book_Title.isnot(None),
        BookIssueMerge.IssueStatus == "Rejected",
        BookIssueMerge.UserName.isnot(None)).all()
    
    return render_template("requestBooks.html", books=BookIssueMergeTable, approvedBooks = ApprovedBookIssueMergeTable, rejectedBooks = RejectedBookIssueMergeTable)

@app.route("/adminStats", methods=["GET","POST"])
def adminStats():
    if 'admin_id' not in session:
        return redirect(url_for('librarianLogin'))
    # users = db.session.query(func.count()).filter(User.Role == "user").scalar()
    # admins = db.session.query(func.count()).filter(User.Role == "admin").scalar()
    user_type = db.session.query(User.Role, func.count()).group_by(User.Role).order_by(func.count().desc()).all()
    roles, counts = zip(*user_type)
    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=roles, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("bright"), textprops={'fontsize': 12})
    # plt.title('Distribution of Users by Role', fontsize=14)

    plt.axis('equal')
    plt.savefig('app/static/Graphs/graph1.png')


    use, counts = zip(*user_type)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=use, y=counts, hue=use, palette="viridis")
    sns.despine()
    plt.xlabel('Role', fontsize=12)
    plt.ylabel('Count', fontsize=12)

    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

    plt.savefig('app/static/Graphs/graph2.png')

    Issuestat = db.session.query(BookIssueMerge.IssueStatus, func.count()).group_by(BookIssueMerge.IssueStatus).order_by(func.count().desc()).all()
    try:
        issuemerge, counts = zip(*Issuestat)

        plt.figure(figsize=(8, 6))
        sns.barplot(x=issuemerge, y=counts, palette="viridis")
        sns.despine()
        plt.xlabel('Issue Status', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.title('Count of Books by Issue Status', fontsize=14)

        for i, count in enumerate(counts):
            plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

        plt.savefig('app/static/Graphs/graph3.png')
    except:
        pass
    
    Sections = db.session.query(BookSection.Section_Title, func.count()).group_by(BookSection.Section_Title).order_by(func.count().desc()).all()

    sections, counts = zip(*Sections)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sections, y=counts, hue=sections, palette="viridis")
    sns.despine()
    plt.xlabel('Section', fontsize=12)
    plt.ylabel('Count', fontsize=12)

    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

    plt.savefig('app/static/Graphs/graph4.png')

    return render_template("adminStats.html", header = "headerAdmin.html", Graph1 = "Admin & User Count Pie chart", Graph2 = "Admin & User Count Bar", Graph3 = "Books Request Status", Graph4 = "Section-wise Book Count")

@app.route("/userStats", methods=["GET","POST"])
def userStats():
    if 'user_id' not in session:
        return redirect(url_for('userLogin'))
    requestStatus = db.session.query(BookIssueMerge.IssueStatus, func.count()).filter(and_(BookIssueMerge.UserId == session['user_id'])).group_by(BookIssueMerge.IssueStatus).order_by(func.count().desc()).all()
    # user_type = db.session.query(User.Role, func.count()).group_by(User.Role).order_by(func.count().desc()).all()
    try:
        roles, counts = zip(*requestStatus)
        plt.figure(figsize=(8, 6))
        plt.pie(counts, labels=roles, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("bright"), textprops={'fontsize': 12})
        # plt.title('', fontsize=14)

        plt.axis('equal')
        plt.savefig('app/static/Graphs/graph1.png')
    
        sections, counts = zip(*requestStatus)
        plt.figure(figsize=(8, 6))
        sns.barplot(x=sections, y=counts, hue=sections, palette="viridis")
        sns.despine()
        plt.xlabel('Issue Status', fontsize=12)
        plt.ylabel('Count', fontsize=12)

        for i, count in enumerate(counts):
            plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

        plt.savefig('app/static/Graphs/graph2.png')
        
    except:
        pass

    buks = db.session.query(func.count(Books.BookId)).scalar()
    secs = db.session.query(func.count(Section.SectionId)).scalar()
    labels = ['Books', 'Sections']
    counts = [buks, secs]

    plt.figure(figsize=(8, 6))
    sns.barplot(x=labels, y=counts, palette='viridis')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    # plt.title('Number of Books and Sections', fontsize=14)

    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

    plt.savefig('app/static/Graphs/graph3.png')

    Sections = db.session.query(BookSection.Section_Title, func.count()).group_by(BookSection.Section_Title).order_by(func.count().desc()).all()

    sections, counts = zip(*Sections)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sections, y=counts, hue=sections, palette="viridis")
    sns.despine()
    plt.xlabel('Section', fontsize=12)
    plt.ylabel('Count', fontsize=12)

    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

    plt.savefig('app/static/Graphs/graph4.png')
    return render_template("adminStats.html", header = "header.html", Graph1 = "My request Status Pie", Graph2 = "My request Status Bar", Graph3 = "Books & Section Counts", Graph4 = "Section-wise Book Count")

@app.route('/download-book/<path:filename>')
def download_book(filename):
    pdf_path = os.path.join("books", filename)
    return send_file(pdf_path, as_attachment=True)