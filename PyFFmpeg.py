#!/bin/python
import sys,os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

## A GUI for FFmpeg in Qt4
# requires FFmpeg version 3.4.2

class mainwin(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self) # inizialize the module
        cWidget = QWidget(self) # widget container
        self.version = '0.2.3'
        # Changelog moved to README.txt
                
        self.setGeometry(30,30,500,250) # starting position and size of the window
        self.setWindowTitle('A GUI for FFmpeg - v%s' % self.version)
        
        # Store parameters here
        self.command = QString('') # it is a string that will be passed to ffmpeg
        self.input = QString('') # absolute path of the input
        self.output = QString('') # absolute path of the output or output name
        self.acodec = QString('copy') # audio codec, default = copy
        self.vcodec = QString('copy') # video codec, default = copy
        self.width = QString('') # Resize parameter
        self.height = QString('') # Resize parameter
        self.crf = QString('23') # Video quality (default crf = 23)
        
        # Layout
        vBox = QVBoxLayout() # main layout
        hBox1 = QHBoxLayout() # input layout
        hBox2 = QHBoxLayout() # output layout
        hBox3 = QHBoxLayout() # 'convert' layout
        hBox4 = QHBoxLayout() # codecs layout
        hBox5 = QHBoxLayout() # resize layout
        vBox1 = QVBoxLayout() # resize sub-layout
        vBox2 = QVBoxLayout() # resize sub-layout
        vBox3 = QVBoxLayout() # resize sub-layout
        
        # StyleSheets
        self.setStyleSheet("""QWidget{background-color: rgb(100,100,105)}
            QToolTip{background-color: black; color: white}
            QLineEdit{background-color: white; color: black}
            QLabel{color: white}
            QLineEdit{background-color: white; color:black}
            QPushButton{background-color: white; color:black}
            QCheckBox{color: white}
            QComboBox{background-color: white; color: black}
            QComboBox QAbstractItemView{background-color: white}
        """)
        
        # Label1: input
        self.label_in = QLabel()
        self.label_in.setFont(QFont('Ubuntu',12))
        self.label_in.setText('<b><i>Input file</i></b>')
        self.label_in.setAlignment(Qt.AlignLeft)
        
        vBox.addWidget(self.label_in)
        
        # Line edit1: input
        self.ledit_in = QLineEdit()
        self.ledit_in.setAlignment(Qt.AlignLeft)
        self.ledit_in.setReadOnly(True) # input is chosen with dialog
        self.ledit_in.textChanged.connect(self.update_input) # store input path
        
        hBox1.addWidget(self.ledit_in)
        
        # PushButton1: input
        self.but_in = QPushButton()
        self.but_in.setText('Input')
        self.but_in.clicked.connect(self.get_input)
        
        hBox1.addWidget(self.but_in)
        
        vBox.addLayout(hBox1)
        vBox.addItem(QSpacerItem(20,20))
        
        # Label2: output
        self.label_out = QLabel()
        self.label_out.setFont(QFont('Ubuntu',12))
        self.label_out.setText('<b><i>Output file</i></b>')
        self.label_out.setAlignment(Qt.AlignLeft)
        
        
        vBox.addWidget(self.label_out)
        
        # Line edit2: output
        self.ledit_out = QLineEdit()
        self.ledit_out.setAlignment(Qt.AlignLeft)
        self.ledit_out.setReadOnly(False) # input is chosen with dialog
        self.ledit_out.textChanged.connect(self.update_output) # store input path
        self.ledit_out.setToolTip('Output file. If no path is provided,\nit works on\
 the current path.\nDefault name is \'output.mp4\'')
        
        hBox2.addWidget(self.ledit_out)
        
        # PushButton2: output
        self.but_out = QPushButton()
        self.but_out.setText('Output')
        self.but_out.clicked.connect(self.get_output)
        
        hBox2.addWidget(self.but_out)
        
        vBox.addLayout(hBox2)
        vBox.addItem(QSpacerItem(15,15))
        
        # Dropdown menus
        # Label: Audio codec
        self.label_acodec = QLabel()
        self.label_acodec.setFont(QFont('Ubuntu condensed',12))
        self.label_acodec.setText('Audio codec')
        
        hBox4.addWidget(self.label_acodec)
        
        # ComboBox: Audio codec
        self.combo_acodec = QComboBox()
        
        # Use StyledItemDelegate (without this, it inherits the non-styled ItemDelegate and
        # stylesheet doesn't work properly)
        itDel = QStyledItemDelegate()
        self.combo_acodec.setItemDelegate(itDel)
        
        self.combo_acodec.addItems(['-','AAC','AC3','OGG','MP3'])
        self.combo_acodec.currentIndexChanged.connect(self.update_acodec)
        self.combo_acodec.setMinimumContentsLength(5)
        self.combo_acodec.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.combo_acodec.setToolTip('Audio codec<br> Select none for <i>copy</i>')
        # if HTML tags are used special characters like \n can't be used
        
        hBox4.addWidget(self.combo_acodec)
        hBox4.addItem(QSpacerItem(50,20))
        hBox4.addStretch()
        
        # Label: Video codec
        self.label_vcodec = QLabel()
        self.label_vcodec.setFont(QFont('Ubuntu condensed',12))
        self.label_vcodec.setText('Video codec')
        
        hBox4.addWidget(self.label_vcodec)
        
        # ComboBox: Video codec
        self.combo_vcodec = QComboBox()
        
        # Use StyledItemDelegate (without this, it inherits the non-styled ItemDelegate and
        # stylesheet doesn't work properly)
        self.combo_vcodec.setItemDelegate(itDel)
        
        self.combo_vcodec.addItems(['-','H264','H265','MPEG4'])
        self.combo_vcodec.currentIndexChanged.connect(self.update_vcodec)
        self.combo_vcodec.setMinimumContentsLength(6)
        self.combo_vcodec.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.combo_vcodec.setToolTip('Video codec<br> Select none for <i>copy</i>')
                
        hBox4.addWidget(self.combo_vcodec)
        
        vBox.addLayout(hBox4)

        # CheckBox: resize
        self.check_res = QCheckBox()
        self.check_res.setText('Resize')
        self.check_res.setFont(QFont('Ubuntu',12))
        self.check_res.stateChanged.connect(self.res_update)
        
        hBox5.addWidget(self.check_res)
        
        # Label: width
        self.label_width = QLabel()
        self.label_width.setText('Width')
        self.label_width.setFont(QFont('Ubuntu',12))
        self.label_width.setAlignment(Qt.AlignCenter)
        
        vBox1.addWidget(self.label_width)
        
        # Line Edit: width
        self.ledit_w = QLineEdit()
        self.ledit_w.setAlignment(Qt.AlignRight)
        self.ledit_w.setValidator(QIntValidator()) # only integer input
        self.ledit_w.setMaxLength(4)
        self.ledit_w.textChanged.connect(self.width_update)
        self.ledit_w.setToolTip('Video dimensions. Leave one of the\nfields blank to keep aspect ratio.')
        
        vBox1.addWidget(self.ledit_w)
        
        hBox5.addStretch()
        hBox5.addLayout(vBox1)
        
        # spacer + label
        vBox2.addItem(QSpacerItem(10,20))
        self.label_x = QLabel('x')
        self.label_x.setFont(QFont('Ubuntu',12))
        vBox2.addWidget(self.label_x)
        
        hBox5.addLayout(vBox2)
        
        # Label: height
        self.label_height = QLabel()
        self.label_height.setText('Height')
        self.label_height.setFont(QFont('Ubuntu',12))
        self.label_height.setAlignment(Qt.AlignCenter)
        
        vBox3.addWidget(self.label_height)
        
        # Line Edit: height
        self.ledit_h = QLineEdit()
        self.ledit_h.setAlignment(Qt.AlignRight)
        self.ledit_h.setValidator(QIntValidator()) # only integer input
        self.ledit_h.setMaxLength(4)
        self.ledit_h.textChanged.connect(self.height_update)
        self.ledit_h.setToolTip('Video dimensions. Leave one of the\nfields blank to keep aspect ratio.')
        
        vBox3.addWidget(self.ledit_h)
        
        hBox5.addLayout(vBox3)
        
        vBox.addItem(QSpacerItem(20,30))
        vBox.addLayout(hBox5)
        
        # PushButton3: convert
        self.but_conv = QPushButton()
        self.but_conv.setText('Convert')
        self.but_conv.clicked.connect(self.convert2)
        
        hBox3.addStretch()
        hBox3.addWidget(self.but_conv)
        hBox3.addStretch()
        
        vBox.addItem(QSpacerItem(20,20))        
        vBox.addLayout(hBox3)
        
        vBox.addStretch() # to keep widgets from resizing
        # Applying Layout
        cWidget.setLayout(vBox)
        self.setCentralWidget(cWidget)
        
        self.res_update() # check the intial state of the checkbox

    # SLOT definitions

    def update_input(self):
        self.input = self.ledit_in.text()
    
    def get_input(self):
