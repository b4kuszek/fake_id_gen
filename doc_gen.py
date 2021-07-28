import PIL
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import os
import matplotlib.pyplot as plt
from mrz.generator.td1 import TD1CodeGenerator
from tqdm import tqdm
import random
from random import choice
from copy import copy
import json


def load_fonts(root):
    fonts = {}
    fonts['names'] = ImageFont.truetype(os.path.join(root, 'arialbi.ttf'), 125)
    fonts['other_front_data'] = ImageFont.truetype(os.path.join(root, 'arialbi.ttf'), 115)
    fonts['can'] = ImageFont.truetype(os.path.join(root, 'ocrb_regular.ttf'), 150)
    fonts['pesel'] = ImageFont.truetype(os.path.join(root, 'arialbi.ttf'), 34)
    fonts['mrz'] = ImageFont.truetype(os.path.join(root, 'ocrb_regular.ttf'), 29)
    fonts['id_number'] = ImageFont.truetype(os.path.join(root, 'arial.ttf'), 20)
    fonts['issue_date'] = ImageFont.truetype(os.path.join(root, 'arial.ttf'), 14)
    fonts['other_back_data'] = ImageFont.truetype(os.path.join(root, 'arial.ttf'), 17)

    return fonts


def load_original_images(root, image_names):
    front, back = image_names
    front_image = Image.open(os.path.join(root, front))
    back_image = Image.open(os.path.join(root, back))
    return front_image, back_image
 

def paste_image(root_image, image_name, root_original):
    img = Image.open(os.path.join(root_image, image_name))#.convert('LA')
    image = img.copy()
    image.putalpha(180)
    # image = image.filter(ImageFilter.GaussianBlur(radius=1))
    # image = ImageEnhance.Contrast(image).enhance(1.5)
    # image = image.rotate(random.randint(-30,30))
    # image = image.filter(ImageFilter.GaussianBlur(radius=100))
    # plt.imshow(image)
    # plt.show()

    # plt.imshow(image)
    # plt.show()
    front_image, back_image = load_original_images(root_original, ('TEMPLATE_FRONT_ORIGINAL.jpg', 'TEMPLATE_BACK_BARCODE.jpg' ))
    front_image.putalpha(255)
    back_image.putalpha(255)

    offsets = [
        (460, 1000),
        (3350, 1600),
        (630, 150)
    ]

    image = image.resize((1000,1330))
    front_image_part = front_image.crop([460, 1000, 460+1000, 1000+1330])
    image = Image.alpha_composite(front_image_part, image)
    imageg = ImageOps.grayscale(image)
    front_image.paste(imageg, offsets[0])
    
    image = image.resize((450,540))
    front_image_part = front_image.crop([3350, 1600, 450+3350, 540+1600])    
    image = Image.alpha_composite(front_image_part, image)
    imageg = ImageOps.grayscale(image)
    front_image.paste(imageg, offsets[1])

    image = image.resize((90, 100))
    back_image_part = back_image.crop([630, 150, 630+90, 150+100])
    image = Image.alpha_composite(back_image_part, image)
    imageg = ImageOps.grayscale(image)
    back_image.paste(imageg, offsets[2]) 

    return front_image, back_image


