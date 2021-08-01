import os
import re
from datetime import datetime

import unreal

# Project root path
ROOT_PATH = 'F:/github/ue4py'

CURRENT_TIME = datetime.now().strftime('%y%m%d%H%M%S')
print(CURRENT_TIME)

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
    long_name = False

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
            # 'Name': self.tex2d.get_name(),
            self.name,
            self.srgb,
            self.address_x,
            self.address_y,
            self.source_file,
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
        detail.long_name = True
        detail.property_value = '%s' % self.tex2d.get_name()
        detail.display_name = detail.property_value
        return detail

    @property
    def source_file(self):
        detail = Detail()
        detail.property_name = 'asset_import_data'
        detail.property_display_name = 'Source File'
        detail.long_name = True
        detail.property_value = self.tex2d.get_editor_property(detail.property_name)
        detail.display_name = detail.property_value.get_first_filename()
        return detail


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
            print(test11.name.display_name)
            for ppp in detail:
                print('\t%s:>%s<' % (ppp.property_display_name, ppp.display_name))

            # print(item.get_editor_property('address_x'))


def set_html_list():
    tex2d_infos = Texture2DInfos()

    content = ' \n'
    content += '<table id="tableSort">\n'
    content += '\t<thead>\n'
    content += '\t<tr>\n'

    details = tex2d_infos.details
    details[0].detail
    property_display_name_list = details[0].property_display_name_list

    for prop_display_name in property_display_name_list:
        content += '''\t<th onclick="$.sortTable.sort('tableSort',0)" style="cursor: pointer;">%s</th>\n''' % (
            prop_display_name)
    content += '\t<tr>\n'
    content += '</thead>\n'
    content += '<tbody>\n'

    for tex2d_info in details:
        tex2d_info_detail = tex2d_info.detail
        content += '<tr>\n'

        for prop in tex2d_info_detail:
            if prop.long_name:
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
    content = re.sub(r'{{ project_root_path }}', ROOT_PATH, content)
    # save_html_path = os.path.join(qyzpath.temp_dir, 'jointsDetails.html')
    save_html_path = r'd:\temp.html'
    with open(save_html_path, 'w') as f:
        f.write(content)
    os.startfile(save_html_path)
    return content


set_page(set_html_list(), '', '')
