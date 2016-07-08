from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160625_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='created',
            field=models.DateField(default=datetime.datetime(2016, 6, 28, 14, 52, 39, 77937)),
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.URLField(default='http://www.theblogstarter.com/wp-content/uploads/2016/01/start-your-blog-4-steps.png'),
        ),
    ]
