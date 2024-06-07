# from crypt import methods
import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from sqlalchemy import func, and_
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.secret_key = 'B00KL1BRARYS4S7EM'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"library.db")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

api = Api(app)

# For Graphs to not show old one
def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

file_paths = ["static\Graphs\graph1.png","static\Graphs\graph2.png","static\Graphs\graph3.png","static\Graphs\graph4.png",]
for file in file_paths:
    delete_file_if_exists(file)


class User(db.Model):
    __tablename__ = 'user'
    UserId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UserName = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(40), nullable=False)
    Role = db.Column(db.String(20), nullable=False)

user_parser = reqparse.RequestParser()
user_parser.add_argument('UserName', type=str, required=True, help='UserName is required')
user_parser.add_argument('Password', type=str, required=True, help='Password is required')
user_parser.add_argument('Role', type=str, required=True, help='Role is required')

class UserAPI(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                user_data = {
                    'UserId' : user.UserId,
                    'UserName' : user.UserName,
                    'Password' : user.Password,
                    'Role' : user.Role
                }
                return user_data, 200
            else:
                return "User not found", 404
        else:
            users = User.query.all()
            users_data = []
            for user in users:
                user_data = {
                    'UserId' : user.UserId,
                    'UserName' : user.UserName,
                    'Password' : user.Password,
                    'Role' : user.Role
                }
                users_data.append(user_data)
            return users_data, 200
            
    def post(self):
        args = user_parser.parse_args()
        new_user = User(
            UserName=args['UserName'],
            Password=args['Password'],
            Role=args['Role']
        )
        db.session.add(new_user)
        db.session.commit()
        return "User added successfully", 201
    
    def put(self, user_id):
        args = user_parser.parse_args()
        user = User.query.get(user_id)
        if user:
            user.UserName = args['UserName']    
            user.Password = args['Password']    
            user.Role = args['Role']
            db.session.commit()
            return f"User with {user_id} updated successfully" , 200
        else:
            return f"User with {user_id} not found", 404  

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return f"User with ID {user_id} Deleted", 200
        else:
            return f"User with id {user_id} not found", 400

api.add_resource(UserAPI, "/API/Users", "/API/Users/<int:user_id>")


class Section(db.Model):
    __tablename__ = 'section'
    SectionId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Title = db.Column(db.String(50), nullable=False)
    CreatedDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    Description = db.Column(db.Text, nullable=False)
    ImageLink = db.Column(db.String(255))

section_parser = reqparse.RequestParser()
section_parser.add_argument('Title', type=str, required=True, help='Title is required')
section_parser.add_argument('Description', type=str, required=True, help='Description is required')
section_parser.add_argument('ImageLink', type=str)

class SectionAPI(Resource):
    def get(self, section_id=None):
        if section_id:
            section = Section.query.get(section_id)
            if section:
                section_data = {
                    'SectionId': section.SectionId,
                    'Title': section.Title,
                    'CreatedDate': section.CreatedDate.strftime('%Y-%m-%d %H:%M:%S'),
                    'Description': section.Description,
                    'ImageLink': section.ImageLink
                }
                return section_data, 200
            else:
                return "Section not found", 404
        else:
            sections = Section.query.all()
            sections_data = []
            for section in sections:
                section_data = {
                    'SectionId': section.SectionId,
                    'Title': section.Title,
                    'CreatedDate': section.CreatedDate.strftime('%Y-%m-%d %H:%M:%S'),
                    'Description': section.Description,
                    'ImageLink': section.ImageLink
                }
                sections_data.append(section_data)
            return sections_data, 200
    
    def post(self):
        args = section_parser.parse_args()
        new_section = Section(
            Title=args['Title'],
            Description=args['Description'],
            ImageLink=args['ImageLink']
        )
        db.session.add(new_section)
        db.session.commit()
        return "Section added successfully", 201
    
    def put(self, section_id):
        args = section_parser.parse_args()
        section = Section.query.get(section_id)
        if section:
            section.Title = args['Title']
            section.Description = args['Description']
            section.ImageLink = args['ImageLink']
            db.session.commit()
            return f"Section with ID {section_id} updated successfully", 200
        else:
            return f"Section with ID {section_id} not found", 404
    
    def delete(self, section_id):
        section = Section.query.get(section_id)
        if section:
            db.session.delete(section)
            db.session.commit()
            return f"Section with ID {section_id} deleted successfully", 200
        else:
            return f"Section with ID {section_id} not found", 404

api.add_resource(SectionAPI, "/API/Sections", "/API/Sections/<int:section_id>")

class Books(db.Model):
    __tablename__ = 'books'
    BookId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    SectionId = db.Column(db.Integer, db.ForeignKey('section.SectionId'), nullable=False)
    Title = db.Column(db.String(50), nullable=False)
    Author = db.Column(db.String(50), nullable=False)
    Content = db.Column(db.Text)
    ImageLink = db.Column(db.String(255))

book_parser = reqparse.RequestParser()
book_parser.add_argument('SectionId', type=int, required=True,help="SectionID is required")
book_parser.add_argument('Title', type=str, required=True,help="Title is required")
book_parser.add_argument('Author', type=str, required=True,help="Author is required")
book_parser.add_argument('Content', type=str)
book_parser.add_argument('ImageLink', type=str)

class BooksAPI(Resource):
    def get(self, book_id=None):
        if book_id:
            book = Books.query.get(book_id)
            if book:
                book_data = {
                    "BookId" : book.BookId,
                    "SectionId" : book.SectionId,
                    "Title" : book.Title,
                    "Author" : book.Author,
                    "Content": book.Content,
                    "ImageLink":book.ImageLink
                }
                return book_data, 200
            else:
                return f"No Book with {book_id} found", 400
        else:
            books = Books.query.all()
            books_data = []
            for book in books:
                book_data = {
                    "BookId" : book.BookId,
                    "SectionId" : book.SectionId,
                    "Title" : book.Title,
                    "Author" : book.Author,
                    "Content": book.Content,
                    "ImageLink":book.ImageLink
                }
                books_data.append(book_data)
            return books_data, 200
        
    def post(self):
        args = book_parser.parse_args()
        new_section = Books(
            SectionId = args['SectionId'],
            Title = args['Title'],
            Author = args['Author'],
            Content = args['Content'],
            ImageLink = args['ImageLink']
        )
        db.session.add(new_section)
        db.session.commit()
        return "Book added successfully", 200

    def put(self, book_id):
        args = book_parser.parse_args()
        book = Books.query.get(book_id)
        if book:
            book.SectionId = args['SectionId']
            book.Title = args['Title']
            book.Author = args['Author']
            book.Content = args['Content']
            book.ImageLink = args['ImageLink']
            db.session.commit()
            return f"Book data updated for {book_id}", 200
        else:
            return f"Book for ID {book_id} not found", 400
    
    def delete(self, book_id):
        book = Books.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return f"Book for ID {book_id} deleted", 200
        else:
            return f"No book with {book_id} found", 400

api.add_resource(BooksAPI,"/API/Books", "/API/Books/<int:book_id>")

class BookIssue(db.Model):
    __tablename__ = 'BookIssue'
    IssueId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey(User.UserId), nullable=False)
    BookId = db.Column(db.Integer, db.ForeignKey(Books.BookId), nullable=False)
    SectionId = db.Column(db.Integer, db.ForeignKey(Section.SectionId), nullable=False)
    RequestDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    Days = db.Column(db.Integer, nullable=False)
    IssueDate = db.Column(db.String)
    IssueStatus = db.Column(db.String, nullable=False)
    LastIssueStatusDate = db.Column(db.String)
    
