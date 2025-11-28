#Run on windows: 'py "D:\Python\InformatikTfgBibilothek\gui.py"'
class guierrs():
	class InvailidArgument(Exception): ...

#Prepeare log file
with open("gui.log","w+") as fle: fle.write("### Log of GUI for Bibilothek project")

def log(src:str,tpe:str,txt:str): #Log function for GUI functions
	clr = "31" if tpe.lower() in ("err","error","fatal") else "32" if tpe.lower() in ("okay") else "33" if tpe.lower() in ("warn","warning") else "36" if tpe.lower() in ("info") else "34" if tpe.lower() in ("debug") else "0"
	mdclr = "red" if tpe.lower() in ("err","error","fatal") else "green" if tpe.lower() in ("okay") else "orange" if tpe.lower() in ("warn","warning") else "cyan" if tpe.lower() in ("info") else "blue" if tpe.lower() in ("debug") else "white"
	print(f"\033[{clr}m[GUI/{src}] {tpe.upper()}: {txt}\033[0m")
	try:
		with open("gui.log","a") as fle:
			#fle.write(f"<span style='color:{mdclr}>**[GUI/{src}]** *{tpe.upper()}*: {txt}</span>\n")
			fle.write(f"GUI/{src}] {tpe.upper()}: {txt}")
	except: pass

from tkinter import *
from tkinter import ttk
try: import database as db
except: log("import","warn","Could not find module database.py")

class guivars(): #Variables & Widgets of GUI
	test = True
	class pages():
		pages_tp = {"Bücher verwalten":"manageBooks","Schüler verwalten":"managePupils","Meldungen":"Alerts"}
		pages_pt = {"manageBooks":"Bücher verwalten","managePupils":"Schüler verwalten","Alerts":"Meldungen"}
		pages_tlst = ["Bücher verwalten","Schüler verwalten","Meldungen"]
		currentpage = "manageBooks"
	class frames():
		defsize = []
		class manageBooks(): ...
		class managePupils(): ...
	class elements():
		class general(): ...
		class manageBooks(): ...
		class managePupils(): ...

class guicmds(): #Commands of GUI
	def test(*args,**kwargs): print(f"Test proceed {args} {kwargs}")
	
	class general():
		def change_page(event): #Show specific page
			log("guicmds.general.change_page","info",f"Changing page of GUI to '{guivars.elements.general.navigation.get()}' (Internal adress is '{guivars.pages.pages_tp[guivars.elements.general.navigation.get()]}')")
			for frm in guivars.frames.pages:
				frm.grid_forget()
			guivars.frames.pages[guivars.pages.pages_tlst.index(guivars.elements.general.navigation.get())].grid(row=1,column=0,pady=4)
			guivars.pages.currentpage = guivars.pages.pages_tp[guivars.elements.general.navigation.get()]
		
		def reload_widget(event): #Reload specified widget on page
			actlst = {"manageBooks":guicmds.manageBooks.list_searched_books,"managePupils":guicmds.managePupils.getPupils}
			try: actlst[guivars.pages.currentpage]()
			except Exception as exc:
				log("guicmds.general.reload_list","warn",f"Failed to reload specified widget on page '{guivars.pages.currentpage}' ({exc})")
	
	class manageBooks():
		def list_searched_books():
			log("guicmds.manageBooks.list_searched_books","info",f"Searching for book with keyword '{guivars.elements.manageBooks.search_ent.get()}'")
			try:
				guiutils.clearTreeviewContent(guivars.elements.manageBooks.searchresults)
				if guivars.test:
					tstlst = []
					for i in range(200): tstlst.append((f"Title (Entry {i})","Author","Publishion","ISBN","Signature","Status"))
					for elm in tstlst:
						guivars.elements.manageBooks.searchresults.insert("","end",values=elm)
				else:
					for elm in db.suche_buch(guivars.elements.manageBooks.search_ent.get()):
						guivars.elements.manageBooks.searchresults.insert("","end",values=elm)
				log("guicmds.manageBooks.list_searched_books","okay","List of books with search keyword loaded")
			except Exception as exc:
				log("guicmds.manageBooks.list_searched_books","error",f"Search for books failed ({exc})")
				guivars.elements.manageBooks.searchresults.insert("","end",values=["None","None","None","None","None","ERROR"])
		
		def get_selected():
			log("guicmds.manageBooks.get_selected","info",f"Trying to get selected item(-s) from grid")
			_return = []
			for elm in guivars.elements.manageBooks.searchresults.selection():
				log("guicmds.manageBooks.get_selected","debug",f"Selected item found: {guivars.elements.manageBooks.searchresults.item(elm,'values')}")
				_return.append(guivars.elements.manageBooks.searchresults.item(elm,"values"))
			log("guicmds.manageBooks.get_selected","okay","Selected items read")
			return _return

	class managePupils():
		def getPupils():
			log("guicmds.managePupils.getPupils","info","Loading list of Pupils...")
			try:
				guiutils.clearTreeviewContent(guivars.elements.managePupils.searchresults)
				if guivars.test:
					tstlst = []
					for i in range(200): tstlst.append((f"Name (Pupil {i})","Mail@adress.tst","8T"))
					for elm in tstlst:
						guivars.elements.managePupils.searchresults.insert("","end",values=elm)
				else:
					for elm in db.schueler_liste():
						guivars.elements.managePupils.searchresults.insert("","end",values=elm)
				log("guicmds.managePupils.getPupils","okay","List of pupils loaded")
			except Exception as exc:
				log("guicmds.managePupils.getPupils","error",f"Search for pupils failed ({exc})")
				guivars.elements.managePupils.searchresults.insert("","end",values=("None","None","None"))

