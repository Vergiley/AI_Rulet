#!/usr/bin/env python3
"""Сборка AI_Rulet: из src/ — по самодостаточной странице на каждый готовый язык.

Русская страница — index.html в корне (адрес сайта не меняется), остальные — <код>/index.html.
Язык готов, когда есть папка src/lang/<код>/ со всеми файлами:
  strings.js — словарь T (тексты, которые собирает код);
  page.json  — тексты разметки страницы;
  help.html  — содержимое панели справки;
  catalog.js — CATEGORIES: области и идеи;
  mix.js     — тексты «Микса»: сферы, техники, форматы, аномалии, фразы.
Общее для всех языков: src/template.html (вёрстка, стили, код) и src/shared/mix.js (структура «Микса»).
Запуск: python3 build.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://airulet.dev/'
# код (папка в src/lang), название на своём языке, папка страницы, направление письма, локаль превью ссылки,
# тег языка для lang, hreflang и Intl (у китайского — упрощённое письмо)
LANGS = [
    ('ru', 'Русский', '', 'ltr', 'ru_RU', 'ru'),
    ('en', 'English', 'en/', 'ltr', 'en_US', 'en'),
    ('zh', '中文', 'zh/', 'ltr', 'zh_CN', 'zh-Hans'),
    ('hi', 'हिन्दी', 'hi/', 'ltr', 'hi_IN', 'hi'),
    ('ar', 'العربية', 'ar/', 'rtl', 'ar_AR', 'ar'),
    ('fa', 'فارسی', 'fa/', 'rtl', 'fa_IR', 'fa'),
    ('he', 'עברית', 'he/', 'rtl', 'he_IL', 'he'),
]
FILES = ['strings.js', 'page.json', 'help.html', 'catalog.js', 'mix.js']


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


def ready_langs():
    out = []
    for lang in LANGS:
        d = os.path.join(ROOT, 'src', 'lang', lang[0])
        if os.path.isdir(d):
            missing = [f for f in FILES if not os.path.isfile(os.path.join(d, f))]
            if missing:
                sys.exit(f'{lang[0]}: нет файлов {missing}')
            out.append(lang)
    return out


def catalog_shape(js):
    """области по порядку: (id, глиф, идей, аномалий в пуле) — у всех языков должны совпадать"""
    shape = []
    for m in re.finditer(r"\{ id:'([^']+)', name:'[^']*', ep:'[^']*', glyph:'([^']+)',.*?twists:`(.*?)`,\s*ideas:`(.*?)`", js, re.S):
        count = lambda block: len([l for l in block.strip().split('\n') if l.strip()])
        shape.append((m.group(1), m.group(2), count(m.group(4)), count(m.group(3))))
    return shape


def array_rows(js, name):
    """сколько записей в массиве const NAME = [ … ] (по строке на запись)"""
    m = re.search(r'const ' + name + r' = \[\n(.*?)\n\];', js, re.S)
    if not m:
        sys.exit(f'нет массива {name}')
    return len([l for l in m.group(1).split('\n') if l.startswith(' [') or l.startswith(" '")])


def check(lang, ru):
    """тексты языка совпадают со структурой: те же области, идеи и записи «Микса» в том же порядке"""
    code = lang[0]
    if code != 'ru' and catalog_shape(read(f'src/lang/{code}/catalog.js')) != catalog_shape(read('src/lang/ru/catalog.js')):
        sys.exit(f'{code}: каталог не совпадает с русским по областям, глифам или числу идей и аномалий')
    shared, text = read('src/shared/mix.js'), read(f'src/lang/{code}/mix.js')
    for s_name, t_name in [('MIX_D', 'DOMAINS_TX'), ('MIX_T', 'TECH_TX'), ('MIX_F', 'FORMATS_TX'), ('MIX_A', 'TWISTS_TX')]:
        if array_rows(shared, s_name) != array_rows(text, t_name):
            sys.exit(f'{code}: в {t_name} {array_rows(text, t_name)} записей, а в {s_name} — {array_rows(shared, s_name)}')
    page = json.loads(read(f'src/lang/{code}/page.json'))
    missing = set(json.loads(read('src/lang/ru/page.json'))) - set(page)
    if missing:
        sys.exit(f'{code}: в page.json нет ключей {sorted(missing)}')


def rel(from_dir, to_dir):
    """относительная ссылка между папками языков — работает и на сайте, и из файлов на диске"""
    up = '../' * from_dir.count('/')
    return (up + to_dir) or './'


def build(lang, ready):
    code, _, folder, direction, locale, tag = lang
    page = json.loads(read(f'src/lang/{code}/page.json'))
    s = read('src/template.html')
    # данные: строка языка, словарь, каталог, «Микс»
    lang_line = f"const LANG = '{tag}', PAGE_URL = '{SITE}{folder}';   // язык и адрес этой страницы — задаёт сборка\n"
    for token, value in [('/*@@LANG@@*/', lang_line),
                         ('/*@@STRINGS@@*/\n', read(f'src/lang/{code}/strings.js')),
                         ('/*@@CATALOG@@*/\n', read(f'src/lang/{code}/catalog.js')),
                         ('/*@@MIX_SHARED@@*/\n', read('src/shared/mix.js')),
                         ('/*@@MIX_TEXT@@*/', read(f'src/lang/{code}/mix.js'))]:
        assert s.count(token) == 1, token
        s = s.replace(token, value)
    # выбор языка и hreflang — только когда языков больше одного
    if len(ready) > 1:
        links = ''.join(
            f'<a href="{rel(folder, l[2])}" hreflang="{l[5]}" lang="{l[5]}"' + (' aria-current="page"' if l[0] == code else '') + f'>{l[1]}</a>'
            for l in ready)
        nav = f'  <nav class="langs" aria-label="{page["lang_nav"]}">{links}</nav>\n'
        alt = ''.join(f'<link rel="alternate" hreflang="{l[5]}" href="{SITE}{l[2]}">\n' for l in ready) + \
              f'<link rel="alternate" hreflang="x-default" href="{SITE}">\n'
    else:
        nav = alt = ''
    # описание для поисковиков (schema.org): что это за страница, на каком языке, бесплатно, без установки
    ld = {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': 'AI_Rulet', 'url': SITE + folder,
          'description': page['og_description'], 'inLanguage': tag, 'image': SITE + folder + 'og.jpg',
          'applicationCategory': 'EducationalApplication', 'operatingSystem': 'Any', 'browserRequirements': 'Requires JavaScript',
          'isAccessibleForFree': True, 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
          'license': 'https://opensource.org/licenses/MIT'}
    jsonld = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    if not os.path.isfile(os.path.join(ROOT, folder, 'og.jpg')):
        print(f'{code}: нет {folder}og.jpg — картинка превью (сделать: ai_rulet_tools/seo/make_og.py)')
    s = s.replace('{{@langs}}', nav).replace('{{@hreflang}}', alt).replace('{{@jsonld}}', jsonld) \
         .replace('{{@help}}', read(f'src/lang/{code}/help.html'))
    values = dict(page, lang=tag, dir=direction, page_url=SITE + folder, locale=locale)
    s = re.sub(r'\{\{(\w+)\}\}', lambda m: values[m.group(1)], s)
    left = re.findall(r'\{\{@?\w+\}\}|/\*@@\w+@@\*/', s)
    if left:
        sys.exit(f'{code}: не подставлено {left[:5]}')
    out = os.path.join(ROOT, folder, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)
    return out, len(s.encode('utf-8'))


def main():
    ready = ready_langs()
    ru = next(l for l in ready if l[0] == 'ru')
    for lang in ready:
        check(lang, ru)
    for lang in ready:
        out, size = build(lang, ready)
        print(f'{lang[0]}: {os.path.relpath(out, ROOT)} — {size / 1024:.0f} КБ')
    open(os.path.join(ROOT, '.nojekyll'), 'a').close()   # GitHub Pages отдаёт файлы как есть, без Jekyll
    write_sitemap(ready)


def write_sitemap(ready):
    """sitemap.xml со всеми языками (у каждой страницы — ссылки на её версии) и robots.txt со ссылкой на него"""
    alts = ''.join(f'    <xhtml:link rel="alternate" hreflang="{l[5]}" href="{SITE}{l[2]}"/>\n' for l in ready) + \
           f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}"/>\n'
    urls = ''.join(f'  <url>\n    <loc>{SITE}{l[2]}</loc>\n{alts}  </url>\n' for l in ready)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           f'{urls}</urlset>\n')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(xml)
    with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')


if __name__ == '__main__':
    main()