BookIssue_parser = reqparse.RequestParser()
BookIssue_parser.add_argument('UserId', type=int, required=True, help='UserId is required')
BookIssue_parser.add_argument('BookId', type=int, required=True, help='BookId is required')
BookIssue_parser.add_argument('SectionId', type=int, required=True, help='SectionId is required')
BookIssue_parser.add_argument('Days', type=int, required=True, help='Days is required')
BookIssue_parser.add_argument('IssueDate', type=str)
BookIssue_parser.add_argument('IssueStatus', type=str, required=True, help='IssueStatus is required')
BookIssue_parser.add_argument('LastIssueStatusDate', type=str)

class BookIssueApi(Resource):
    def get(self, issue_id=None):
        if issue_id:
            issue = BookIssue.query.get(issue_id)
            if issue:
                issue_data = {
                    "IssueId" : issue.IssueId,
                    "UserId" : issue.UserId,
                    "BookId" : issue.BookId,
                    "SectionId" : issue.SectionId,
                    "RequestDate" : issue.RequestDate.strftime('%Y-%m-%d %H:%M:%S'),
                    "Days" : issue.Days,
                    "IssueDate" : issue.IssueDate,
                    "IssueStatus" : issue.IssueStatus,
                    "LastIssueStatusDate" : issue.LastIssueStatusDate,
                }
                return issue_data, 200
            else:
                return f"No issue with {issue_id}"
        else:
            issues = BookIssue.query.all()
            issues_data = []
            for issue in issues:
                issue_data = {
                "IssueId" : issue.IssueId,
                "UserId" : issue.UserId,
                "BookId" : issue.BookId,
                "SectionId" : issue.SectionId,
                "RequestDate" : issue.RequestDate.strftime('%Y-%m-%d %H:%M:%S'),
                "Days" : issue.Days,
                "IssueDate" : issue.IssueDate,
                "IssueStatus" : issue.IssueStatus,
                "LastIssueStatusDate" : issue.LastIssueStatusDate,
                }
                issues_data.append(issue_data)
            return issues_data, 200
    
    def post(self):
        args = BookIssue_parser.parse_args()
        new_issue = BookIssue(
            UserId = args["UserId"],
            BookId = args["BookId"],
            SectionId = args["SectionId"],
            Days = args["Days"],
            IssueDate = args["IssueDate"],
            IssueStatus = args["IssueStatus"],
            LastIssueStatusDate = args["LastIssueStatusDate"]
        )
        db.session.add(new_issue)
        db.session.commit()
        return "Book added successfully", 200
    
    def put(self, issue_id):
        args = BookIssue_parser.parse_args()
        issue = BookIssue.query.get(issue_id)
        if issue:
            issue.UserId = args["UserId"]
            issue.BookId = args["BookId"]
            issue.SectionId = args["SectionId"]
            issue.Days = args["Days"]
            issue.IssueDate = args["IssueDate"]
            issue.IssueStatus = args["IssueStatus"]
            issue.LastIssueStatusDate = args["LastIssueStatusDate"]
            db.session.commit()
            return f"Book Issue Updated for {issue_id}"
        else:
            return f"No Issue found with {issue_id}"
    
    def delete(self, issue_id):
        issue = BookIssue.query.get(issue_id)
        if issue:
            db.session.delete(issue)
            db.session.commit()
            return f"Issue deleted with ID {issue_id}",200
        else:
            return f"No issue found with {issue_id}",400

