def timer(timed):
    def wrapper(*args):
        time = datetime.now()
        timed(*args)
        print(str(timed), (datetime.now() - time))
    return wrapper