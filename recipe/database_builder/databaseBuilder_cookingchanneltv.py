#!/usr/bin/env python
import requests
import re
import pickle
import time
import os

from ShowProgressBar import ShowProgressBar

database_filename = os.environ['MainDir']+'/recipe/database_cookingchanneltv.pickle'
debug = False

accepted_units = ['small', 'medium', 'big', 'medium-size',
                  'g', 'pound', 'pounds',
                  'ounce', 'ounces', 'oz', 'oz.',
                  'l', 'ml',
                  'pint',
                  'jar', 'cup', 'cups', 'can', 'cans'
                  'package',
                  'spoon', 'spoons', 'tablespoon', 'tablespoons', 'teaspoon', 'teaspoons',
                  'Pinch', 'pinch', 'handful',
                  'clove', 'cloves',
                  'slice', 'slices',
                  'bunch'
                 ]

def getName(content):
    template = '<span class="o-AssetTitle__a-HeadlineText">'
    idx_start = content.find(template) + len(template)
    s = content[idx_start:idx_start+100]
    idx_stop = s.find('</span>')
    title = s[:idx_stop]
    if ':' in title:
        title = title[:title.find(':')]
    if debug: print('\t'+title)

    return title

def getLevel(content):
    try:
        template = '<span class="o-RecipeInfo__a-Headline">Level:</span>'
        idx_start = content.find(template) + len(template)
        s = content[idx_start:idx_start+100]
        out = re.search(r'">[A-Za-z]+</span', s)
        level = out.group(0)[2:-6]
    except: level = 'None'
    if debug: print('\t'+level)

    return level

def getNumberPeople(content):
    try:
        template = '<span class="o-RecipeInfo__a-Headline">Yield:</span>'
        idx_start = content.find(template) + len(template)
        s = content[idx_start:idx_start+100]
        out = re.search(r'">[0-9]+', s)
        Nppl = out.group(0)[2:]
    except:
        Nppl = '-1'
    if debug: print('\t'+Nppl)

    return int(Nppl)

def getIngredients(content):
    template = '<p class="o-Ingredients__a-Ingredient">'
    idx_start = content.find(template) + len(template)
    s = content[idx_start:]
    cut_template = '<h6 class="o-Ingredients__a-SubHeadline">'
    if cut_template in s:
        idx_stop = s.find(cut_template)
        s = s[:idx_stop]
    slist = s.split(template)

    ingredients_list = []

    for l in slist:
        i = l.find('</p>')
        aux = l[:i]
        if ',' in aux:
            aux = aux[:aux.find(',')]
        if '(' in aux:
            aux = aux[:aux.find('(')-1] + aux[aux.find(')')+1:]
        if '/' in aux:
            aux = aux[aux.find('/')+1:]
        if aux[-8:] == '\\xc2\\xa0':
            aux = aux[:-8]

        l_aux = aux.split(' ')
        if len(l_aux)==2 and l_aux[0].isnumeric():
            name = l_aux[1].capitalize()
            amount = l_aux[0]
            units = ''
        elif len(l_aux) > 2 and (l_aux[1] in accepted_units):
            name = ' '.join(l_aux[2:])
            name.capitalize()
            amount = l_aux[0]
            units = l_aux[1]
        elif len(l_aux) > 1 and not l_aux[0].isnumeric() and not (l_aux[1] in accepted_units):
            name = ' '.join(l_aux)
            name.capitalize()
            amount = ''
            units = ''
        elif len(l_aux) > 2 and l_aux[0].isnumeric() and not (l_aux[1] in accepted_units):
            name = ' '.join(l_aux[1:])
            name.capitalize()
            amount = l_aux[0]
            units = ''
        elif len(l_aux) == 1:
            name = l_aux[0]
            amount = ''
            units = ''
        else:
            if debug: print(l_aux)
            name = 'NaN'
            amount = 'NaN'
            units = 'NaN'

        if name.startswith('of '):
            name = name[3:]

        out = '\t\t'+ name + '-->'
        out += 'Amount: '+ amount + '(' + units + ')'
        if debug: print(out)

        ingredients_list.append([name, amount, units])

    return ingredients_list

class Recipe():
    def __init__(self, name=''):
        self.name = name


if __name__=='__main__':

    alphabet = ['123']
    for letter in range(97,120):
        alphabet.append(chr(letter))
    alphabet.append('xyz')

    # alphabet = alphabet[15:17]

    recipes_database = []
    print('------------ Starting download loop --------------')
    try:
        for source_letter in alphabet:
            print('>>>>> Downloading letter', source_letter)

            letter_source = 'https://www.cookingchanneltv.com/recipes/a-z/'+source_letter+'/p/'

            pag_N = 1
            empty_page = False
            while(not empty_page):
                top_source = 'https://www.cookingchanneltv.com/recipes/a-z/'+source_letter+'/p/'+str(pag_N)

                try:
                    r = requests.get(top_source)
                except:
                    pag_N += 1
                    continue

                content = str(r.content)

                # Get only the part with recipes links
                idx_start = content.find('<span class="o-Capsule__a-HeadlineText">'+source_letter.upper()+'</span>')
                content = content[idx_start:]
                idx_stop = content.find('<section class="o-Pagination ">')
                content = content[:idx_stop]

                recipes_url_list = []
                for ln in content.split('href')[1:]:
                    idx_end = ln.find('">')
                    url = 'https:' + ln[2:idx_end]
                    recipes_url_list.append(url)

                print('\tPage {} --> {}'.format(pag_N, len(recipes_url_list)))


                if len(recipes_url_list) == 0:# or pag_N == 3:
                    empty_page == True
                    if debug: print('Total valid pages:', pag_N-1)
                    break


                for i_r, url in enumerate(recipes_url_list):
                    ShowProgressBar(i_r, len(recipes_url_list))
                    recipe = Recipe()
                    recipe.url = url
                    if debug: print(url)

                    try:
                        content = str(requests.get(url).content)
                    except:
                        continue
                    recipe.name = getName(content)
                    recipe.level = getLevel(content)
                    recipe.Nppl = getNumberPeople(content)
                    recipe.ingredients = getIngredients(content)

                    recipes_database.append(recipe)

                pag_N += 1

        print('----------------  Done  ----------------------')
    except KeyboardInterrupt:
        print(' -------   Manually interrupted ----------')
    except:
        print('!!!!!!!    ERROR FOUND   !!!!!!!!')

    print('Number of recipes found:', len(recipes_database))
    print('Saving database in:', database_filename)
    pickle.dump(recipes_database, open(database_filename, 'wb'))
    size = os.path.getsize(database_filename) #bytes
    size /= 1024.0**2 #Mb
    print('Database size: {:.2f} Mb'.format(size))
