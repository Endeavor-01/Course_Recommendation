from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import pandas as pd
from tkinter import ttk, filedialog
from tkinter import messagebox
import neattext.functions as nfx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dbSERVER import insert_user, check_user, username_exists
import webbrowser



class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Courses Suggestions")
        self.geometry("1000x1500")  # Set the window size
        self.configure(bg="#2C3E50")  # Set background color

        # Container to hold different pages
        self.container = tk.Frame(self, bg="#2C3E50")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.pages = {}  # Dictionary to hold pages
        
        # Add the pages
        self.add_page(HomePage)
        self.add_page(LoginPage)
        self.add_page(MainPage)
        self.add_page(RecommendPage)

        # Show the initial page
        self.show_page(HomePage)

    def add_page(self, page_class):
        page = page_class(self.container, self)
        self.pages[page_class] = page
        page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#CFB284")  # Set background color
        self.controller = controller

        # Heading
        heading_label = tk.Label(self, text="Welcome to Our Website", bg="#CFB284", fg="Black", font=("Helvetica", 24, "bold"))
        heading_label.pack(pady=40)

        # Image space
        try:
            image = Image.open("images/Keep it simple.png")  # Replace "your_image.png" with the path to your image
            image = image.resize((900, 200), Image.BILINEAR) # Resize image while maintaining quality
            self.image = ImageTk.PhotoImage(image)
            image_label = tk.Label(self, image=self.image, bg="#001427")
            image_label.pack(pady=20)  # Adjust padding to position the image
        except Exception as e:
            print("Error loading image:", e)

        # Paragraph space
        paragraph_frame = tk.Frame(self, bg="#CFB284")  # Create a frame for paragraph
        paragraph_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Define the paragraph text
        paragraph_text = ("Our web application, CourseGenie, is designed to assist students in making informed decisions "
                          "about their college courses. With CourseGenie, you can receive personalized course "
                          "recommendations based on your individual subjects data. Whether "
                          "you're aiming for a specific career path or simply exploring your options, CourseGenie "
                          "analyzes your academic performance and suggests courses that align with your interests and "
                          "capabilities. Say goodbye to uncertainty and let CourseGenie guide you toward a bright "
                          "academic future!")

        # Create a Message widget to display the paragraph text with word wrapping
        message = tk.Message(paragraph_frame, text=paragraph_text, bg="#CFB284", fg="black", font=("Helvetica", 12), justify="center", width=800)
        message.pack(padx=20, pady=20)

        button = tk.Button(self, text="Go to Login Page", command=lambda: controller.show_page(LoginPage), bg="black", fg="white", font=("Helvetica", 12, "bold"), width=20, height=2, bd=0)  # Set button colors and size
        button.pack(pady=200)# Adjust padding to position the button a little lower


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#CFB284")  # Set background color
        self.controller = controller
        self.parent = parent
        self.window = parent.winfo_toplevel()
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Login Page')

        # ============================background image============================

        self.bg_frame = Image.open('images/background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self, bg='#040405', width=1000, height=600)
        self.lgn_frame.place(x=230, y=130)
        # ========================================================================
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",fg='white',bd=5, relief=FLAT)
        self.heading.place(x=300, y=50, width=300, height=30)
        # ============ Left Side Image ==============================================
        self.side_image = Image.open('images/vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)
        # ============ Sign In Image =============================================
        self.sign_in_image = Image.open('images\\hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)
        # ============ Sign In label =============================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)      
        # ============================username====================================
       
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
      
        # ============================login button================================
        
        self.lgn_button = Image.open('images\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',
                            command=self.login_or_register)
        self.login.place(x=20, y=10)
 
        # ============================password====================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
     
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage \
            (file='images\\show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='images\\hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def login_or_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        if username_exists(username):
            if check_user(username, password):
                self.controller.show_page(MainPage)
            else:
                messagebox.showerror("Error", "Invalid password or user already exists")
        else:
            insert_user(username, password)
            messagebox.showinfo("Success", "User registered successfully!")
            self.controller.show_page(MainPage)    

    def switch_to_front_page(self):
        self.controller.show_page(HomePage)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

# ========= MAIN PAGE ==================================================================

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.uploaded_dataset = None  # To store the uploaded dataset

        # Split the page into left and right frames
        self.left_frame = tk.Frame(self, bg="#CFB284", width=250)
        self.left_frame.pack(side="left", fill="y", padx=(20, 10))

        self.right_frame = tk.Frame(self, bg="#CFB284", width=550)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 20))

        # Disable resizing for individual frames
        self.left_frame.pack_propagate(False)
        self.right_frame.pack_propagate(False)

        # Left frame components
        search_label = tk.Label(self.left_frame, text="Search", bg="#CFB284", fg="black", font=("Helvetica", 12))
        search_label.pack(pady=(20, 5))
        self.search_entry = tk.Entry(self.left_frame, font=("Helvetica", 12), width=20)
        self.search_entry.pack(pady=5)

        upload_button = tk.Button(self.left_frame, text="UPLOAD DATASET", command=self.upload_dataset, bg="black",
                                  fg="white", font=("Helvetica", 12, "bold"), width=20, height=2, bd=0)
        upload_button.pack(pady=20)

        recommend_button = tk.Button(self.left_frame, text="RECOMMEND", command=self.display_recommendations,
                                     bg="black", fg="white", font=("Helvetica", 12, "bold"), width=20, height=2, bd=0)
        recommend_button.pack(pady=20)

        quit_button = tk.Button(self.left_frame, text="QUIT", command=self.quit_application, bg="black", fg="white",
                                font=("Helvetica", 12, "bold"), width=20, height=2, bd=0)
        quit_button.pack(pady=20)

        # Right frame components
        self.dataset_label = tk.Label(self.right_frame, text="Uploaded Dataset", bg="#CFB284", fg="black",
                                       font=("Helvetica", 18,"bold"))
        self.dataset_label.pack(pady=20)
        self.dataset_text = tk.Text(self.right_frame, height=50, width=150)
        self.dataset_text.pack(pady=(0, 20))

    def quit_application(self):
        self.controller.quit()

    def upload_dataset(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Read the dataset and display it
            self.uploaded_dataset = pd.read_csv(file_path)
            self.display_uploaded_dataset()

    def display_uploaded_dataset(self):
        if self.uploaded_dataset is not None:
            self.dataset_text.delete(1.0, tk.END)
            
            # Calculate the maximum width of each column
            col_widths = [max(len(str(val)) for val in self.uploaded_dataset[col]) for col in self.uploaded_dataset.columns]
            col_names = self.uploaded_dataset.columns.tolist()
            header_widths = [len(col) for col in col_names]
            col_widths = [max(col_width, header_width) for col_width, header_width in zip(col_widths, header_widths)]
            
            # Create header string with alignment
            header_str = "    ".join([f"{col:<{col_widths[i]}}" for i, col in enumerate(col_names)]) + "\n"
            header_str += "-" * (sum(col_widths) + (len(col_widths) - 1) * 4) + "\n"
            
            # Create row strings with alignment
            rows_str = "\n".join(["    ".join([f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row)]) for row in self.uploaded_dataset.itertuples(index=False)])
            
            dataset_str = header_str + rows_str
            
            self.dataset_text.insert(tk.END, dataset_str)

    def display_recommendations(self):
        query = self.search_entry.get()
        if query and self.uploaded_dataset is not None:
            # Pass the query to the RecommendPage instance
            recommend_page_instance = self.controller.pages[RecommendPage]
            recommend_page_instance.set_query(query)
            self.controller.show_page(RecommendPage)
        else:
            messagebox.showinfo("Missing Query or Dataset", "Please enter a search query and upload a dataset.")




class RecommendPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#CFB284")
        self.controller = controller
        self.query = None
        self.main_page_instance = controller.pages[MainPage]
        self.url_dict = {}  # Dictionary to store URLs

        # Heading
        heading_label = tk.Label(self, text="Recommendations", bg="#CFB284", fg="black", font=("Helvetica", 30, "bold"))
        heading_label.pack(pady=20)

        # Initialize Treeview to display recommendations
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 14), rowheight=25, background="#CFB284", foreground="black")
        style.configure("Treeview.Heading", font=("Helvetica", 16, "bold"), background="#CFB284", foreground="black")
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove borders
        style.map('Treeview', background=[('selected', '#CFB284')], foreground=[('selected', 'black')])

        columns = ("course_title", "content_duration", "price", "url")
        self.recommendations_treeview = ttk.Treeview(self, columns=columns, show="headings", height=20)
        self.recommendations_treeview.heading("course_title", text="Course Title")
        self.recommendations_treeview.heading("content_duration", text="Duration")
        self.recommendations_treeview.heading("price", text="Price")
        self.recommendations_treeview.heading("url", text="URL")
        self.recommendations_treeview.column("course_title", width=400)
        self.recommendations_treeview.column("content_duration", width=150)
        self.recommendations_treeview.column("price", width=100)
        self.recommendations_treeview.column("url", width=300)
        
        self.recommendations_treeview.pack(pady=(0, 20), padx=50, fill="both", expand=True)
        self.recommendations_treeview.tag_configure('evenrow', background="#D3D3D3")
        self.recommendations_treeview.tag_configure('oddrow', background="#EFEFEF")

        # Add vertical and horizontal scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.recommendations_treeview.yview)
        vsb.pack(side='right', fill='y')
        self.recommendations_treeview.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.recommendations_treeview.xview)
        hsb.pack(side='bottom', fill='x')
        self.recommendations_treeview.configure(xscrollcommand=hsb.set)

        # Back to Main Page button
        back_button = tk.Button(self, text="Back to Main Page", command=lambda: controller.show_page(MainPage), bg="#CFB284", fg="black", font=("Helvetica", 14, "bold"), bd=0)
        back_button.pack(pady=10)

        # Bind double-click event to the Treeview
        self.recommendations_treeview.bind("<Double-1>", self.on_treeview_double_click)

    def set_query(self, query):
        self.query = query
        self.display_recommendations()

    def display_recommendations(self):
        if self.query and self.main_page_instance.uploaded_dataset is not None:
            recommendations = recommend_courses(self.query, self.main_page_instance.uploaded_dataset)
            if not recommendations.empty:
                self.recommendations_treeview.delete(*self.recommendations_treeview.get_children())  # Clear previous recommendations
                self.url_dict = {}  # Clear previous URLs
                for i, (index, row) in enumerate(recommendations.iterrows()):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    self.recommendations_treeview.insert("", "end", iid=index, values=(row['course_title'], row['content_duration'], row['price'], row['url']), tags=(tag,))
                    self.url_dict[index] = row['url']  # Store URL in dictionary
            else:
                messagebox.showinfo("No Results", "No recommendations found.")
        else:
            messagebox.showinfo("Missing Query or Dataset", "Please enter a search query and upload a dataset.")

    def on_treeview_double_click(self, event):
        item = self.recommendations_treeview.selection()[0]
        url = self.url_dict[int(item)]  # Get the URL from the dictionary
        webbrowser.open(url)  # Open the URL in the default web browser



# Function to recommend courses
def recommend_courses(query, dataset):
    if not query.strip():
        return pd.DataFrame(columns=['course_title', 'content_duration', 'price', 'url'])

    df = dataset.copy()
    df['Clean_title'] = df['course_title'].apply(nfx.remove_stopwords)
    df['Clean_title'] = df['Clean_title'].apply(nfx.remove_special_characters)

    countvect = CountVectorizer()
    cvmat = countvect.fit_transform(df['Clean_title'])
    cos_sim = cosine_similarity(cvmat)

    try:
        query_idx = df[df['course_title'].str.lower().str.contains(query.lower())].index[0]
    except IndexError:
        return pd.DataFrame(columns=['course_title', 'content_duration', 'price', 'url'])  # If query not found, return empty DataFrame

    scores = list(enumerate(cos_sim[query_idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_n = 10  # You can adjust the number of recommendations
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    
    recommendations = df.loc[top_indices, ['course_title', 'content_duration', 'price', 'url']]

    return recommendations



        




def main():
    app = SampleApp()
    app.mainloop()


if __name__ == '__main__':
    main()