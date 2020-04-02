from PIL import Image, ImageDraw

newimg = Image.new('RGB', (400, 400), color='white')
draw = ImageDraw.Draw(newimg)



newimg.save('red.png')
