class newppm:
	def __init__(self, filename, height, width, maxn=255, valspace=1, pixelspace=2, lineEndLength=2, formatPedantically=False):
		self.lineEndLength = lineEndLength
		self.formatPedantically = formatPedantically
		#the minimum whitespace between values
		self.valspace = 1
		#extra whitespace between pixels
		self.pixelspace = 2

		#array of the pixel data. Dimensions: [height][width][3]
		self.array = []

		if filename.endswith(".ppm"):
			filename = filename[:-4]
		self.file = open(filename + ".ppm", 'w')
		self.width = width
		self.height = height
		self.magic = "P3\n" #line 1. File type. plain ASCII
		self.note = "# " + filename + ".ppm\n" #line 2. Comment. Contains filename
		self.dim = str(width) + " " + str(height) +"\n" #line 3. Space separated width and height
		self.maxn = maxn 
		self.maxcol = str(self.maxn) + "\n" #line 4. The maximum colourant value.

		#each pixel will be padded with whitesapce to this width.
		self.numform = len(str(maxn)) + self.valspace

		self.file.write(self.magic + self.note + self.dim + self.maxcol)

		#offset to beginning of pixels.
		self.blength = len(self.magic + self.note + self.dim + self.maxcol) + 4*(self.lineEndLength-1)
		print(self.blength,len(self.magic + self.note + self.dim + self.maxcol),4*(self.lineEndLength-1))
		self.empty()
	def toPixel(self, row, col):
		#moves the file editing/reading index to the pixel at (row, col)

		position = self.blength
		position += row*(self.width*(3*self.numform + self.pixelspace) + self.lineEndLength)
		position += col*(3*self.numform + self.pixelspace)
		self.file.seek(position)
	def edit(self, row, col, pixel):
		#changes the value of 1 pixel to 'pixel' (array of length 3)

		self.toPixel(row, col)
		self.array[row][col] = pixel[:]
		for i in range(3):
			dig = str(pixel[i])
			self.file.write(" "*(self.numform - len(dig)) + dig)
	def input(self, arr):
		#overwrites ppm with input array (arr)

		self.array = arr[:]
		self.rewrite()
	def colRect(self, r, c, w, h, colour):
		#colors every pixel of a rectangle as 'pixel'
		#rectangle of width w, height h, and top-left corner row r, column c.

		for row in range(h):
			for col in range(w):
				self.edit(r + row, c + col, colour)
	def empty(self):
		#rewrites entire file as black (0, 0, 0)
		self.array = [[[0, 0, 0] for i in range(self.width)] for ii in range(self.height)]
		self.rewrite()
	def rewrite(self):
		#writes the pixel data in self.array to the file

		self.file.seek(self.blength)
		for row in range(self.height):
			for col in range(self.width):
				for i in range(3):
					dig = str(self.array[row][col][i])

					self.file.write(" "*(self.numform - len(dig)) + dig)
				self.file.write(" "*self.pixelspace)
				if self.formatPedantically:
				    #Print a newline after every triple to avoid going over the 70 character limit
				    #Most definitely overkill - but bettter then underkill
				    #The file is still readable however, as there will be a double newline after the end of a row
                                    self.file.write('\n')
			self.file.write('\n')
	def close(self):
		self.file.close()
class openppm:
	def __init__(self, filename, valspace=1, pixelspace=2, lineEndLength=2, formatPedantically=False):
		self.lineEndLength = lineEndLength
		self.formatPedantically = formatPedantically

		#the minimum space between individual pixel values
		self.valspace = valspace
		#extra spacing between values of different pixels
		self.pixelspace = pixelspace

		#array of the ppm's pixel data. Dimensions will be: [height][width][3]
		self.array = []

		if (filename.endswith('.ppm')):
			filename = filename[:-4]

		self.file = open(filename + '.ppm', 'r+')
		data = self.file.readlines()
		self.magic = data[0]
		self.note = data[1]
		self.dim = data[2]
		self.maxcol = data[3]

		#a 1-dimensional array of all the pixel values in order
		self.pureData = []
		for i in data[4:]:
			try:
				line = i.strip()
				elements = line.split()
				end = False
				for num in elements:
					try:
						num = int(num)
						self.pureData.append(num)
					except:
						end = True
						break
				if end:
					break
			except:
				break


		#offset of the start of the file's pixel data
		self.blength = len(self.magic + self.note + self.dim + self.maxcol) + 4*(self.lineEndLength - 1)

		self.width, self.height = self.dim.strip().split()
		self.width = int(self.width)
		self.height = int(self.height)

		self.maxn = int(self.maxcol.strip())

		#each value will be padded with whitespace to be 'numform' characters in length
		self.numform = len(str(self.maxn)) + self.valspace

		self.extractData()
		self.rewrite()
	def extractData(self):
		#process the pixel values in self.pureData into 3-dimensional self.array

		self.array = []
		index = 0
		for row in range(self.height):
			self.array.append([])
			for col in range(self.width):
				self.array[row].append([0,0,0])
				for i in range(3):
					self.array[row][col][i] = self.pureData[index]
					index += 1
	def rewrite(self):
		#writes the pixel data in self.array to the file

		self.file.seek(self.blength)
		for row in range(self.height):
			for col in range(self.width):
				for i in range(3):
					dig = str(self.array[row][col][i])

					self.file.write(" "*(self.numform - len(dig)) + dig)
				self.file.write(" "*self.pixelspace)
				if self.formatPedantically:
				    #Print a newline after every triple to avoid going over the 70 character limit
				    #Most definitely overkill - but bettter then underkill
				    #The file is still readable however, as there will be a double newline after the end of a row
				    self.file.write('\n')
			self.file.write('\n')
		self.file.write('END')
	def input(self, arr):
		#overwrites ppm with input array (arr)

		self.array = arr[:]
		self.rewrite()
	def empty(self):
		#rewrites entire file as black (0, 0, 0)

		self.array = [[[0, 0, 0] for i in range(width)] for ii in range(height)]
		self.rewrite()

	# only use the following functions if the data has been extracted and rewritten
	# i.e. is in the form: 'height' rows of 'width' pixels of 3 vlaues
	# and with 'valspace' whitepace in front of each pixel(which are also padded to
	# 	 number of digits in maxval)
	# and with extra 'pixelspace' whitepace between each pixel (and at end of line)

	def toPixel(self, row, col):
		#moves the file editing/reading index to the pixel at (row, col)

		position = self.blength
		position += row*(self.width*(3*self.numform + self.pixelspace) + self.lineEndLength)
		position += col*(3*self.numform + self.pixelspace)
		self.file.seek(position)
	def edit(self, row, col, pixel):
		#changes the value of 1 pixel to 'pixel' (array of length 3)

		self.toPixel(row, col)
		self.array[row][col] = pixel[:]
		for i in range(3):
			dig = str(pixel[i])

			self.file.write(" "*(self.numform - len(dig)) + dig)
	def colRect(self, r, c, w, h, colour):
		#colors every pixel of a rectangle as 'pixel'
		#rectangle of width w, height h, and top-left corner row r, column c.

		for row in range(h):
			for col in range(w):
				self.edit(r + row, c + col, colour)
	def close(self):
		self.file.close()


