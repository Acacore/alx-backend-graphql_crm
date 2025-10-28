#!/bin/bash


#Activate the Django environment if needed
# source /path/to/env/bin/activate


# got to jango project directory
cd /path/alx-backend-graphql_crm

# Run a Django shell command that delets inactive custumers (no order in a year)
deleted_count=$(python manage.py shell -c "
from datetime import timedelata
from django.utils import timezone
from crm.model import Customer

cutoff_date = timezone.now() - timedelta(days=365)
to_delete = Custumer.objects.filter(order_isnull=True, creataed_at__lt=cutoff_date)
count = to_delete.count()
to_delete.delete()
print(count)
")

#log the deletion count with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S')" - Deleted custumers: $deleted_count\" >> /tmp/customer_cleanenup_log.txt