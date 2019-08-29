from django.contrib.auth.models import Group, User

def populate_models(sender, **kwargs):
    new_group, created1 = Group.objects.get_or_create(name='Common')
    new_group2, created2 = Group.objects.get_or_create(name='Operators')
    operator1, created3 = User.objects.get_or_create(username='operator1')
    noreply, created4 = User.objects.get_or_create(username='noreply')
    if created3:
        operator1.set_password('operator123')
        operator1.save()
        operator1.groups.add(new_group2)

    if created4:
        noreply.set_password('noreply123')
        noreply.save()
        noreply.groups.add(new_group)