def add_data(images, data):
    fonts = load_fonts('/home/notkacper/fake_id_gen/font_mrz')
    front_image, back_image = images

    front_image_editable = ImageDraw.Draw(front_image)
    back_image_editable = ImageDraw.Draw(back_image)

    # SURNAME
    front_image_editable.text((1600, 740), data['surname'], (0,0,0), font=fonts['names'])
    # NAME 
    front_image_editable.text((1600, 1080), data['name'], (0,0,0), font=fonts['names'])
    # NATIONALITY 
    front_image_editable.text((1600, 1365), data['nationality'], (0,0,0), font=fonts['other_front_data'])
    # DATA OF BIRTH 
    front_image_editable.text((2840, 1365), data['birth'], (0,0,0), font=fonts['other_front_data'])
    # ID NUMBER 
    front_image_editable.text((1600, 1720), data['id_number'], (0,0,0), font=fonts['other_front_data'])
    # SEX
    front_image_editable.text((2830, 1630), data['sex'], (0,0,0), font=fonts['other_front_data'])
    # EXPIRY DATE
    front_image_editable.text((1600, 1980), data['expiry'], (0,0,0), font=fonts['other_front_data'])
    # CAN
    front_image_editable.text((3340, 2380), data['can'], (0,0,0), font=fonts['can'])


    # PESEL
    back_image_editable.text((48,60), data['pesel'], (0,0,0), font=fonts['pesel'])
    # PLACE OF BIRTH
    back_image_editable.text((48,113), data['birth_place'], (0,0,0), font=fonts['other_back_data'])
    # FAMILY NAME
    back_image_editable.text((48,165), data['family_name'], (0,0,0), font=fonts['other_back_data'])
    # PARENTS NAMES
    back_image_editable.text((48,205), data['parents'], (0,0,0), font=fonts['other_back_data'])
    # ISSUING AUTHORITHY
    back_image_editable.text((48,245), data['authority'], (0,0,0), font=fonts['other_back_data'])
    # ID NUMBER
    back_image_editable.text((520,90), data['id_number'][:3] + '  ' + data['id_number'][3:], (0,0,0), font=fonts['id_number'])
    # DATE OF ISSUE
    back_image_editable.text((515,205), data['issue_date'], (0,0,0), font=fonts['issue_date'])
    # MRZ
    back_image_editable.text((60, 340), data['mrz'], (0,0,0), font=fonts['mrz'])

    return front_image, back_image


def generate():
    def date_transform(data):
        date =  data[-2:] + data[3:5] + data[0:2]
        return date

    #for i, file_name in tqdm(enumerate(os.listdir(r'C:\Users\gkrzy\OneDrive\Pulpit\praca\ludzie_nieistniejący'))):
    for i in tqdm(range(130,10000)):
        print(i)
        file_name = choice(os.listdir('/home/notkacper/fake_id_gen/photos'))

        images = paste_image('/home/notkacper/fake_id_gen/photos', file_name, '/home/notkacper/fake_id_gen/wzory')

        random_surname = choice(['KLUZKA', 'ANIHILACJA', 'MEDUZA', 'DŻORŻ', 'CZESTER', 'ŁINCZESTER', 'CZARMOWSKI', 'KOKULSKI', 'PODLASKOWICZ', 'BEZPRZEWODOWY'])
        random_name = choice(['MILF', 'DONICZKA', 'KABLEK', 'SZYMON', 'HERMENEGILDA', 'ANJA', 'JULIA', 'HUBERT'])
        random_sex = choice(['M', 'F'])
        random_auth = choice(['MISS DOLNEGO ŚLĄSKA', 'PREZYDENT POLSKI', 'POLSKI PREZYDENT', 'PAN ZDZISIEK'])

        data = {
            'surname' : random_surname,
            'name' : random_name,
            'nationality' : 'POLSKIE',
            'id_number' : 'EZA976380',
            'expiry' : '21.02.2024',
            'birth' : '14.01.1969',
            'sex' : random_sex,
            'can' : '817379',
            'pesel' : '69011406650' if random_sex == 'M' else '69011421743',
            'birth_place' : 'BIAŁA PODLASKA',
            'family_name' : random_surname,
            'parents' : 'MARIA JARSOŁAW',
            'authority' : random_auth,
            'issue_date' : '21.02.2014',
        }

        mrz = TD1CodeGenerator('I', 'POL', data['id_number'], date_transform(data['birth']),
            data['sex'], date_transform(data['expiry']), data['nationality'][:3], data['surname'], data['name'], optional_data2=data['pesel'])

        data['mrz'] = mrz.__str__()



        # fw, fh = front_image.size
        # bw, bh = back_image.size
        #
        # f_scalar = 0.1*random.randint(9,10)
        # front_image = front_image.resize((int(f_scalar*front_image.size[0]), int(f_scalar*front_image.size[1])))
        # back_image = back_image.resize((int(f_scalar*back_image.size[0]), int(f_scalar*back_image.size[1])))
        # background = Image.open(r'C:\Users\gkrzy\OneDrive\Pulpit\praca\gazety\\' + choice(os.listdir(r'C:\Users\gkrzy\OneDrive\Pulpit\praca\gazety')))
        #
        # background_scalar = 1.15
        # front_background = background.resize((int(background_scalar*fw), int(background_scalar*fh)))
        # back_background = background.resize((int(background_scalar*bw), int(background_scalar*bh)))
        #
        # front_background = front_background.rotate(random.randint(-3,3))
        # back_background = back_background.rotate(random.randint(-3,3))
        #
        # # front_background = Image.new('RGB', (int(2*front_image.size[0]), int(2*front_image.size[1])), color='white')
        # # back_background = Image.new('RGB', (int(2*back_image.size[0]), int(2*back_image.size[1])), color='white')
        #
        # width_coeff = 0.01*random.randint(5,13)
        # height_coeff = 0.01*random.randint(5,13)
        # front_background.paste(front_image, (int(width_coeff*front_background.size[0]), int(height_coeff*front_background.size[1])))
        # back_background.paste(back_image, (int(width_coeff*back_background.size[0]), int(height_coeff*back_background.size[1])))

        # front_background = front_background.filter(ImageFilter.GaussianBlur(radius=4))
        # back_background = back_background.filter(ImageFilter.GaussianBlur(radius=4))

        data = {
            'surname': 'małeDUŻE',
            'name': 'DUZEmałeDUZE',
            'nationality': 'POLSKIE',
            'id_number': 'EZA976380',
            'expiry': '21.02.2024',
            'birth': '14.01.1969',
            'sex': 'M',
            'can': '817379',
            'pesel': '69011406650',
            'birth_place': 'BIAŁA PODLASKA',
            'family_name': '?????????????',
            'parents': 'MARIA JARSOŁAW ANNA HENIO',
            'authority': 'PAPUGA',
            'issue_date': '21.02.2014',
        }

        front_image, back_image = add_data(images, data)

        # with open(fr'D:\data\front{i}', 'w') as outfile:
        #     json.dump(data_front, outfile)
        # with open(fr'D:\data\back{i}', 'w') as outfile:
        #     json.dump(data_back, outfile)

        front_image.save(fr'D:\data\front{i}.png')
        back_image.save(fr'D:\data\back{i}.png')