class guiutils(): #Useful functions for GUI
	def get_page_frm(pn="",pa=""):
		"""
		pn (pagename) means the name which is shown in the Navigation Menu, pa (pageaddr) means the internal PageAdress
		"""
		if pn in (None,"") and pa in (None,""): raise guierrs.InvailidArgument(f"Invailid arguments used in guiutils.get_page_frm (Either 'pagename' or 'pageaddr' has to be set)")
		return guivars.frames.pages[guivars.pages.pages_tlst.index(pn if pn not in (None,"") else guivars.pages.pages_pt[pa])]#
	
	def setupBookSearch():
		guivars.elements.manageBooks.searchresults.column("title",anchor=CENTER,width=300)
		guivars.elements.manageBooks.searchresults.heading("title",text="Titel")
		guivars.elements.manageBooks.searchresults.column("author",anchor=CENTER,width=150)
		guivars.elements.manageBooks.searchresults.heading("author",text="Autor")
		guivars.elements.manageBooks.searchresults.column("publishingDate",anchor=CENTER,width=110)
		guivars.elements.manageBooks.searchresults.heading("publishingDate",text="Veröffentlichung")
		guivars.elements.manageBooks.searchresults.column("ISBN",anchor=CENTER,width=60)
		guivars.elements.manageBooks.searchresults.heading("ISBN",text="ISBN")
		guivars.elements.manageBooks.searchresults.column("signature",anchor=CENTER,width=60)
		guivars.elements.manageBooks.searchresults.heading("signature",text="Signatur")
		guivars.elements.manageBooks.searchresults.column("state",anchor=CENTER,width=80)
		guivars.elements.manageBooks.searchresults.heading("state",text="Status")
		guivars.elements.manageBooks.searchresults.column("scrollbar",anchor=CENTER,width=2)
	
	def setupPupilSearch():
		guivars.elements.managePupils.searchresults.column("name",anchor=CENTER,width=400)
		guivars.elements.managePupils.searchresults.heading("name",text="Name")
		guivars.elements.managePupils.searchresults.column("mail",anchor=CENTER,width=260)
		guivars.elements.managePupils.searchresults.heading("mail",text="E-Mail Adresse")
		guivars.elements.managePupils.searchresults.column("class",anchor=CENTER,width=100)
		guivars.elements.managePupils.searchresults.heading("class",text="Klasse")
		guivars.elements.managePupils.searchresults.column("scrollbar",anchor=CENTER,width=2)
	
	def clearTreeviewContent(treeview:ttk.Treeview):
		treeview.delete(*treeview.get_children())


