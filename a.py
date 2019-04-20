from PIL.Image import *

def fonctionEscalier(i, n):
	(l, h)=i.size
	for y in range(h):
		for x in range(l):
			c = Image.getpixel(i, (x, y))
			min = True
			j=1
			while(j<n and min==True):
				indice = (j*256)//n
				if(c<indice):
					ind = ((j-1)*256)//n
					Image.putpixel(i, (x, y), ind)
					min=False
				j+=1
			if (min==True):
				Image.putpixel(i, (x, y), 255)
	return i
					