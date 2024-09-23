from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings

def sync_to_other_db(sender, instance, created, **kwargs):
    if not settings.DATABASE_ROUTERS:
        return
    
    other_db = 'heroku_db' if settings.DATABASES['default'] == settings.DATABASES['local_db'] else 'local_db'
    
    model = apps.get_model(app_label=sender._meta.app_label, model_name=sender._meta.model_name)
    
    if created:
        model.objects.using(other_db).create(**{f.name: getattr(instance, f.name) for f in instance._meta.fields})
    else:
        try:
            other_instance = model.objects.using(other_db).get(pk=instance.pk)
            for field in instance._meta.fields:
                setattr(other_instance, field.name, getattr(instance, field.name))
            other_instance.save(using=other_db)
        except model.DoesNotExist:
            model.objects.using(other_db).create(**{f.name: getattr(instance, f.name) for f in instance._meta.fields})

def sync_delete_to_other_db(sender, instance, **kwargs):
    if not settings.DATABASE_ROUTERS:
        return
    
    other_db = 'heroku_db' if settings.DATABASES['default'] == settings.DATABASES['local_db'] else 'local_db'
    
    model = apps.get_model(app_label=sender._meta.app_label, model_name=sender._meta.model_name)
    
    try:
        model.objects.using(other_db).get(pk=instance.pk).delete()
    except model.DoesNotExist:
        pass

def register_sync_signals():
    for model in apps.get_models():
        post_save.connect(sync_to_other_db, sender=model)
        post_delete.connect(sync_delete_to_other_db, sender=model)