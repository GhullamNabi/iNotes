from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from fpdf import FPDF

app = Flask(__name__)

# Set up the database connection using SQLite
DATABASE_URL = 'sqlite:///note.db'
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Define the Notes model
class Notes(Base):
    __tablename__ = 'notes'
    
    sno = Column(Integer, primary_key=True)
    question = Column(String(200), nullable=False)
    answer = Column(String(100000), nullable=False)
    important = Column(Boolean, default=False, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    important_text = Column(String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.question}"

# Create tables in the database if they don't exist
Base.metadata.create_all(engine)

# Set up session maker
Session = sessionmaker(bind=engine)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    session = Session()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        imp = 'imp' in request.form  # True if 'imp' checkbox is checked
        impt = request.form['impt']
        new_note = Notes(question=title, answer=desc, important=imp, important_text=impt)
        session.add(new_note)
        session.commit()
    notes = session.query(Notes).all()
    session.close()
    return render_template('index.html', allTodo=notes)

@app.route('/show')
def products():
    session = Session()
    all_todo = session.query(Notes).all()
    session.close()
    print(all_todo)
    return 'This is the products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    session = Session()
    todo = session.query(Notes).filter_by(sno=sno).first()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        imp = 'imp' in request.form
        impt = request.form['impt']
        todo.question = title
        todo.answer = desc
        todo.important = imp
        todo.important_text = impt
        session.commit()
        session.close()
        return redirect("/")
    session.close()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    session = Session()
    todo = session.query(Notes).filter_by(sno=sno).first()
    session.delete(todo)
    session.commit()
    session.close()
    return redirect("/")

@app.route('/dsn')
def dsn():
    session = Session()
    notes = session.query(Notes).all()
    content = ""
    for note in notes:
        if note.important:
            content += f"""
                                                              {note.question}
                    {note.important_text}
            """
    session.close()
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "iNotes Short Notes", 0, 1, "C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
    def create_pdf(filename):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        pdf.output(filename)
    create_pdf("static/iNotes SNotes.pdf")
    return render_template('dsn.html')

@app.route('/dln')
def dln():
    session = Session()
    notes = session.query(Notes).all()
    content = ""
    for note in notes:
        if note.important:
            content += f"""
                                                            {note.question}
                        {note.answer}
                                                            Important
                        {note.important_text}
            """
        else:
            content += f"""
                                                          {note.question}
                    {note.answer}
            """
    session.close()
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "iNotes Long Notes", 0, 1, "C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
    def create_pdf(filename):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        pdf.output(filename)
    create_pdf("static/iNotes LNotes.pdf")
    return render_template('dln.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