#        print self.input.toUtf8() # Debug
        fname = QFileDialog.getOpenFileName(self, 'Open file', './',"Video files (*.avi *.mpeg *.mp4)")
        self.input = fname
        self.ledit_in.setText(self.input)
    
    def update_output(self):
        self.output = self.ledit_out.text()
        
    def get_output(self):
#        print self.output.toUtf8() # Debug
        fname = QFileDialog.getSaveFileName(self, 'Save file', './',"Video files (*.avi *.mpeg *.mp4)")
        self.output = fname
        self.ledit_out.setText(self.output)
    
    def update_acodec(self):
        codecs = {'AAC':'aac','MP3':'libmp3lame','AC3':'ac3','OGG':'libvorbis','-':'copy'}
        ind = self.combo_acodec.currentIndex()
        key = str(self.combo_acodec.itemText(ind))
        self.acodec = QString(codecs[key])
#        print 'acodec = ', self.acodec.toUtf8()   # Debug

    def update_vcodec(self):
        codecs = {'H264':'libx264','H265':'libx265','MPEG4':'libxvid','-':'copy'}
        ind = self.combo_vcodec.currentIndex()
        key = str(self.combo_vcodec.itemText(ind))
        self.vcodec = QString(codecs[key])
#        print 'vcodec = ', self.vcodec.toUtf8()   # Debug

    def width_update(self):
        self.width = self.ledit_w.text()
