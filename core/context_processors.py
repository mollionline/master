from issue_tracker.models import Status, Type


def statuses(request):
    return {
        'statuses': Status.objects.all()
    }


def types(request):
    return {
        'types': Type.objects.all()
    }
