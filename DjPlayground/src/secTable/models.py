from django.db import models

class Reporters(models.Model):
    timestamp    = models.DateTimeField(db_column='timestamp')
    symbol       = models.TextField(db_column='symbol')
    officertitle = models.TextField(db_column='officertitle')
    officername  = models.TextField(db_column='officername')
    title        = models.TextField(db_column='title')
    isdirector   = models.TextField(db_column='isDirector')  # Field name made lowercase.
    hlink        = models.TextField(db_column='hlink')
    xlink        = models.TextField(db_column='xlink')
    pnlink       = models.TextField(db_column='pnlink')
    id           = models.IntegerField(db_column='id', primary_key=True)

    class Meta:
        managed = True
        db_table = 'reporters'

    def __unicode__(self):
        return(self.timestamp)

class Transactions(models.Model):
    timestamp   = models.DateTimeField(db_column='timestamp')
    symbol      = models.TextField(db_column='symbol')
    aord        = models.TextField(db_column='aord')
    stockordv   = models.TextField(db_column='stockordv')
    amount      = models.FloatField(db_column='amount')
    code        = models.TextField(db_column='code')
    ownedafter  = models.TextField(db_column='ownedAfter')  # Field name made lowercase.
    price       = models.FloatField(db_column='price')
    title       = models.TextField(db_column='title')
    id          = models.IntegerField(db_column='id', primary_key=True)

    class Meta:
        managed = True
        db_table = 'transactions'
        
    def __unicode__(self):
        return(self.timestamp)