"""
Notitzen:
Listbox für Bücher/Schülerliste Nutzen (s. https://www.geeksforgeeks.org/python/dropdown-menus-tkinter/; https://derlinuxwikinger.de/tabellen-mit-python-erstellen/)
(bg="red",relief="raised"/"flat"/"sunken"/"groove",bd=2) -> Argumente für Frame Border
"""

def init_gui(title="Bücherverwaltung"):
	log("init_gui","info","Initializing GUI...")
	guivars.win = Tk() #Create Tk Window
	guivars.frames.main = Frame(guivars.win) #Create mainframe of Tk Window

	#set Title of window
	log("init_gui","info","Setting title")
	guivars.win.title(title if not guivars.test else title + " (Test)") #Configure title of window, but if test mode is active, add "(Test)" and the end
	if guivars.test: log("init_gui","warn","This program currently runs in 'test' Mode (resulting in faked databases, etc.)")

	#Create Tk Win content frames
	guivars.frames.top = Frame(guivars.frames.main,bg="gray")
	guivars.frames.content = Frame(guivars.frames.main)

	#Bind frames to Main Frame
	guivars.frames.top.grid(row=0,column=0,sticky="W")
	guivars.frames.content.grid(row=1,column=0)

	#Configure different weight of frames
	guivars.frames.main.grid_rowconfigure(0,weight=1)
	guivars.frames.main.grid_rowconfigure(1,weight=10)
	guivars.frames.top.grid_columnconfigure(1,weight=4)

	#Configure Elements of navigation line
	log("init_gui","info","Configuring Navigation Widgets")
	guivars.elements.general.navigation = ttk.Combobox(guivars.frames.top,values=guivars.pages.pages_tlst,width=20)
	guivars.elements.general.navigation.bind("<<ComboboxSelected>>",guicmds.general.change_page) #On every change of selection, change the GUI page
	guivars.elements.general.navigation.current(0) #Set current selection to first page text
	guivars.elements.general.navigation.grid(row=0,column=0,sticky="W")
	
	#Generate frames for GUI
	log("init_gui","info","Generating Frames for Pages")
	guivars.frames.pages = []
	for i in range(len(guivars.pages.pages_tlst)):
		guivars.frames.pages.append(Frame(guivars.frames.main,pady=2,padx=2,bg="lightgray",relief="sunken",bd=4))
	
	log("init_gui","info","Defining contents for pages")
	#Configure content widgets for page "manageBooks"
	log("init_gui","info","Configuring widgets for page 'manageBooks'")
	p = guiutils.get_page_frm(pa="manageBooks")
	p.grid_columnconfigure(0,weight=5)
	guivars.frames.manageBooks.searchBooks = Frame(p,bg="lightgray",relief="raised",bd=4) #Frame for Book search
	guivars.frames.manageBooks.searchBooks.grid(row=0,column=0,rowspan=60)

	log("init_gui","info","Configuring widgets for search frame on page 'manageBooks'")
	guivars.elements.manageBooks.title = Label(guivars.frames.manageBooks.searchBooks,text="Bücher suchen",font=("Monospace",18),fg="green")
	guivars.elements.manageBooks.title.grid(row=0,column=0,columnspan=4,sticky="W")
	guivars.elements.manageBooks.search_lbl = Label(guivars.frames.manageBooks.searchBooks,text="Suchbegriff:")
	guivars.elements.manageBooks.search_lbl.grid(row=1,column=0,columnspan=2,sticky="E")
	guivars.elements.manageBooks.search_ent = Entry(guivars.frames.manageBooks.searchBooks)
	guivars.elements.manageBooks.search_ent.grid(row=1,column=2,columnspan=3,sticky="W")
	guivars.elements.manageBooks.search_btn = Button(guivars.frames.manageBooks.searchBooks,text="Suchen (F6)",command=guicmds.manageBooks.list_searched_books)
	guivars.elements.manageBooks.search_btn.grid(row=1,column=5,sticky="W")
	"""guivars.elements.manageBooks.searchresults = Listbox(guivars.frames.manageBooks.searchBooks,width=150,height=30,font=("Monospace",9))
	guivars.elements.manageBooks.searchresults.grid(row=2,column=0,sticky="W",columnspan=50)"""
	guivars.elements.manageBooks.searchresults = ttk.Treeview(guivars.frames.manageBooks.searchBooks,columns=("title","author","publishingDate","ISBN","signature","state","scrollbar"),selectmode="browse",show="headings",height=20)
	guivars.elements.manageBooks.sr_scrollbar = ttk.Scrollbar(guivars.elements.manageBooks.searchresults,orient="vertical",command=guivars.elements.manageBooks.searchresults.yview)
	guivars.elements.manageBooks.sr_scrollbar.place(x=745,y=25,height=400)
	guivars.elements.manageBooks.searchresults.configure(yscrollcommand=guivars.elements.manageBooks.sr_scrollbar.set)
	guivars.elements.manageBooks.searchresults.grid(row=2,column=0,sticky="W",columnspan=50)
	guiutils.setupBookSearch() #Setup columns of searchresults

	log("init_gui","info","Configuring buttons for editing books")
	guivars.frames.manageBooks.editbooks_frm = Frame(p,bg="#AE6D6D")
	guivars.elements.manageBooks.addbook_btn = Button(guivars.frames.manageBooks.editbooks_frm,text="Buch hinzufügen",command=lambda:log("addbook_btn","okay","Click event detected"))
	guivars.elements.manageBooks.addbook_btn.grid(row=0,column=0,padx=6,pady=4)
	guivars.elements.manageBooks.rembook_btn = Button(guivars.frames.manageBooks.editbooks_frm,text="Buch entfernen",command=lambda:log("rembook_btn","okay","Click event detected"))
	guivars.elements.manageBooks.rembook_btn.grid(row=1,column=0,padx=6,pady=4)
	guivars.elements.manageBooks.cnfbook_btn = Button(guivars.frames.manageBooks.editbooks_frm,text="  Buch bearbeiten  ",command=lambda:log("cnfbook_btn","okay","Click event detected"))
	guivars.elements.manageBooks.cnfbook_btn.grid(row=2,column=0,padx=6,pady=4)
	guivars.elements.manageBooks.rembook_btn = Button(guivars.frames.manageBooks.editbooks_frm,text="TEST SELECT",command=guicmds.manageBooks.get_selected)
	guivars.elements.manageBooks.rembook_btn.grid(row=3,column=0,padx=6,pady=4)
	guivars.frames.manageBooks.editbooks_frm.grid(row=0,column=1)
	guivars.frames.manageBooks.rentbooks_frm = Frame(p,bg="#6DAD73")
	guivars.elements.manageBooks.rentbook_btn = Button(guivars.frames.manageBooks.rentbooks_frm,text="Buch ausleihen",command=lambda:log("rentbook_btn","okay","Click event detected"))
	guivars.elements.manageBooks.rentbook_btn.grid(row=0,column=0,padx=6,pady=4)
	guivars.elements.manageBooks.returnbook_btn = Button(guivars.frames.manageBooks.rentbooks_frm,text="Buch zurückgeben",command=lambda:log("returnbook_btn","okay","Click event detected"))
	guivars.elements.manageBooks.returnbook_btn.grid(row=1,column=0,padx=6,pady=4)
	guivars.frames.manageBooks.rentbooks_frm.grid(row=1,column=1,pady=2)
	
	log("init_gui","okay","Page 'manageBooks' configured")

	#Store informational data of Frame 1 to apply on other page frames
	log("init_gui","info","Loading size of page frame for 'manageBooks'")
	guivars.win.update_idletasks()
	w = p.winfo_reqwidth()
	h = p.winfo_reqheight()
	guivars.frames.pages_defsize = [w,h]
	log("init_gui","debug",f"Loaded size for default page content frames: [W:{w} H:{h}]")

	#Configure size of other page frames depending on the size of page 1
	log("init_gui","info","Changing height of page frames...")
	for frm in guivars.frames.pages:
		frm.configure(width=w)
		frm.configure(height=h)

	#Configure content widgets for page "managePupils"
	log("init_gui","info","Configuring widgets for page 'managePupils'")
	p = guiutils.get_page_frm(pa="managePupils")
	p.grid_columnconfigure(0,weight=5)
	guivars.frames.managePupils.searchPupils = Frame(p,bg="lightgray",relief="raised",bd=4) #Frame for Book search
	guivars.frames.managePupils.searchPupils.grid(row=0,column=0,rowspan=60)

	log("init_gui","info","Configuring widgets for search frame on page 'managePupils'")
	guivars.elements.managePupils.title = Label(guivars.frames.managePupils.searchPupils,text="Schülerliste",font=("Monospace",18),fg="orange")
	guivars.elements.managePupils.title.grid(row=0,column=0,columnspan=4,sticky="W")
	guivars.elements.managePupils.reload_btn = Button(guivars.frames.managePupils.searchPupils,text="Aktualisiere Liste (F6)",command=guicmds.managePupils.getPupils)
	guivars.elements.managePupils.reload_btn.grid(row=1,column=0,columnspan=4,sticky="W",pady=2)
	"""guivars.elements.managePupils.searchresults = Listbox(guivars.frames.managePupils.searchPupils,width=150,height=30,font=("Monospace",9))
	guivars.elements.managePupils.searchresults.grid(row=2,column=0,sticky="W",columnspan=50)"""
	guivars.elements.managePupils.searchresults = ttk.Treeview(guivars.frames.managePupils.searchPupils,columns=("name","mail","class","scrollbar"),selectmode="browse",show="headings",height=20)
	guivars.elements.managePupils.sr_scrollbar = ttk.Scrollbar(guivars.elements.managePupils.searchresults,orient="vertical",command=guivars.elements.managePupils.searchresults.yview)
	guivars.elements.managePupils.sr_scrollbar.place(x=745,y=25,height=400)
	guivars.elements.managePupils.searchresults.configure(yscrollcommand=guivars.elements.managePupils.sr_scrollbar.set)
	guivars.elements.managePupils.searchresults.grid(row=2,column=0,sticky="W",columnspan=50)
	guiutils.setupPupilSearch() #Setup columns of searchresults
	guicmds.managePupils.getPupils() #Load list of Pupils to listbox

	log("init_gui","info","Configuring buttons for editing pupils")
	guivars.elements.managePupils.importpupil_btn = Button(p,text="Importiere Schüler aus CSV",command=lambda:log("importpupil_btn","okay","Click event detected"))
	guivars.elements.managePupils.importpupil_btn.grid(row=0,column=1,padx=6)
	guivars.elements.managePupils.addpupil_btn = Button(p,text="Füge einzelnen Schüler hinzu",command=lambda:log("addpupil_btn","okay","Click event detected"))
	guivars.elements.managePupils.addpupil_btn.grid(row=1,column=1,padx=6)

	log("init_gui","okay","Page 'managePupils' configured")
	
	#Bind frame of first Page in guivars.pages.pages_tlst to window
	guivars.frames.pages[0].grid(row=1,column=0,pady=4)

	#Load keybinds
	log("init_gui","info","Loading window keybinds")
	guivars.win.bind("<F6>",guicmds.general.reload_widget)
	log("init_gui","okay","Window keybinds loaded")
	
	#Bind mainframe to window
	guivars.frames.main.pack(side="left",anchor="nw")

def change_title(title=""):
	guivars.win.title(title)

def change_current_path(path=""):
	guivars.elements.general.actionpath.configure(text=path)

if __name__ == "__main__":
	init_gui()
	guivars.win.mainloop()