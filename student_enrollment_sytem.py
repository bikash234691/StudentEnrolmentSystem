import tkinter as tk
from tkinter import messagebox
from datetime import datetime


# ==================================================
# STUDENT CLASS
# ==================================================
class Student:
    def __init__(self, student_id, name, email):
        self.__student_id = student_id
        self.__name = name
        self.__email = email

    # Getters
    def get_id(self):
        return self.__student_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    # REQUIRED METHOD
    def display_student_info(self):
        return f"{self.__student_id} | {self.__name} | {self.__email}"


# ==================================================
# COURSE CLASS
# ==================================================
class Course:
    def __init__(self, code, name, capacity):
        self.__code = code
        self.__name = name
        self.__capacity = int(capacity)
        self.__students = []
        self.__waitlist = []

    def get_code(self):
        return self.__code

    def get_name(self):
        return self.__name

    def is_full(self):
        return len(self.__students) >= self.__capacity

    def add_student(self, student):
        if not self.is_full():
            self.__students.append(student)
            return "Enrolled"
        else:
            self.__waitlist.append(student)
            return "Waitlisted"

    # REQUIRED METHOD
    def display_course_details(self):
        return f"{self.__code} | {self.__name} | Capacity: {self.__capacity} | Enrolled: {len(self.__students)} | Waitlist: {len(self.__waitlist)}"


# ==================================================
# ENROLMENT CLASS
# ==================================================
class Enrolment:
    def __init__(self, student, course):
        self.student = student
        self.course = course
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = course.add_student(student)

    # REQUIRED METHOD
    def display_enrolment_details(self):
        return f"{self.student.get_name()} ({self.student.get_id()}) → {self.course.get_name()} | {self.status} | {self.date}"


# ==================================================
# GUI APPLICATION
# ==================================================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Enrolment System")
        self.root.geometry("700x550")

        self.students = []
        self.courses = []
        self.enrolments = []

        # ⭐ REQUIRED PRELOADED DATA (MAIN PROGRAM REQUIREMENT)
        self.load_sample_data()

        self.main_menu()

    # ================================
    # SAMPLE DATA (MEETS REQUIREMENT)
    # ================================
    def load_sample_data(self):
        self.students.append(Student("S101", "Alice", "alice@email.com"))
        self.students.append(Student("S102", "Bob", "bob@email.com"))

        self.courses.append(Course("CSE101", "Programming", 2))
        self.courses.append(Course("CSE102", "Data Structures", 1))

    # ================================
    # CLEAR SCREEN
    # ================================
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ================================
    # MAIN MENU (LANDING PAGE)
    # ================================
    def main_menu(self):
        self.clear()

        tk.Label(self.root, text="Student Enrolment System",
                 font=("Arial", 20, "bold")).pack(pady=25)

        tk.Button(self.root, text="Add Student", width=25,
                  command=self.add_student).pack(pady=8)

        tk.Button(self.root, text="Add Course", width=25,
                  command=self.add_course).pack(pady=8)

        tk.Button(self.root, text="Enrol Student", width=25,
                  command=self.enrol_screen).pack(pady=8)

        tk.Button(self.root, text="View All Data", width=25,
                  command=self.view_data).pack(pady=8)

    # ================================
    # ADD STUDENT
    # ================================
    def add_student(self):
        self.clear()

        tk.Label(self.root, text="Add Student", font=("Arial", 16)).pack(pady=10)

        sid = tk.Entry(self.root)
        name = tk.Entry(self.root)
        email = tk.Entry(self.root)

        tk.Label(self.root, text="Student ID").pack()
        sid.pack()

        tk.Label(self.root, text="Name").pack()
        name.pack()

        tk.Label(self.root, text="Email").pack()
        email.pack()

        def save():
            self.students.append(Student(sid.get(), name.get(), email.get()))
            messagebox.showinfo("Success", "Student Added Successfully")

        tk.Button(self.root, text="Save", command=save).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    # ================================
    # ADD COURSE
    # ================================
    def add_course(self):
        self.clear()

        tk.Label(self.root, text="Add Course", font=("Arial", 16)).pack(pady=10)

        code = tk.Entry(self.root)
        name = tk.Entry(self.root)
        cap = tk.Entry(self.root)

        tk.Label(self.root, text="Course Code").pack()
        code.pack()

        tk.Label(self.root, text="Course Name").pack()
        name.pack()

        tk.Label(self.root, text="Capacity").pack()
        cap.pack()

        def save():
            self.courses.append(Course(code.get(), name.get(), cap.get()))
            messagebox.showinfo("Success", "Course Added Successfully")

        tk.Button(self.root, text="Save", command=save).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    # ================================
    # ENROL SCREEN (DROPDOWN)
    # ================================
    def enrol_screen(self):
        self.clear()

        tk.Label(self.root, text="Enrol Student", font=("Arial", 16)).pack(pady=10)

        student_var = tk.StringVar()
        course_var = tk.StringVar()

        student_list = [f"{s.get_id()} - {s.get_name()}" for s in self.students]
        course_list = [f"{c.get_code()} - {c.get_name()}" for c in self.courses]

        student_var.set(student_list[0])
        course_var.set(course_list[0])

        tk.Label(self.root, text="Select Student").pack()
        tk.OptionMenu(self.root, student_var, *student_list).pack()

        tk.Label(self.root, text="Select Course").pack()
        tk.OptionMenu(self.root, course_var, *course_list).pack()

        def enrol():
            sid = student_var.get().split(" - ")[0]
            cid = course_var.get().split(" - ")[0]

            student = next(s for s in self.students if s.get_id() == sid)
            course = next(c for c in self.courses if c.get_code() == cid)

            enrolment = Enrolment(student, course)
            self.enrolments.append(enrolment)

            messagebox.showinfo(
                "Enrolment Result",
                f"{enrolment.display_enrolment_details()}"
            )

        tk.Button(self.root, text="Enrol", command=enrol).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    # ================================
    # VIEW DATA (ALL OUTPUT)
    # ================================
    def view_data(self):
        self.clear()

        tk.Label(self.root, text="System Data", font=("Arial", 16)).pack(pady=10)

        text = tk.Text(self.root, width=80, height=25)
        text.pack()

        text.insert(tk.END, "STUDENTS:\n")
        for s in self.students:
            text.insert(tk.END, s.display_student_info() + "\n")

        text.insert(tk.END, "\nCOURSES:\n")
        for c in self.courses:
            text.insert(tk.END, c.display_course_details() + "\n")

        text.insert(tk.END, "\nENROLMENTS:\n")
        for e in self.enrolments:
            text.insert(tk.END, e.display_enrolment_details() + "\n")

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)


# ==================================================
# RUN APPLICATION
# ==================================================
root = tk.Tk()
app = App(root)
root.mainloop()