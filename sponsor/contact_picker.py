#! -*- coding:utf-8 -*-

class contact_picker(object):
    scan = 0
    email_address = 1
    phone_number = 2
    email_char_set = None
    
    length_at_least = 7
    def __init__(self,):
        pass
    
    def init_char_set(self,):
        self.email_char_set = []
        for c in range(65, 91):
            self.email_char_set.append(chr(c))
        for c in range(97, 123):
            self.email_char_set.append(chr(c))
        self.email_char_set.append('.')
        self.email_char_set.append('-')
        self.email_char_set.append('_')

    def pick(self, text):
        result = {contact_picker.email_address: [], \
                    contact_picker.phone_number: []}
        pick_mode = contact_picker.scan
        temp = None
        at_found = False
        text = text + "\n"
        for c in text:
            if pick_mode == contact_picker.scan:
                if c in self.email_char_set:
                    temp = c
                    at_found = False
                    pick_mode = contact_picker.email_address
                elif c.isdigit():
                    temp = c
                    pick_mode = contact_picker.phone_number
                else:
                    pass
            elif pick_mode == contact_picker.email_address:
                if c in self.email_char_set:
                    temp += c
                elif c.isdigit():
                    temp += c
                elif c == '@':
                    temp += c
                    at_found = True
                else:
                    if at_found:
                        result[contact_picker.email_address].append(temp)
                    pick_mode = contact_picker.scan
            elif pick_mode == contact_picker.phone_number:
                if c.isdigit() or c == '-':
                    temp += c
                else:
                    if len(temp) >= contact_picker.length_at_least:
                        result[contact_picker.phone_number].append(temp)
                    pick_mode = contact_picker.scan
                
        return result

if __name__ == '__main__':
    text = u'中国城市规划学会城市交通规划学术委员会； \
        联系人： 张宇 电话：010-58323221 赵小云 \
        电话：010-58323110 电子邮箱：cutpa@qq.com'

    text2 = u'中国海洋大学、中国科学院海洋研究所； \
        联系人：张晓华教授 （中国海洋大学海洋生命学院） \
        Email: xhzhang1965@163.com Tel/Fax: \
        0086-532-82032767; Mobile: 0086-13606428332'
    text3 = u'方法一 打电话到门店 \
            3Garden的电话是：021-54655690 \
            工作时间为：10:00am-9:00pm \
                    \
            方法二 \
            给我们发邮件 \
            3Garden E-mail \
            sh_3garden@qq.com  '
    p = contact_picker()
    p.init_char_set()
    print p.pick(text3)
