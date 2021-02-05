from django.core.management.base import BaseCommand
from django.db import models
from olympicvaxinfo.models import Post, Comment, Category
import argparse
import os
import time
import datetime

class Command(BaseCommand):
    help = '--path where-to-save-posts'

    def latest_from_category(self, category):
        try:
            firstpost = Post.objects.filter(
                categories__name__contains=category.name
            ).order_by(
                '-created_on'
            )[0]
        except:
            firstpost = None
        return (firstpost)

    def get_posts(self, path):
        categories = Category.objects.all().order_by('-name')
        for c in categories:
            tmp = self.latest_from_category(c)
            if tmp:
                foldername = os.path.join(path, c.name)
                try:
                    os.mkdir(foldername)
                except:
                    pass
                timestamp = tmp.body.splitlines()[-1]
                
                filename = os.path.join(foldername, timestamp)

                if os.path.exists(filename):
                    print("file exists for latest post [" + tmp.title + "]: " + timestamp)
                    pass
                else:
                    f = open(filename, 'w+')
                    f.write(tmp.title + '\n' + tmp.siteurl + '\n' + tmp.body)
                    f.close()
                    print("no backup existed for latest post, backup exported")


        

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
    def handle(self, *args, **kwargs):
        path = kwargs['path']
        try:
            os.mkdir(path)
        except:
            pass
        self.get_posts(path)

