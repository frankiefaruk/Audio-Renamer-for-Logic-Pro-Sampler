import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.font import Font
import re
import os


class AudioFileRenamerTextFileGenerator:
   def __init__(self, root):
       self.root = root
       self.root.title("Audio File Renamer / Text File Generator")
       self.root.geometry("500x600")
       self.root.configure(bg="#323232")


       # Define font styles
       label_font = Font(family="Helvetica", size=14)
       entry_font = Font(family="Helvetica", size=14)
       button_font = Font(family="Helvetica", size=14)
       preview_font = Font(family="Helvetica", size=14)


       # Complete MIDI Note Mapping
       self.note_mapping = {
           "C-1": 0, "C#-1": 1, "D-1": 2, "D#-1": 3, "E-1": 4, "F-1": 5, "F#-1": 6, "G-1": 7, "G#-1": 8, "A-1": 9, "A#-1": 10, "B-1": 11,
           "C0": 12, "C#0": 13, "D0": 14, "D#0": 15, "E0": 16, "F0": 17, "F#0": 18, "G0": 19, "G#0": 20, "A0": 21, "A#0": 22, "B0": 23,
           "C1": 24, "C#1": 25, "D1": 26, "D#1": 27, "E1": 28, "F1": 29, "F#1": 30, "G1": 31, "G#1": 32, "A1": 33, "A#1": 34, "B1": 35,
           "C2": 36, "C#2": 37, "D2": 38, "D#2": 39, "E2": 40, "F2": 41, "F#2": 42, "G2": 43, "G#2": 44, "A2": 45, "A#2": 46, "B2": 47,
           "C3": 48, "C#3": 49, "D3": 50, "D#3": 51, "E3": 52, "F3": 53, "F#3": 54, "G3": 55, "G#3": 56, "A3": 57, "A#3": 58, "B3": 59,
           "C4": 60, "C#4": 61, "D4": 62, "D#4": 63, "E4": 64, "F4": 65, "F#4": 66, "G4": 67, "G#4": 68, "A4": 69, "A#4": 70, "B4": 71,
           "C5": 72, "C#5": 73, "D5": 74, "D#5": 75, "E5": 76, "F5": 77, "F#5": 78, "G5": 79, "G#5": 80, "A5": 81, "A#5": 82, "B5": 83,
           "C6": 84, "C#6": 85, "D6": 86, "D#6": 87, "E6": 88, "F6": 89, "F#6": 90, "G6": 91, "G#6": 92, "A6": 93, "A#6": 94, "B6": 95,
           "C7": 96, "C#7": 97, "D7": 98, "D#7": 99, "E7": 100, "F7": 101, "F#7": 102, "G7": 103, "G#7": 104, "A7": 105, "A#7": 106, "B7": 107,
           "C8": 108, "C#8": 109, "D8": 110, "D#8": 111, "E8": 112, "F8": 113, "F#8": 114, "G8": 115, "G#8": 116, "A8": 117, "A#8": 118, "B8": 119,
           "C9": 120, "C#9": 121, "D9": 122, "D#9": 123, "E9": 124, "F9": 125, "F#9": 126, "G9": 127
       }


       # Main frame
       main_frame = tk.Frame(root, bg="#323232", bd=0)
       main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

       # Input fields
       tk.Label(main_frame, text="Enter Name", bg="#323232", fg="white", font=label_font).pack(anchor='w')
       self.name_entry = tk.Entry(main_frame, bg="#4D4D4D", fg="white", insertbackground="white", highlightthickness=0, relief="flat", font=entry_font)
       self.name_entry.pack(fill=tk.X)
       self.name_entry.bind('<KeyRelease>', self.on_entry_change)

       tk.Label(main_frame, text="Enter Group Name", bg="#323232", fg="white", font=label_font).pack(anchor='w')
       self.group_entry = tk.Entry(main_frame, bg="#4D4D4D", fg="white", insertbackground="white", highlightthickness=0, relief="flat", font=entry_font)
       self.group_entry.pack(fill=tk.X)
       self.group_entry.bind('<KeyRelease>', self.on_entry_change)

       # Preview Section
       preview_frame = tk.LabelFrame(main_frame, text="Preview", bg="#323232", fg="white",
                                   font=label_font, bd=0, relief="flat")
       preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
       self.preview_text = tk.Text(preview_frame, height=8, bg="#4D4D4D", fg="white",
                                 insertbackground="white", highlightthickness=0, relief="flat", font=preview_font)
       self.preview_text.pack(fill=tk.BOTH, expand=True)


       # Buttons
       button_frame = tk.Frame(main_frame, bg="#323232")
       button_frame.pack(pady=10)
       
       tk.Button(button_frame, text="Select Folder", command=self.process_folder,
                bg="#4D4D4D", fg='grey', relief="flat", bd=0,
                activebackground="#4D4D4D", font=button_font).pack(side=tk.LEFT, padx=5)
       
       tk.Button(button_frame, text="Submit", command=self.submit_rename,
                bg="#4D4D4D", fg='grey', relief="flat", bd=0,
                activebackground="#4D4D4D", font=button_font).pack(side=tk.LEFT, padx=5)
       
       # Store selected folder path
       self.selected_folder = None
       self.rename_pairs = []


   def extract_note_name(self, filename):
       try:
           # Split by hyphens and look for the note part
           parts = filename.split('-')
           if len(parts) >= 3:
               # Look for a part that matches a note pattern (like C4, G#5, etc.)
               for part in parts:
                   # Clean up the part (remove spaces, file extensions, etc.)
                   cleaned_part = part.strip().split('.')[0]
                   # Check if this part is in our note mapping
                   if cleaned_part in self.note_mapping:
                       print(f"Found note: {cleaned_part}")
                       return self.note_mapping[cleaned_part], cleaned_part
               
               print(f"No valid note found in parts: {parts}")
               return None, None
           else:
               print(f"Filename format incorrect: {filename}")
               return None, None
       except Exception as e:
           print(f"Error processing filename: {e}")
           return None, None


   def process_folder(self):
       # 1- Load Folder containing audio files
       folder = filedialog.askdirectory(title="Select Folder with Audio Files")
       if not folder:
           return
       
       self.selected_folder = folder
       self.update_preview()


   def update_preview(self):
       if not self.selected_folder:
           return

       # Clear preview text
       self.preview_text.delete(1.0, tk.END)
       
       # Get all audio files in the folder
       files = [os.path.join(self.selected_folder, f) for f in os.listdir(self.selected_folder) 
                if f.endswith(('.wav', '.aif', '.aiff', '.mp3'))]
       
       if not files:
           self.preview_text.insert(tk.END, "No audio files found in the selected folder.")
           return

       preview_text = ""
       self.rename_pairs = []
       
       for file_path in files:
           folder, original_name = os.path.split(file_path)
           
           # 2- Parse note names
           # 3- Find and adjust the relevant tracks using note_mapping
           midi_number, note_name = self.extract_note_name(original_name)
           
           if midi_number is None or note_name is None:
               preview_text += f"Skipping {original_name} (no valid note found)\n"
               continue
           
           # Extract velocity (if exists)
           velocity_match = re.search(r'V(\d+)', original_name)
           velocity = velocity_match.group(0) if velocity_match else "V127"
           
           # 4- Adjust instrument name and group names from user inputs
           base_name = self.name_entry.get().strip() or "unnamed"
           group_name = self.group_entry.get().strip() or "nogroup"
           
           # Create new name with strict ordering:
           # [Note Number]_[Note Name]_[Name]_[Velocity]_[Group Name]
           name_parts = [
               str(midi_number),
               note_name,
               base_name,
               velocity,
               group_name
           ]
           
           new_name = "_".join(name_parts) + os.path.splitext(original_name)[1]
           preview_text += f"{original_name} → {new_name}\n"
           self.rename_pairs.append((file_path, os.path.join(folder, new_name)))
       
       # Update preview
       self.preview_text.insert(tk.END, preview_text)


   def submit_rename(self):
       if not self.selected_folder:
           messagebox.showwarning("No Folder", "Please select a folder first.")
           return
           
       if not self.rename_pairs:
           messagebox.showwarning("Nothing to Rename", "No files to rename.")
           return
           
       # Ask for confirmation
       if messagebox.askyesno("Confirm Rename", "Do you want to proceed with renaming?"):
           for old_path, new_path in self.rename_pairs:
               os.rename(old_path, new_path)
           messagebox.showinfo("Success", "Files have been renamed.")
           
           # Clear everything after successful rename
           self.name_entry.delete(0, tk.END)
           self.group_entry.delete(0, tk.END)
           self.preview_text.delete(1.0, tk.END)
           self.selected_folder = None
           self.rename_pairs = []


   def rename_multiple_audio_files(self):
       folder = filedialog.askdirectory(title="Select Folder for New Audio Files")
       if not folder:
           messagebox.showwarning("No Folder Selected", "Please select a destination folder.")
           return


       base_name = self.name_entry.get().strip()
       if not base_name:
           messagebox.showwarning("No Name", "Please enter a base name for the files.")
           return


       preview_text = "Files will be named as:\n\n"
       for note_name, midi_number in self.note_mapping.items():
           filename = f"{midi_number}_{note_name}_{base_name}.wav"
           preview_text += f"{filename}\n"


       self.preview_text.delete(1.0, tk.END)
       self.preview_text.insert(tk.END, preview_text)


   def create_text_file(self):
       folder = filedialog.askdirectory(title="Select Folder for Text File")
       if not folder:
           messagebox.showwarning("No Folder Selected", "Please select a destination folder.")
           return


       base_name = self.name_entry.get().strip()
       if not base_name:
           messagebox.showwarning("No Name", "Please enter a base name for the files.")
           return


       preview_text = "Text file will contain:\n\n"
       text_content = ""
      
       for note_name, midi_number in self.note_mapping.items():
           line = f"{midi_number}_{note_name}_{base_name}.wav\n"
           preview_text += line
           text_content += line


       self.preview_text.delete(1.0, tk.END)
       self.preview_text.insert(tk.END, preview_text)


       if messagebox.askyesno("Confirm", "Do you want to create the text file?"):
           file_path = os.path.join(folder, f"{base_name}_mapping.txt")
           with open(file_path, 'w') as f:
               f.write(text_content)
           messagebox.showinfo("Success", "Text file has been created.")


   def process_action(self):
       action = self.action_var.get()
       if action == "rename":
           self.rename_multiple_audio_files()
       elif action == "text":
           self.create_text_file()
       elif action == "rename_existing":
           self.rename_existing_files()


   def on_entry_change(self, event=None):
       """Called whenever an entry field is modified"""
       if self.selected_folder:  # Only update if a folder is selected
           self.update_preview()


# Run the GUI application
if __name__ == "__main__":
   root = tk.Tk()
   app = AudioFileRenamerTextFileGenerator(root)
   root.mainloop()