api.add_resource(BookIssueApi,"/API/BookIssue","/API/BookIssue/<int:issue_id>")

class BookIssueMerge(db.Model):
    __tablename__ = 'book_issue_merge'
    IssueId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey(User.UserId), nullable=False)
    BookId = db.Column(db.Integer, db.ForeignKey(Books.BookId), nullable=False)
    SectionId = db.Column(db.Integer, db.ForeignKey(Section.SectionId), nullable=False)
    RequestDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    Days = db.Column(db.Integer, nullable=False)
    IssueDate = db.Column(db.String)
    IssueStatus = db.Column(db.String, nullable=False)
    LastIssueStatusDate = db.Column(db.String)
    Book_Title = db.Column(db.String(50), nullable=False)
    Author = db.Column(db.String(50), nullable=False)
    UserName = db.Column(db.String(20), unique=True, nullable=False)
    Section_Title = db.Column(db.String(50), nullable=False)
    Book_Link = db.Column(db.String(50), nullable=False)

class BookSection(db.Model):
    __tablename__ = 'book_section'
    Books_BookId = db.Column(db.Integer, primary_key=True, nullable=False)
    Section_SectionId = db.Column(db.Integer, db.ForeignKey(Section.SectionId), nullable=False)
    Section_Title = db.Column(db.String(50), nullable=False)
    Section_CreatedDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    Section_Description = db.Column(db.Text, nullable=False)
    Section_ImageLink = db.Column(db.String(255))
    Books_Title = db.Column(db.String(50), nullable=False)
    Books_Author = db.Column(db.String(50), nullable=False)
    Books_Content = db.Column(db.Text)
    Books_ImageLink = db.Column(db.String(255))

# Expire if date passed
def update_issue_status():
    with app.app_context():
        today = datetime.date.today().strftime('%Y-%m-%d')
        book_issues_to_update = BookIssue.query.filter(BookIssue.IssueStatus == 'Approved', BookIssue.IssueDate < today).all()
        for book_issue in book_issues_to_update:
            book_issue.IssueStatus = 'Rejected'
        db.session.commit()

update_issue_status()

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
            return render_template("user-login.html", error="User already registered please login!")
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
        file_path = os.path.join("books", new_filename)
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
@app.route("/updateSections/<int:SectionId>", methods=["GET", "POST"])
def updateSections(SectionId):
    book = Section.query.get(SectionId)
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
        books = Section.query.all()
        return render_template("showBooks.html", books=books)

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
    plt.savefig('static/Graphs/graph1.png')

    use, counts = zip(*user_type)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=use, y=counts, hue=use, palette="viridis")
    sns.despine()
    plt.xlabel('Role', fontsize=12)
    plt.ylabel('Count', fontsize=12)

    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

    plt.savefig('static/Graphs/graph2.png')

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

        plt.savefig('static/Graphs/graph3.png')
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

    plt.savefig('static/Graphs/graph4.png')

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
        plt.savefig('static/Graphs/graph1.png')
    
        sections, counts = zip(*requestStatus)
        plt.figure(figsize=(8, 6))
        sns.barplot(x=sections, y=counts, hue=sections, palette="viridis")
        sns.despine()
        plt.xlabel('Issue Status', fontsize=12)
        plt.ylabel('Count', fontsize=12)

        for i, count in enumerate(counts):
            plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

        plt.savefig('static/Graphs/graph2.png')
        
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

    plt.savefig('static/Graphs/graph3.png')

    Sections = db.session.query(BookSection.Section_Title, func.count()).group_by(BookSection.Section_Title).order_by(func.count().desc()).all()

    sections, counts = zip(*Sections)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sections, y=counts, hue=sections, palette="viridis")
    sns.despine()
    plt.xlabel('Section', fontsize=12)
    plt.ylabel('Count', fontsize=12)

    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10)

    plt.savefig('static/Graphs/graph4.png')
    return render_template("adminStats.html", header = "header.html", Graph1 = "My request Status Pie", Graph2 = "My request Status Bar", Graph3 = "Books & Section Counts", Graph4 = "Section-wise Book Count")

@app.route('/download-book/<path:filename>')
def download_book(filename):
    pdf_path = os.path.join("books", filename)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)