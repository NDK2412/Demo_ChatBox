import time
import threading
import tkinter as tk
from google import genai

# API Key từ Google GenAI
API_KEY = "AIzaSyAH7ynNF7vZDM-3y34Bz4eMGNjqq0sUv6E"

# Khởi tạo client của Google GenAI
client = genai.Client(api_key=API_KEY)


class ChatBox:
    def __init__(self, master):
        self.master = master
        master.title("Chatbox")


        master.config(bg="#1c1e21")
        self.master.geometry("400x600")

        # Frame chứa nội dung trò chuyện
        self.chat_frame = tk.Frame(master, bg="#1c1e21")
        self.chat_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Text widget để hiển thị cuộc trò chuyện
        self.text_area = tk.Text(self.chat_frame, state='disabled', wrap='word', height=25, width=50,
                                 bg="#1c1e21", fg="white", font=("Arial", 12), insertbackground="white",
                                 bd=0, padx=10, pady=5)
        self.text_area.pack(fill='both', expand=True)

        # Frame chứa thanh nhập tin nhắn
        self.input_frame = tk.Frame(master, bg="#1c1e21")
        self.input_frame.pack(fill='x', padx=10, pady=10)

        # Entry widget cho người dùng nhập câu hỏi
        self.input_entry = tk.Entry(self.input_frame, width=50, font=("Arial", 12), bg="#3a3b3c", fg="white",
                                    insertbackground="white", bd=0, relief="flat")
        self.input_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.send_message)

        # Nút gửi tin nhắn kiểu Messenger
        self.send_button = tk.Button(self.input_frame, text="➤", command=self.send_message, font=("Arial", 14),
                                     bg="#0084ff", fg="white", relief="flat", activebackground="#006bbf",
                                     activeforeground="white", width=4, height=1)
        self.send_button.pack(side=tk.RIGHT)

        # Chào mừng ban đầu từ assistant
        self.display_message("Chatbox", "Hello there, I'm your personal NDK2412. Do you need any help?")

    def display_message(self, sender, message):
        self.text_area.configure(state='normal')
        align = 'right' if sender == "User" else 'left'
        self.text_area.tag_configure(align, justify=align)
        self.text_area.insert(tk.END, f"{sender}: {message}\n", align)
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

    def send_message(self, event=None):
        """Gửi tin nhắn người dùng và xử lý phản hồi."""
        user_message = self.input_entry.get().strip()
        if user_message:
            self.display_message("User", user_message)
            self.input_entry.delete(0, tk.END)
            if user_message.lower() == "quit":
                self.master.quit()
            else:
                self.input_entry.config(state='disabled')
                self.send_button.config(state='disabled')
                threading.Thread(target=self.process_message, args=(user_message,)).start()

    def process_message(self, user_message):
        """Gửi câu hỏi của người dùng đến Google GenAI và lấy phản hồi từ assistant."""
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=user_message
            )
            assistant_response = response.text
            self.display_message("Chatbox", assistant_response)
        except Exception as e:
            self.display_message("Chatbox", f"An error occurred: {str(e)}")
        finally:
            self.input_entry.config(state='normal')
            self.send_button.config(state='normal')


if __name__ == "__main__":
    root = tk.Tk()
    chat_box = ChatBox(root)
    root.mainloop()
