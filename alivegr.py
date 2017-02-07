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

from resources.lib.modules import params

action = params.get('action')
name = params.get('name')
title = params.get('title')
tvshowtitle = params.get('tvshowtitle')
season = params.get('season')
episode = params.get('episode')
premiered = params.get('premiered')
image = params.get('image')
meta = params.get('meta')
select = params.get('select')
query = params.get('query')
source = params.get('source')
content = params.get('content')
url = params.get('url')

########################################################################################################################

if action is None:

    from resources.lib.indexers import root

    root.Main().root()

########################################################################################################################

elif action == 'live_tv':
    from resources.lib.indexers import live
    live.Main().live_tv()

elif action == 'pvr_client':
    from resources.lib.modules import statics
    statics.pvr_client()

elif action == 'networks':
    from resources.lib.indexers import networks
    networks.Main().networks()

elif action == 'movies':
    from resources.lib.indexers import gm
    gm.Main().movies()

elif action == 'short_films':
    from resources.lib.indexers import gm
    gm.Main().short_films()

elif action == 'shows':
    from resources.lib.indexers import gm
    gm.Main().shows()

elif action == 'series':
    from resources.lib.indexers import gm
    gm.Main().series()

elif action == 'kids':
    from resources.lib.indexers import cartoons
    cartoons.Main().kids()

elif action == 'cartoon_series':
    from resources.lib.indexers import gm
    gm.Main().cartoons_series()

elif action == 'cartoon_collection':
    from resources.lib.indexers import cartoons
    cartoons.Main().cartoon_collection()

elif action == 'educational':
    from resources.lib.indexers import cartoons
    cartoons.Main().educational()

elif action == 'kids_songs':
    from resources.lib.indexers import cartoons
    cartoons.Main().kids_songs()

elif action == 'listing':
    from resources.lib.indexers import gm
    gm.Main().listing(url)

elif action == 'episodes':
    from resources.lib.indexers import gm
    gm.Main().episodes(url, image)

elif action == 'theater':
    from resources.lib.indexers import gm
    gm.Main().theater()

elif action == 'documentaries':
    from resources.lib.indexers import documentaries
    documentaries.Main().documentaries()

elif action == 'miscellany':
    from resources.lib.indexers import miscellany
    miscellany.Main().miscellany()

elif action == 'addBookmark':
    from tulip import bookmarks
    bookmarks.add(url)

elif action == 'deleteBookmark':
    from tulip import bookmarks
    bookmarks.delete(url)

elif action == 'bookmarks':
    from resources.lib.indexers import bookmarks
    bookmarks.Main().bookmarks()

elif action == 'settings':
    from resources.lib.modules import statics
    statics.settings()

elif action == 'play':
    from resources.lib.modules import player
    player.play(url)

elif action == 'live_switcher':
    from resources.lib.indexers import live
    live.Main().switcher()

elif action == 'vod_switcher':
    from resources.lib.indexers import gm
    gm.Main().vod_switcher(url)

elif action == 'setup_iptv':
    from resources.lib.modules import tools
    tools.setup_iptv()

elif action == 'setup_previous_menu_key':
    from resources.lib.modules import tools
    tools.setup_previous_menu_key()

elif action == 'cache_clear':
    from resources.lib.modules import statics
    statics.cache_clear()

elif action == 'refresh':
    from resources.lib.modules import statics
    statics.refresh()

elif action == 'refresh_and_clear':
    from resources.lib.modules import statics
    statics.refresh_and_clear()

elif action == 'yt_setup':
    from resources.lib.modules import tools
    tools.yt_setup()
