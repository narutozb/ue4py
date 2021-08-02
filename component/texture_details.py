import os
import re
from datetime import datetime

from PIL import Image

import unreal

# Path
# Tools project root path
ROOT_PATH = 'F:/github/ue4py'

# User temp folder
HOME = os.path.expanduser('~')

#
TEMP_FOLDER = os.path.join(HOME, 'CUSTOMUETEMP')
if not os.path.exists(TEMP_FOLDER):
    os.mkdir(TEMP_FOLDER)

#
TEMP_IMG_FOLDER = os.path.join(TEMP_FOLDER, 'TEMP_IMG')
if not os.path.exists(TEMP_IMG_FOLDER):
    os.mkdir(TEMP_IMG_FOLDER)

TEMP_PREVIEW_IMG = os.path.join(TEMP_FOLDER, 'TEMP_PREVIEW_IMG')
if not os.path.exists(TEMP_IMG_FOLDER):
    os.mkdir(TEMP_IMG_FOLDER)

# UE project 's content path
CONTENT_PATH = unreal.Paths.project_content_dir()

# current time
CURRENT_TIME = datetime.now().strftime('%y%m%d%H%M%S')

# Texture object's class list
TEXTURE_CLASS = {
    'Texture2D': unreal.Texture2D,
}

# texture_address_reference
texture_address_reference = ['Wrap', 'Clamp', 'Mirror']


class Name(object):
    '''
    display name
    '''
    display_name = ''
    property_display_name = ''
    zh_cn = ''
    ja_jp = ''
    # set path or long type
    is_long_name = False

    # is display?
    is_display = True

    def __init__(self):
        pass


class Detail(Name):
    # set value
    __value = ''
    property_name = ''

    def __init__(self, ):
        ''''''
        super().__init__()

    def __get_prop_value(self):
        return self.__value

    def __set_prop_value(self, value):
        self.__value = value

    property_value = property(__get_prop_value, __set_prop_value)


class Texture2DInfo(Detail):

    def __init__(self, texture):
        '''
        '''
        super().__init__()
        self.tex2d = texture
        self.property_display_name_list = []

    @property
    def detail(self):
        res = [
            self.name,
            self.asset_full_path,
            self.srgb,
            self.address_x,
            self.address_y,
            self.texture_size_x,
            self.texture_size_y,
            self.source_file,
            self.referencers_for_asset,
        ]
        self.property_display_name_list = [item.property_display_name for item in res]

        return res

    @property
    def address_x(self):
        detail = Detail()
        detail.property_name = 'address_x'
        detail.property_display_name = 'X-axis Tiling Method'
        detail.property_value = self.tex2d.get_editor_property(detail.property_name)
        for item in texture_address_reference:
            match = re.match(r'.*?%s.*?' % item, str(detail.property_value), re.I)
            if match:
                detail.display_name = item
                return detail
        return

    @property
    def address_y(self):
        detail = Detail()
        detail.property_name = 'address_y'
        detail.property_display_name = 'Y-axis Tiling Method'
        detail.property_value = self.tex2d.get_editor_property(detail.property_name)
        for item in texture_address_reference:
            match = re.match(r'.*?%s.*?' % item, str(detail.property_value), re.I)
            if match:
                detail.display_name = item
                return detail
        return

    @property
    def srgb(self):
        detail = Detail()
        detail.property_value = self.tex2d.srgb
        detail.property_name = 'srgb'
        detail.property_display_name = 'sRGB'
        detail.display_name = '%s' % detail.property_value
        return detail

    @property
    def name(self):
        detail = Detail()
        detail.property_name = 'Name'
        detail.property_display_name = 'Asset Name'
        detail.is_long_name = True
        detail.property_value = '%s' % self.tex2d.get_name()
        detail.display_name = detail.property_value
        return detail

    @property
    def source_file(self):
        detail = Detail()
        detail.property_name = 'asset_import_data'
        detail.property_display_name = 'Source File'
        detail.is_long_name = True
        detail.property_value = self.tex2d.get_editor_property(detail.property_name)
        set_display_name = re.sub(r'\\', '/', detail.property_value.get_first_filename())
        match = re.match(r'(\w.*)(/)(\w.*$)', set_display_name)
        if match:
            set_display_name = '%s%s\n%s' % (match.group(1), match.group(2), match.group(3))
        detail.display_name = set_display_name
        return detail

    @property
    def texture_size_x(self):
        detail = Detail()
        detail.property_name = 'blueprint_get_size_x'
        detail.property_display_name = 'Texture Size X'
        detail.property_value = self.tex2d.blueprint_get_size_x()
        detail.display_name = detail.property_value
        return detail

    @property
    def texture_size_y(self):
        detail = Detail()
        detail.property_name = 'blueprint_get_size_y'
        detail.property_display_name = 'Texture Size Y'
        detail.property_value = self.tex2d.blueprint_get_size_x()
        detail.display_name = detail.property_value
        return detail

    @property
    def asset_full_path(self):
        detail = Detail()
        path_name = re.sub(r'\.\w.*', '', self.tex2d.get_path_name())
        detail.property_value = self.tex2d.get_path_name()
        set_display_name = re.sub('^/Game/', CONTENT_PATH + '\n', path_name)
        detail.display_name = set_display_name
        detail.property_display_name = 'Full Path'
        detail.is_long_name = True
        return detail

    @property
    def referencers_for_asset(self):
        detail = Detail()
        detail.property_display_name = 'Referencers'
        detail.property_value = unreal.EditorAssetLibrary.find_package_referencers_for_asset(self.tex2d.get_path_name())
        set_display_name = ''
        for item in detail.property_value:
            set_display_name += re.sub('^/Game/', '\n', item)
        if not set_display_name:
            set_display_name = 'None'
        detail.display_name = set_display_name
        detail.is_long_name = True
        return detail

    @property
    def img_preview_path(self):
        return re.sub(r'\.\w.*', '', self.tex2d.get_path_name())