#        print self.width # Debug
    
    def height_update(self):
        self.height = self.ledit_h.text()
#        print self.height # Debug
    
    def res_update(self):
        if self.check_res.isChecked():
            self.ledit_w.setEnabled(True)
            self.ledit_h.setEnabled(True)
            self.ledit_h.setStyleSheet('background-color: white; color = black')
            self.ledit_w.setStyleSheet('background-color: white; color = black')
            
        else:
            self.ledit_w.setEnabled(False)
            self.ledit_h.setEnabled(False)
            self.ledit_h.setStyleSheet('background-color: gray; color = black')
            self.ledit_w.setStyleSheet('background-color: gray; color = black')
            self.ledit_h.clear()
            self.ledit_w.clear()
    
    def convert2(self):
        if not QString.compare(self.input,''):
            os.system('echo "Error: missing input"') # bash in linux
        else:
            self.command = QString('') # clear command
            self.command.append('ffmpeg ') # call the program
            self.command.append('-i "%s" ' % self.input) # input file
            self.command.append('-c:a %s ' % self.acodec) # audio codec
            self.command.append('-c:v %s ' % self.vcodec) # video codec
            self.command.append('-crf %s ' % self.crf) # video quality
            
            if self.check_res.isChecked():
                if not QString.compare(self.vcodec,'copy'):
                    os.system('echo "Error: cannot resize withot encoding video. Please select a video codec."')
                    sys.exit(app.exec_())
                self.command.append('-vf scale=') # resize filter
                if not QString.compare(self.width,'') and not QString.compare(self.height,''):
                    self.command.append('iw:ih ') # do not resize
                elif not QString.compare(self.width,'') and QString.compare(self.height,''):
                    self.command.append('-2:%s ' % self.height) # change height with constant ratio
                elif QString.compare(self.width,'') and not QString.compare(self.height,''):
                    self.command.append('%s:-2 ' % self.width) # change width with constant ratio
                elif QString.compare(self.width,'') and QString.compare(self.height,''):
                    self.command.append('%s:%s ' % (self.width,self.height)) # change height with constant ratio
            
            if not QString.compare(self.output,''):
                self.command.append('output.mp4') # default output
            else:
                self.command.append('"%s"' % self.output) # output file
            
            os.system(str(self.command.toUtf8()))
#            print self.command.toUtf8() # Debug
        
app = QApplication(sys.argv)
win = mainwin()
win.show()

sys.exit(app.exec_())
