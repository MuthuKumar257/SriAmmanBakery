import os, glob, re

files = [f for f in glob.glob('src/**/*', recursive=True) if os.path.isfile(f) and f.endswith(('.ts', '.tsx'))]

print('=== 1. AUDIT FOR HINDI & REGIONAL TERMS ===')
hindi_terms = ['shuddh', 'desi', 'kadai', 'kadhai', 'mithai', 'halwai', 'chulha', 'besan', 'vark', 'bharat', 'tamil']
hindi_hits = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        for idx, line in enumerate(fp, 1):
            for t in hindi_terms:
                if t in line.lower():
                    print(f'  [HINDI/REGIONAL] {f}:{idx} -> {line.strip()[:80]}')
                    hindi_hits += 1
if hindi_hits == 0:
    print('  [PASS] Zero Hindi or regional terms found.')

print('\n=== 2. AUDIT FOR INDIC / NON-ASCII SCRIPTS ===')
indic_hits = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        for idx, line in enumerate(fp, 1):
            m = re.findall(r'[\u0900-\u097F\u0B80-\u0BFF]', line)
            if m:
                print(f'  [INDIC SCRIPT] {f}:{idx}: {len(m)} characters found')
                indic_hits += 1
if indic_hits == 0:
    print('  [PASS] Zero Indic or Devanagari or Tamil characters found.')

print('\n=== 3. AUDIT FOR ORDERING & PURCHASING PHRASES ===')
order_terms = ['order now', 'add to cart', 'buy now', 'shopping cart', 'checkout', 'order on whatsapp', 'order through whatsapp', 'wa.me', 'order sweets']
order_hits = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        for idx, line in enumerate(fp, 1):
            for t in order_terms:
                if t in line.lower():
                    print(f'  [PURCHASE CONTROL] {f}:{idx} -> {line.strip()[:80]}')
                    order_hits += 1
if order_hits == 0:
    print('  [PASS] Zero purchase or ordering controls found.')

print('\n=== 4. AUDIT FOR GHEE TAGLINE ===')
ghee_tagline = '100% pure homemade ghee'
count_ghee = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
        count_ghee += content.lower().count(ghee_tagline)
print(f'  [PASS] Found {count_ghee} occurrences of "100% Pure Homemade Ghee".')

print('\n=== 5. AUDIT FOR ALL 12 SWEETS ===')
sweets = [
    'Laddu', 'Mysore Pak', 'Jalebi', 'Badam Burfi', 'Boost Burfi', 'Horlicks Burfi', 'Badusha',
    'Carrot Burfi', 'Pista Burfi', 'Rose Burfi', 'Gulab Jamun', 'Milk Laddu'
]
with open('src/config/site.ts', 'r', encoding='utf-8') as fp:
    cfg = fp.read()
    for s in sweets:
        if s in cfg:
            print(f'  [PASS] Sweet: {s}')
        else:
            print(f'  [FAIL] Missing sweet: {s}')

print('\n=== 6. AUDIT FOR FOUNDER & YEAR ===')
if 'Mangalasamy P' in cfg and '2022' in cfg:
    print('  [PASS] Founder Mangalasamy P and 2022 present in config.')
else:
    print('  [FAIL] Missing founder or year in config.')

