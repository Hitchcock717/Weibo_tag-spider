#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
"""
weibo tag analysis
"""

import codecs
import re


class TagAnalysis(object):
    def __init__(self):
        pass

    def read(self, f):
        fin = codecs.open(f, 'r', encoding='utf-8')
        data = []
        for fi in fin.readlines():
            fii = fi.replace(' ', '')
            data.append(fii)
        return data

    def clean(self, f):
        raw_data = self.read(f)
        clean_data = [eval(x) for x in raw_data]
        frequency, tags = [], []
        for d in clean_data[0]:
            frequency.append(d['nick'])
            if d['tags'] != 'N/A':
                tags.extend(d['tags'])
        print('爬取用户数为%s' % len(frequency))
        sorted_li = self.sort(frequency)
        print('标签总数为%s' % len(sorted_li))
        print('top10标签为%s' % sorted_li[:10])
        return clean_data, len(frequency)

    def sort(self, example):
        count_dict = {}
        for ex in example:
            if ex in count_dict:
                count_dict[ex] += 1
            else:
                count_dict[ex] = 1
        sorted_li = sorted(count_dict.items(), key=lambda item: item[1], reverse=True)
        return sorted_li

    def calculate(self, f):
        clean_data, total = self.clean(f)[0], self.clean(f)[1]
        average_concern = self.average(clean_data, total, key='concerns')
        average_fans = self.average(clean_data, total, key='fans')
        average_posts = self.average(clean_data, total, key='posts')
        print('二次元平均关注数为%s' % average_concern)
        print('二次元平均粉丝数为%s' % average_fans)
        print('二次元平均发博数为%s' % average_posts)

    def average(self, data, total, key):
        sum = 0
        for c in data[0]:
            if c[key] != 'N/A':
                if re.search('万', c[key]):
                    c[key] = int(re.sub('万', '', c[key])) * 10000
                    sum += c[key]
                else:
                    if c[key].isdigit():
                        sum += int(c[key])
        average = round(sum / total, 2)
        return average

    def degree(self, f):
        clean_data = self.clean(f)[0]
        education, work = [], []
        for d in clean_data[0]:
            if d['education'] != 'N/A':
                education.append(d['education'])
            if d['work'] != 'N/A':
                work.append(d['work'])
        print('爬取教育信息数为%s' % len(set(education)))
        print('爬取职位信息数为%s' % len(set(work)))
        sorted_li = self.sort(education)
        sorted_li1 = self.sort(work)
        for s in sorted_li1:
            if re.search('合作|无', s[0]):
                sorted_li1.remove(s)
        print('top10教育信息为%s' % sorted_li[:10])
        print('top10职业信息为%s' % sorted_li1[:11])

    def classify(self, f):
        clean_data = self.clean(f)[0]
        filter, core, subcore, left = [], [], [], []
        new_data = clean_data[0]
        for d in new_data:
            if d['fans'] and d['posts'] != 'N/A':
                if re.search('万', d['fans']) or re.search('万', d['posts']):
                    d['fans'] = str(int(re.sub('万', '', d['fans'])) * 10000)
                    d['posts'] = str(int(re.sub('万', '', d['posts'])) * 10000)
            else:
                new_data.remove(d)
        for s in new_data:
            if s['fans'].isdigit() and s['posts'].isdigit():
                filter.append(s)
        print('过滤后总用户数%s' % len(filter))
        for d in filter:
            if int(d['fans']) > 10000 and int(d['posts']) > 1000:
                core.append(d)
            if d['fans'] != 'N/A' and 10000 > int(d['fans']) > 1000 and 1000 > int(d['posts']) > 100:
                subcore.append(d)

        print('核心用户数为%s' % (len(core)/len(filter)))
        print('次核心用户数为%s' % (len(subcore)/len(filter)))
        print('普通用户数为%s' % (len(filter) - (len(core) + len(subcore))))

        return core

    def core(self, f):
        core = self.classify(f)
        core_tag = []
        for c in core:
            if c['tags'] != 'N/A':
                core_tag.extend(c['tags'])
        sort = self.sort(core_tag)
        print(sort[:10])

if __name__ == '__main__':
    tag = TagAnalysis()
    tag.core(f='/Users/linjue/Desktop/erciyuan_data.txt')
