from PIL import Image


im = Image.open(r'C:\Users\Administrator\CUSTOMUETEMP\TEMP_IMG\新建文件夹\Game\StarterContent\Textures\T_Brick_Clay_Beveled_D.TGA')

im = im.convert('RGB')

im.save(r'C:\Users\Administrator\Desktop\test_2.jpg', compression=None)


def test_fff():
    print(111)
