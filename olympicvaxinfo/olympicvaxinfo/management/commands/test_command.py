from django.core.management.base import BaseCommand
from django.db import models
from olympicvaxinfo.models import Post, Comment, Category
import argparse
class Command(BaseCommand):
    help = 'Understanding management command'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('--category', type=int)
    def handle(self, *args, **kwargs):
        self.stdout.write("Writing management command")
        filename = kwargs['path']
        category = kwargs['category']
        f = open(filename, 'r')
        data = f.read().splitlines()
        
        print(data)
        print('HELLO')
        

        newpost = Post(
            title=data[0],
            siteurl=data[1],
            body=data[2],
        )
        
        newpost.save()
        newpost.categories.set([category])

        f.close()