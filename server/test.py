from lib.meter import MeterOCR

folder="uploads/80aef8b0-5291-49cf-811e-ed3e33d29427/"
img='80aef8b0-5291-49cf-811e-ed3e33d29427.jpg'

mocr = MeterOCR(img,folder,debug=True)
res = mocr.process()
print([r[0] for r in res])

