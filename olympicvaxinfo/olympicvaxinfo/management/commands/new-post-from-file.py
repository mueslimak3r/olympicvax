from django.core.management.base import BaseCommand
from django.db import models
from olympicvaxinfo.models import Post, Comment, Category
import argparse

class Command(BaseCommand):
    help = '--path filename --category post-category'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('--category', type=int)
    def handle(self, *args, **kwargs):
        filename = kwargs['path']
        category = kwargs['category']
        f = open(filename, 'r')
        data = f.read().splitlines()
        
        print('added post to database')        

        newpost = Post(
            title=data[0],
            siteurl=data[1],
            body='\n'.join(data[2:]),
        )
        
        newpost.save()
        newpost.categories.set([category])

        f.close()