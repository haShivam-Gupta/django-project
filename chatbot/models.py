from django.db import models

class TransactionQuery(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return self.transaction_id
