# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Thgiliwt

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re, base64, json, datetime
# noinspection PyUnresolvedReferences
from tulip import syshandle, sysaddon, cache, control, directory, client, ordereddict


class Main:

    def __init__(self):

        self.list = []; self.data = []; self.no_alt = []; self.groups = []; self.trimmed = []
        self.live = 'aHR0cDovL3RoZ2lsaXd0Lm9mZnNob3JlcGFzdGViaW4uY29tL2FsaXZlZ3IubTN1'
        self.alt_str = ['Alt1', 'Alt2', 'Alt3', 'Alt4', 'Alt5', 'BUP']

    def _live_(self):

        text = client.request(base64.b64decode(self.live))
        items = re.compile('EXTINF:-?\d group-title="(.*?)" tvg-logo="(.*?)",(.*?)\n^(.*?)$', re.M + re.U + re.S).findall(text.replace('\r\n', '\n'))

        for group, icon, title, url in items:

            if '{' in title:
                title = title.rpartition('{')[0].decode('utf-8')
                plot = title.rpartition('{')[2].decode('utf-8')

                if control.setting('splitter') == 'true':
                    if control.setting('lang_split') == '0':
                        plot = plot.rpartition('-')[0].strip(' }')
                    elif control.setting('lang_split') == '1':
                        plot = plot.rpartition('-')[2].strip(' }')

            else:
                plot = control.lang(30093)

            data = ({'title': title, 'image': icon, 'group': group, 'url': url, 'duration': None, 'year': datetime.datetime.now().year, 'genre': 'Live', 'plot': plot})
            self.list.append(data)
            self.groups.append(group.decode('utf-8'))

        self.trimmed = list(ordereddict.OrderedDict.fromkeys(self.groups))

        self.trimmed.sort()

        self.no_alt = [item for item in self.list if not any(alt in item['title'] for alt in self.alt_str)]

        return self.list, self.no_alt, self.trimmed

    def switcher(self):

        cached = cache.get(self._live_, 2)

        self.groups = [control.lang(30048)] + cached[2]

        choices = control.selectDialog(heading=control.lang(30049), list=self.groups)

        if choices == 0:
            control.setSetting('live_group', 'ALL')
            control.idle()
            control.sleep(50)  # ensure setting has been saved
            control.refresh()
        elif choices <= len(self.groups) and not choices == -1:
            control.setSetting('live_group', (self.groups.pop(choices)))
            control.idle()
            control.sleep(50)  # ensure setting has been saved
            control.refresh()
        else:
            control.execute('Dialog.Close(all)')

    def live_tv(self):

        if control.setting("show-alt") == "true":
            cached = cache.get(self._live_, 2)[0]
        else:
            cached = cache.get(self._live_, 2)[1]

        switch = {
                    'title': control.lang(30047).format(control.lang(30048) if control.setting('live_group') == 'ALL' else control.setting('live_group').decode('utf-8')),
                    'icon': control.addonmedia('script.AliveGR.artwork', 'switcher.png'),
                    'action': 'live_switcher'
                 }

        filtered = [item for item in cached if any(item['group'] == group for group in [control.setting('live_group').decode('utf-8')])] if not control.setting('live_group') == 'ALL' else cached

        if control.setting('live_sort') == 'true':
            if control.setting('live_method') == '0':
                self.list = sorted(filtered, key=lambda k: k['title'].lower())
            elif control.setting('live_method') == '1':
                self.list = sorted(filtered, key=lambda k: k['group'].lower())
        else:
            self.list = filtered

        for item in self.list:
            item.update({'action': 'play', 'isFolder': 'False'})

        for item in self.list:
            bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
            bookmark['bookmark'] = item['url']
            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            r_and_c_cm = {'title': 30082, 'query': {'action': 'refresh_and_clear'}}
            pvr_client_cm = {'title': 30084, 'query': {'action': 'pvr_client'}}
            item.update({'cm': [bookmark_cm, r_and_c_cm, pvr_client_cm]})

        if control.setting('show-switcher') == 'true':

            li = control.item(label=switch['title'], iconImage=switch['icon'])
            li.setArt({'fanart': control.addonInfo('fanart')})
            url = '{0}?action={1}'.format(sysaddon, switch['action'])
            control.addItem(syshandle, url, li)

        else:
            pass

        directory.add(self.list, content='movies')
