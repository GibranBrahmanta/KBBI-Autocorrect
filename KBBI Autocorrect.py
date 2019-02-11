from tkinter import *
from tkinter.messagebox import showinfo
from selenium import webdriver
import string

'''Program ini menerima berkas masukan berupa teks dan mengeluarkan berkas keluaran berupa teks 
yang berisi teks pada berkas masukan dan mengganti kata yang tidak baku menjadi baku menurut KBBI'''

class KBBI_Converter(Frame):
	'''Class untuk menjalankan program ini secara keseluruhan'''

	def __init__(self):		#Fungsi untuk menjalankan GUI dari  program ini
		Frame.__init__(self)
		self.InputGUI()
		self.OutputGUI()

	def InputGUI(self):		#Fungsi untuk membuat GUI yang berkaitan dengan input program ini
		input_label = Label(text="Pilih berkas yang ingin diperbaharui:",font=("muli", "12"))
		input_label.pack()
		self.input_text = Text(height = 1, width = 20)
		self.input_text.pack()
		input_button = Button(text="Pilih berkas",relief=RAISED, command= lambda:self.File_Split())
		input_button.pack()

	def OutputGUI(self): 	#Fungsi untuk membuat GUI yang berkaitan dengan output program ini
		output_label = Label(text="Pilih berkas sebagai tempat penyimpanan:",font=("muli", "12"))
		output_label.pack()
		self.output_text = Text(height = 1, width = 20)
		self.output_text.pack()
		output_button = Button(text="Pilih dan Perbaharui",relief=RAISED, command= lambda:self.Output())
		output_button.pack()
		self.output_textbox = Text(height = 20, width = 50)
		self.output_textbox.pack()

	def Input_File(self): 	#Fungsi untuk membuka file melalui GUI
		from tkinter import filedialog
		root_window = Tk()
		root_window.withdraw()
		return filedialog.askopenfilename()

	def Open_File_Input(self):	#Fungsi untuk membuka file input dan menjadikanya dalam bentuk list
		self.file_input = open(self.Input_File(),'r')
		self.input_text.delete(1.0,END)
		slash = self.file_input.name.rfind('/')
		file_name = self.file_input.name[slash+1::]
		self.input_text.insert(INSERT,file_name)
		return self.file_input

	def Open_File_Output(self):	#Fungsi untuk membuka file output dan menyiapkanya untuk menulis berkas baru 
		self.file_output = open(self.Input_File(),'w')
		self.output_text.delete(1.0,END)
		slash = self.file_output.name.rfind('/')
		file_name = self.file_output.name[slash+1::]
		self.output_text.insert(INSERT,file_name)
		return self.file_output

	def File_Split(self):	#Fungsi untuk merubah berkas input menjadi dalam bentuk list berisi satu paragraf pada satu indeksnya
		try :
			file = self.Open_File_Input()
			if self.file_input.name[-4::] != ".txt":
				showinfo("Error",message="Tolong masukan berkas dengan format .txt") 
				#Error Handling ketika berkas input yang dimasukan bukan berkas dengan format .txt
				return
			self.lst_paragraph = []
			for line in file : 											#Iterasi per paragraf
				self.lst_paragraph.append(line.split())
			self.file_input.close()
			return self.lst_paragraph
		except:
			showinfo("Error",message="Tolong masukan berkas yang diperlukan") 
			#Error Handling ketika pengguna belum memasukan berkas yang diperlukan namun meminta program untuk dijalankan
			return

	def Clean_Words(self,temp_word):	#Fungsi untuk memisahkan kata dari tanda baca 
		word = ""
		if len(temp_word) ==  0 :
			return word 
		else :
			if temp_word[0] not in string.punctuation:
				word += str(temp_word[0]) 
			return word + self.Clean_Words(temp_word[1::])

	def Symbol(self,temp_sym):			#Fungsi untuk memisahkan tanda baca dari sebuah kata 
		sym = ""
		if len(temp_sym) == 0:
			return sym
		else :
			if temp_sym[0] in string.punctuation and temp_sym[0] != "." :
				sym = str(temp_sym[0])
			return sym + self.Symbol(temp_sym[1::])

	def Write_File(self,word,sym):		#Fungsi untuk menulis pada berkas keluaran
		special_sym = ["''",'""',"()"]
		if sym in special_sym:
			self.file_output.write(word.join(sym)) 
		elif sym == "(":
			self.file_output.write(sym+word)	
		else:
			self.file_output.write(word+sym)	

	def Check_File(self,paragraph):		#Fungsi untuk mengecek kata dalam suatu paragraf dan menuliskanya di berkas keluaran
		if len(paragraph) == 0 :																					#Mengecek apakah baris kosong atau tidak
				self.file_output.write("\n")
		else :
			for pharse in paragraph: 																				#Mengecek apakah suatu kata baku atau tidak menurut KBBI pasa suatu baris
				word = self.Clean_Words(pharse)
				sym = self.Symbol(pharse)
				link = "https://typoonline.com/kbbi/{}".format(word)						
				self.driver.get(link)																				#Membuka web melalui browser dari modul selenium
				checker = "Kata {} tidak ditemukan".format(word)
				words = self.driver.find_element_by_xpath('//*[@id="textres"]')
				if words.text == checker:																			#Jika tidak baku, maka akan dicarikan kata bakunya menurut KBBI
					link_2 = "https://kbbi.kemdikbud.go.id/entri/{}".format(word)
					self.driver.get(link_2)
					checker_2 = "Entri tidak ditemukan"
					words_2 = self.driver.find_element_by_xpath('/html/body/div[2]/h4[1]') 
					try :
						new_word= self.driver.find_element_by_xpath('/html/body/div[2]/ul[1]/li/a') 				#Mengambil kata yang telah diubah menjadi versi baku menurut KBBI
						self.Write_File(new_word.text,sym)		
					except :
						if checker_2 in words_2.text :
							self.output_textbox.insert(INSERT,"Kata '{}' tidak ada di dalam KBBI.\n".format(word)) 	#Jika tidak ada dalam KBBI, program akan memberitahu pengguna
							self.Write_File(word.upper(),sym)														#Menuliskan kata tersebut ke dalam berkas baru dengan huruf kapital
						else :
							self.Write_File(word,sym)																#Jika kata sudah baku, langsung dituliskan ke dalam berkas baru
				else:
					self.Write_File(word,sym)																		#Jika kata sudah baku, langsung dituliskan ke dalam berkas baru
				if pharse == paragraph[len(paragraph)-1] :
					self.file_output.write(".")
				self.file_output.write(" ")
			self.file_output.write("\n")												

	def Output(self): #Fungsi untuk menulis pada berkas output dari program ini
		try :
			self.Open_File_Output()
			if self.file_output.name[-4::] != ".txt":
				showinfo("Error",message="Tolong masukan berkas dengan format .txt") 
				#Error Handling ketika berkas output yang dimasukan bukan berkas dengan format .txt
				return
		except :
			showinfo("Error",message="Tolong masukan berkas yang diperlukan") 
			#Error Handling ketika pengguna belum memasukan berkas yang diperlukan namun meminta program untuk dijalankan
			return
		self.driver = webdriver.Chrome(r"D:\Kuliah\DDP 1\kodingan\tp4\chromedriver.exe") 						
		for paragraph in self.lst_paragraph:																																				
			self.Check_File(paragraph)																											
		self.driver.quit()																												
		self.file_output.close()
		self.output_textbox.insert(INSERT,"Program ini telah selesai dijalankan.\n")							

def main():
	'''Fungsi utama untuk menjalankan program ini'''
	root = Tk()
	root.title("KBBI Autocorrect [Gibran Brahmanta P.]")
	root.geometry("500x500")
	root.iconbitmap('icon.ico')
	app = KBBI_Converter()
	app.mainloop()

if __name__ == "__main__":
	main()
