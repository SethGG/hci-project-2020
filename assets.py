from flask_assets import Environment, Bundle

assets = Environment()

root_page = Bundle('scripts/login.js', output='gen/root_page.js')
user_page = Bundle('scripts/logout.js', output='gen/user_page.js')
char_page = Bundle('scripts/logout.js', 'scripts/stats.js', output='gen/char_page.js')
spellbook_page_logged_in = Bundle('scripts/logout.js', 'scripts/prepare.js', 'scripts/slots.js',
                                  'scripts/spellbook.js', output='gen/spellbook_page_logged_in.js')
spellbook_page_logged_out = Bundle('scripts/login.js', 'scripts/spellbook.js',
                                   output='gen/spellbook_page_logged_out.js')

assets.register('root_page', root_page)
assets.register('user_page', user_page)
assets.register('char_page', char_page)
assets.register('spellbook_page_logged_in', spellbook_page_logged_in)
assets.register('spellbook_page_logged_out', spellbook_page_logged_out)
