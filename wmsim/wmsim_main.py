#	Project Name	:	Visual Python IDE for 2.6#	Date	        :	13-12-2009#	Author		    :	macrocoders team#	Contact		    :	macrocoders@gmail.com#	Web			    :	http://visualpython.org#	Python Ver.     :	2.6# -*- coding: utf-8 -*-from Tkinter import *from tkMessageBox import *from wmsim_py import *# -- Do not change. You may experience problems with the design file. #form1=Tk()form1.title('form1')form1.resizable(width=FALSE, height=FALSE)form1.geometry('427x331+100+100')# -- Do not change. You may experience problems with the design file. ## -- Do not change. You may experience problems with the design file. -- #
button1=Button(text='button1', command=button1Click)
button1.place(relx=0., rely=0., relwidth=0., relheight=0.)

# -- Do not change. You may experience problems with the design file. -- #
textBox1=Entry(font = '{MS Sans Serif} 10')
textBox1.place(relx=0., rely=0., relwidth=0., relheight=0.)

# -- Do not change. You may experience problems with the design file. -- #
label1=Label(text='label1')
label1.place(relx=0., rely=0., relwidth=0., relheight=0.)

form1.mainloop()