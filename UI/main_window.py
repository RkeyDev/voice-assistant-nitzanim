import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Tkinter Base Screen")
root.geometry("500x400")  # Width x Height

# Create a label
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
label.pack(pady=20)

# Create a button
button = tk.Button(root, text="Click Me", command=lambda: label.config(text="Button Clicked!"))
button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()