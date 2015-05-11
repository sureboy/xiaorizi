# -*- coding: utf-8 -*-
"""
Created on Wed Feb 04 10:33:45 2015

@author: sooshian
"""
import json

class sponsor_feature(object):
    TYPE_NONE = 0
    TYPE_EMAIL = 1
    TYPE_PHONE = 2
    

    def __init__(self, feature_string=None):
        if not feature_string:
            self.feature_dict = {}
        else:
            try:
                self.feature_dict = json.loads(feature_string)
            except ValueError:
                self.feature_dict = {}
    
    def __unicode__(self,):
        return json.dumps(self.feature_dict)
        
    def __str__(self,):
        return self.__unicode__()
        
    def add_item(self, name, v, t=None, w=1.0):
        if not t:
            t = sponsor_feature.TYPE_NONE
        if name in self.feature_dict:
            self.feature_dict[name]['value'].append(v)
        else:
            self.feature_dict[name] = {'value': [v], 'type': t, 'weight': w}

    @staticmethod
    def compare(f_item_1, f_item_2):
        if f_item_1['type'] == f_item_2['type']:
            #w = f_item_1['weight']
            s = 0
            for x in f_item_1['value']:
                for y in f_item_2['value']:
                    if x == y:
                        s = 1
            return s
        else:
            return None
    
    def similarity(self, other_feature):
        if len(self.feature_dict) <= len(other_feature.feature_dict):
            small_one = self
            big_one = other_feature
        else:
            small_one = other_feature
            big_one = self
        
        a = 0
        #print small_one, big_one
        for fn in big_one.feature_dict:
            a += big_one.feature_dict[fn]['weight']
        
        if a == 0:
            return 0
        c = 0
        for feature_name in small_one.feature_dict:
            if feature_name in big_one.feature_dict:
                i1 = small_one.feature_dict[feature_name]
                i2 = big_one.feature_dict[feature_name]
                w = i1['weight']
                r = sponsor_feature.compare(i1, i2)
                c += w * r

        return c / float(a)

if __name__ == '__main__':
    """
    sf = sponsor_feature()
    sf.add_item('email', '443022228@qq.com', sponsor_feature.TYPE_EMAIL)
    sf.add_item('email', '1')
    sf2 = sponsor_feature(unicode(sf))
    print sf2
       """
    sf1 = sponsor_feature()
    sf1.add_item('email', 'b@qq.com')
    sf1.add_item('email', 'a@qq.com')
    sf1.add_item('phone', '123')
    sf3 = sponsor_feature(unicode(sf1))
    sf2 = sponsor_feature()                    
    sf2.add_item('email', 'a@qq.com')
    sf2.add_item('phone', '23')
    
    print sf3.similarity(sf2)
