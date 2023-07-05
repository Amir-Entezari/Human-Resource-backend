from celery import shared_task


@shared_task
def add():
    file = open("test.txt","a")
    file.write("shiiiiiiiiiiit")
    file.close()
    print("******test******")