class Texture2DInfos(Texture2DInfo):

    def __init__(self):
        '''

        '''
        self.tex2d_list = unreal.EditorUtilityLibrary.get_selected_assets()

    @property
    def details(self):
        tex2d_details = []

        for tex2d in self.tex2d_list:
            tex2d_details.append(Texture2DInfo(tex2d))

        return tex2d_details


def get_texture_assets():
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    for item in selected_assets:
        if item.__class__ in list(TEXTURE_CLASS.values()):
            test11 = Texture2DInfo(item)
            detail = test11.detail
            # print(test11.name.display_name)
            for ppp in detail:
                print('\t%s:>%s<' % (ppp.property_display_name, ppp.display_name))


def set_html_list():
    # Get Texture2dInfos
    tex2d_infos = Texture2DInfos()

    details = tex2d_infos.details
    # get property display name list
    details[0].detail
    property_display_name_list = details[0].property_display_name_list

    # set html content
    content = ' \n'
    content += '<table id="tableSort">\n'
    content += '\t<thead>\n'
    content += '\t<tr>\n'

    content += '''\t<th onclick="$.sortTable.sort('tableSort',0)" style="cursor: pointer;">Image</th>\n'''
    for prop_display_name in property_display_name_list:
        content += '''\t<th onclick="$.sortTable.sort('tableSort',0)" style="cursor: pointer;">%s</th>\n''' % (
            prop_display_name)
    content += '\t<tr>\n'
    content += '</thead>\n'
    content += '<tbody>\n'

    for tex2d_info in details:
        tex2d_info_detail = tex2d_info.detail
        content += '<tr>\n'

        content += '\t\t<td><img src=file:///%s.jpg></td>\n' % (
                TEMP_PREVIEW_IMG.replace('\\', '/') + tex2d_info.img_preview_path)
        for prop in tex2d_info_detail:
            if prop.is_long_name:
                set_class_mark = 'class="LongName"'
            else:
                set_class_mark = ''

            content += '\t\t<td %s>%s</td>\n' % (set_class_mark, prop.display_name)

        content += '\n'
        content += '</tr>\n'
    content += '</tbody>\n'
    content += '</table>'
    return content


def set_page(li, sub_title, instruction):
    with open('%s/templates/query/query_info_template.html' % ROOT_PATH, 'r') as f:
        content = f.read()

    content = re.sub(r'{{ content }}', li, content)
    content = re.sub(r'{{ sub_title }}', sub_title, content)
    content = re.sub(r'{{ instruction }}', instruction, content)
    content = re.sub(r'{{ project_root_path }}', ROOT_PATH.replace('\\', '/'), content)
    # save_html_path = os.path.join(qyzpath.temp_dir, 'jointsDetails.html')
    save_html_path = os.path.join(TEMP_FOLDER, 'texture_details.html')
    with open(save_html_path, 'w') as f:
        f.write(content)
    os.startfile(save_html_path)
    return content


def excute_import_tasks(textures):
    unreal.AssetToolsHelpers.get_asset_tools().export_assets(textures, export_path=TEMP_PREVIEW_IMG)

    for item in textures:
        path_original = os.path.normpath('%s%s' % (TEMP_PREVIEW_IMG, item.get_path_name()))

        match = re.match(r'(\w.*\.)(\w.*)', path_original)
        if match:
            tga_texture_path = '%s%s' % (match.group(1), 'TGA')

        convert_to_jpg(tga_texture_path)


def convert_to_jpg(tga_texture_path):
    im = Image.open(tga_texture_path)
    # print('Opening:%s' % tga_texture_path)

    # Get save path
    save_jpg_path = re.sub(r'\.TGA$', '.jpg', tga_texture_path)

    # Resize image
    im = im.resize((256, 256))

    # Convert to RGB
    im = im.convert('RGB')

    # Save Image
    im.save(save_jpg_path, compression=None)
    os.remove(tga_texture_path)


selected = unreal.EditorUtilityLibrary.get_selected_assets()
excute_import_tasks(selected)
set_page(set_html_list(), '', '')

# for item in selected:
#     referenced_assets = unreal.EditorAssetLibrary.find_package_referencers_for_asset(item.get_path_name())
#     print(item.get_fname())
#     for refed_asset in referenced_assets:
#         print('\t%s:%s'%(refed_asset, refed_asset.__class__))
