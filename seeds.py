# -*- coding: utf-8 -*-

from app import db
from app.models import User, Brewery, Style, Beer, Survey


def seed_all():
    """Users"""
    users = [
        User(name=u'admin', role=1),
    ]
    db.session.add_all(users)

    """Beer styles"""
    styles = {
        'None': Style(name=u'None'),
        'American': Style(name=u'American Stout'),
        'Imperial': Style(name=u'American Double / Imperial Stout'),
        'Milk': Style(name=u'Milk / Sweet Stout'),
        'Oatmeal': Style(name=u'Oatmeal Stout'),
        'Russian': Style(name=u'Russian Imperial Stout'),
        'Irish': Style(name=u'Irish Dry Stout'),
        'EnglishP': Style(name=u'English Porter'),
        'AmericanP': Style(name=u'American Porter'),
    }
    db.session.add_all(styles.values())

    """Breweries"""
    breweries = {
        'None': Brewery(name=u'None'),
        'Atlantic': Brewery(name=u'Atlantic Brewing Company'),
        'Grimm': Brewery(name=u'Grimm Artisanal Ales'),
        'Founders': Brewery(name=u'Founders Brewing Company'),
        'Smith': Brewery(name=u'Samuel Smith Old Brewery'),
        'Evil': Brewery(name=u'Evil Twin Brewing'),
        'Star': Brewery(name=u'14th Star Brewing Company'),
        'Oskar': Brewery(name=u'Oskar Blues Grill & Brew'),
        'Trillium': Brewery(name=u'Trillium Brewing Company'),
        'Divide': Brewery(name=u'Great Divide Brewing Company'),
        'Guinness': Brewery(name=u'Guinness Ltd.'),
        'Lefthand': Brewery(name=u'Left Hand Brewing Company'),
        'THouse': Brewery(name=u'Tree House Brewing Company'),
        'TwoRds': Brewery(name=u'Two Roads Brewing Company'),
        'Victory': Brewery(name=u'Victory Brewing Company'),
        'Yergey': Brewery(name=u'Yergey Brewing'),
    }
    db.session.add_all(breweries.values())

    """Beers"""
    beers = {
        'Ellen': Beer(
            brewery=breweries['Atlantic'],
            name=u'Ellens Coffee Stout',
            style=styles['Milk'],
            abv=5.4,
            ba=87,
            notes=u'Stout with vanilla and coffee',
            ),
        'Negative': Beer(
            brewery=breweries['Grimm'],
            name=u'Double Negative',
            style=styles['Imperial'],
            abv=10.0,
            ba=93,
            ),
        'FBreak': Beer(
            brewery=breweries['Founders'],
            name=u'Breakfast Stout',
            style=styles['Imperial'],
            abv=8.3,
            ba=99,
            notes=u'Double chocolate coffee oatmeal stout',
            ),
        'SOatmeal': Beer(
            brewery=breweries['Smith'],
            name=u'Oatmeal Stout',
            style=styles['Oatmeal'],
            abv=5.0,
            ba=94,
            ),
        'Biscotti': Beer(
            brewery=breweries['Evil'],
            name=u'Imperial Biscotti Break',
            style=styles['Imperial'],
            abv=11.5,
            ba=96,
            notes=u'Brewed with coffee, almond and vanilla added',
            ),
        'SMaple': Beer(
            brewery=breweries['Star'],
            name=u'Maple Breakfast Stout',
            style=styles['American'],
            abv=5.5,
            ba=84,
            notes=u'Brewed with VT maple syrup',
            ),
        'TenFidy': Beer(
            brewery=breweries['Oskar'],
            name=u'Ten FIDY',
            style=styles['Russian'],
            abv=10.5,
            ba=96,
            notes=u'Cellered 1 year',
            ),
        'Trill': Beer(
            brewery=breweries['Trillium'],
            name=u'Dusk Trill Dawn',
            style=styles['Imperial'],
            abv=11.5,
            ba=98,
            notes=u'Coffee stout brewed in collaboration with Evil Twin Brewing',
            ),
        'LHMilk': Beer(
            brewery=breweries['Lefthand'],
            name=u'Milk Stout Nitro',
            style=styles['Milk'],
            abv=6.0,
            ba=91,
            ),
        'Guinness': Beer(
            brewery=breweries['Guinness'],
            name=u'Guinness Draught',
            style=styles['Irish'],
            abv=4.2,
            ba=79,
            ),
        'THouse': Beer(
            brewery=breweries['THouse'],
            name='All That Is And All That Ever Will Be',
            style=styles['Milk'],
            abv=6.5,
            ba=95,
            notes=u'Cocoa, coffee, milk stout',
            ),
        'CNut': Beer(
            brewery=breweries['Oskar'],
            name='Death by Coconut',
            style=styles['EnglishP'],
            abv=6.5,
            ba=93,
            notes=u'Once a year limited release',
        ),
        'Express': Beer(
            brewery=breweries['TwoRds'],
            name='Expressway',
            style=styles['Oatmeal'],
            abv=6.5,
            ba=0,
            notes=u'Cold brewed coffee stout',
        ),
        'Vicotry': Beer(
            brewery=breweries['Victory'],
            name='Oatmeal',
            style=styles['None'],
            abv=0,
            ba=0,
            notes=u'Allard\'s mystery beer labeled "oatmeal"',
        ),
        'Yergey1': Beer(
            brewery=breweries['Yergey'],
            name='Simply, Chocolate',
            style=styles['AmericanP'],
            abv=6.6,
            ba=0,
            notes=u'Brewed with organic Ghana cacao nibs',
        ),
        'Yergey2': Beer(
            brewery=breweries['Yergey'],
            name='Hot Chocolate',
            style=styles['AmericanP'],
            abv=6.6,
            ba=0,
            notes=u'Chocolate porter kicked up with a little Habanero extract',
        ),
    }



        # 'OYeti': Beer(
        #     brewery=breweries['Divide'],
        #     name=u'Oak Aged Yeti Imperial Stout',
        #     style=styles['Russian'],
        #     abv=9.5,
        #     ba=94,
        #     notes=u'Aged on French and American oak chips',
        #     ),
    db.session.add_all(beers.values())

    # Finally, commit
    db.session.commit()
