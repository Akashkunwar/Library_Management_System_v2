from app import db
import datetime
# Define your SQLAlchemy models here

class User(db.Model):
    __tablename__ = 'user'
    UserId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UserName = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(40), nullable=False)
    Role = db.Column(db.String(20), nullable=False)
    # Content = db.Column(db.Text)
    Name = db.Column(db.Text)
    Email = db.Column(db.Text)
    Department = db.Column(db.Text)
    Description = db.Column(db.Text)
    Phone_No = db.Column(db.Text)
    DOB = db.Column(db.Text)
    Gender = db.Column(db.Text)
    Education = db.Column(db.Text)
    Job = db.Column(db.Text)
    City = db.Column(db.Text)
    Linkedin = db.Column(db.Text)
    Favourate_Books = db.Column(db.Text)

class Section(db.Model):
    __tablename__ = 'section'
    SectionId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Title = db.Column(db.String(50), nullable=False)
    CreatedDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    Description = db.Column(db.Text, nullable=False)
    ImageLink = db.Column(db.String(255))

class Books(db.Model):
    __tablename__ = 'books'
    BookId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    SectionId = db.Column(db.Integer, db.ForeignKey('section.SectionId'), nullable=False)
    Title = db.Column(db.String(50), nullable=False)
    Author = db.Column(db.String(50), nullable=False)
    Content = db.Column(db.Text)
    ImageLink = db.Column(db.String(255))

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
    Rating = db.Column(db.Text)
    Review = db.Column(db.Text)

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
