#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
"""
crawl weibo circle tag
"""

import re
from bs4 import BeautifulSoup
from DecryptLogin import login


class WeiboTag(object):

    def __init__(self, username, password):
        self.circle1 = '古风'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

        self.timeout = 10
        self.session = WeiboTag.decrypt_login(username, password)

    @staticmethod
    def decrypt_login(username, password):
        lg = login.Login()
        infos_return, session = lg.weibo(username, password, 'pc')
        return session

    def start_requests(self):
        data = []
        for pid in range(1, 51):
            url = 'https://s.weibo.com/user/&tag=' + self.circle1 + '&from=profile&wvr=6&page=' + str(pid)
            r = self.session.get(url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(r.text, 'html.parser')
            user_cards = soup.findAll('div', {'class': 'card card-user-b s-pg16 s-brt1'})
            for card in user_cards:
                user_info = {}
                info = card.find('div', {'class': 'info'})
                nickname = info.find('a', {'class': 'name'}).get_text()
                print('用户昵称为%s' % nickname)
                user_info['nick'] = nickname

                ps = card.findAll('p')
                raw_locate = re.sub('个人主页', '', ps[0].get_text())
                locate = raw_locate.replace('\r', '').replace('\n', '').strip()
                print('所在地区为%s' % locate)
                user_info['area'] = locate

                for p in ps:
                    if re.search('粉丝', p.get_text()):
                        try:
                            nums = p.findAll('a')
                            concerns, fans, posts = nums[0].get_text(), nums[1].get_text(), nums[2].get_text()
                            print('关注数为%s' % concerns)
                            print('粉丝数为%s' % fans)
                            print('博文数为%s' % posts)
                            user_info['concerns'] = concerns
                            user_info['fans'] = fans
                            user_info['posts'] = posts
                        except IndexError:
                            user_info['concerns'] = 'N/A'
                            user_info['fans'] = 'N/A'
                            user_info['posts'] = 'N/A'

                    if re.search('标签', p.get_text()):
                        tags = p.findAll('a')
                        tagg = []
                        for t in tags:
                            tagg.append(t.get_text())
                        print(tagg)
                        user_info['tags'] = tagg
                    else:
                        user_info['tags'] = 'N/A'

                    if re.search('教育信息', p.get_text()):
                        education = p.find('a').get_text()
                        print('教育信息为%s' % education)
                        user_info['education'] = education
                    else:
                        user_info['education'] = 'N/A'

                    if re.search('职业信息', p.get_text()):
                        work = p.find('a').get_text()
                        print('职业信息为%s' % work)
                        user_info['work'] = work
                    else:
                        user_info['work'] = 'N/A'
                data.append(user_info)
        print(data)
        return data

    def save(self, file):
        import codecs
        f = codecs.open(file, 'w+', encoding='utf-8')
        data = self.start_requests()
        f.write(str(data))
        f.flush()
        f.close()


if __name__ == '__main__':
    wb = WeiboTag('18860927915', '87537277Abcd')
    wb.save(file="/Users/linjue/Desktop/weibo_data.txt")
