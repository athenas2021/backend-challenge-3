from django.db import models


class DayProcess(models.Model):
    date = models.DateField(auto_now=False, blank=False, null=False)
    process_date = models.DateTimeField(auto_now=True)
    

    db_table = 'day_process'

class Transaction(models.Model):
    origin_bank = models.CharField(blank=False, null=False, max_length=100)
    origin_agency = models.CharField(blank=False, null=False, max_length=100)
    origin_account = models.CharField(blank=False, null=False, max_length=100)
    destiny_bank = models.CharField(blank=False, null=False, max_length=100)
    destiny_agency = models.CharField(blank=False, null=False, max_length=100)
    destiny_account = models.CharField(blank=False, null=False, max_length=100)
    transaction_value = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=20)
    transaction_date_time = models.DateTimeField(auto_now=False, blank=False, null=False)
    day_process = models.ForeignKey(DayProcess, on_delete=models.CASCADE)

    db_table = 'transaction'