def single_gen():
    def date_transform(data):
        date = data[-2:] + data[3:5] + data[0:2]
        return date

    images = paste_image( '/home/notkacper/fake_id_gen/photos', 'grzempagarbocz.jpeg' , '/home/notkacper/fake_id_gen/wzory')

    print(type(images))

    data = {
        'surname' : 'małeDUŻE',
        'name' : 'DUŻEmałeDUŻE',
        'nationality' : 'POLSKIE',
        'id_number' : 'EZA976380',
        'expiry' : '21.02.2024',
        'birth' : '14.01.1969',
        'sex' : 'M',
        'can' : '817379',
        'pesel' : '690II406650',
        'birth_place' : 'BIAŁA PODLASKA',
        'family_name' : '?????????????',
        'parents' : 'MARIA JARSOŁAW',
        'authority' : 'PAPUGA',
        'issue_date' : '21.02.2014',
    }

    mrz = TD1CodeGenerator('I', 'POL', data['id_number'], date_transform(data['birth']),
        data['sex'], date_transform(data['expiry']), data['nationality'][:3], data['surname'], data['name'], optional_data2='69011406650')


# to zmieniać tylko i wyłącznie :P (zmiana wyglądu)
    data = {
        'surname' : 'małeDUŻE',
        'name' : '诶	A	ēi',
        'nationality' : 'POLSKIE',
        'id_number' : 'EZA976380',
        'expiry' : '21.02.2024',
        'birth' : '14.01.1969',
        'sex' : 'M',
        'can' : '817379',
        'pesel' : '69011406650',
        'birth_place' : 'BIAŁA PODLASKA',
        'family_name' : '?????????????',
        'parents' : 'MARIA JARSOŁAW ANNA HENIO',
        'authority' : 'PAPUGA',
        'issue_date' : '21.02.2014',
        #'mrz' : ''
    }

    data['mrz'] = mrz.__str__()

    front_image, back_image = add_data(images, data)

    front_image.save('/home/notkacper/fake_id_gen/nudesygrzempy/front3.png')
    back_image.save('/home/notkacper/fake_id_gen/nudesygrzempy/back3.png')


if __name__ == "__main__":
    single_gen()
    