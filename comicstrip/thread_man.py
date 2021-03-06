'''
  Author: <adrellias@gmail.com>

  This module handles the creation of threads
  For once off and scheduled continues looping jobs

  Originaly Based on:
  http://code.activestate.com/recipes/114644/
  and Sickbeards scheduler:
  https://github.com/SickBeard-Team/SickBeard/blob/develop/sickbeard/scheduler.py
'''

import time
import datetime
import threading
import comicstrip

from comicstrip import logger


class Task(threading.Thread):

    def __init__(self, **kwargs):
        ''' Initiate thread startup '''
        self.action = kwargs.get('action')
        self.cycleTime = kwargs.get('cycleTime')
        self.args = kwargs.get('args')
        self.runImmediatly = kwargs.get('runImmediatly')
        self.running = 1

        if self.runImmediatly:
            self.lastRun = datetime.datetime.fromordinal(1)
        else:
            self.lastRun = datetime.datetime.now()

        threading.Thread.__init__(self)
        logger.log(u'Thread Init: ' + str(threading.current_thread().name))

    def __repr__(self):
        ''' Return the options we passed '''
        return '%s %s %s' % (
            self.action, self.cycleTime, self.lastRun)

    def run(self):
        ''' Run the function we want '''
        logger.log(u'Thread Started: ' + str(threading.current_thread().name))

        while True:
            currentTime = datetime.datetime.now()

            if currentTime - self.lastRun > self.cycleTime:
                logger.log(u'Running task: '  + str(threading.current_thread().name))
                self.lastRun = currentTime
                try:
                    if self.args is not None:
                        self.action(self.args)
                    else:
                        self.action()

                except Exception, e:
                    raise
                    logger.log(u'Exception generated in thread ' + e)

            if not self.running:
                return

            time.sleep(1)

    def stop(self):
        logger.log(u'Sending stop signal')
        self.running = 0


class Scheduler:
    ''' Schedule the threads we want to run'''

    def __init__(self):
        ''' We want a list of tasks ? '''
        comicstrip.TASK_LIST = []
        #self.tasks = []

    def __repr__(self):
        rep = ''
        #for task in self.tasks:
        for task in comicstrip.TASK_LIST:
            rep += '%s\n' % repr(task)
        return rep

    def AddTask(self, **kwargs):
        task = Task(**kwargs)

        if kwargs.get('cycleTime'):
            #self.tasks.append(task)
            comicstrip.TASK_LIST.append(task)
        else:
            task.start()

    def StartAllTasks(self):
        #for task in self.tasks:
        for task in comicstrip.TASK_LIST:
            task.start()

    def StopAllTasks(self):
        #for task in self.tasks:
        for task in comicstrip.TASK_LIST:
            logger.log(u'Stopping task ' + str(task))
            task.stop()
            task.join()
            logger.log(u'Stopped')


'''
if __name__ == '__main__':

    def timestamp(s):
        print '%.2f : %s\r' % (time.time(), s)

    def Task1(text):
        timestamp('%s' % (text))

    def Task2():
        timestamp('\tTask2')

    def Task3():
        timestamp('\t\tTask3')

    s = Scheduler()

    # -------- task - cycleTime - initdelay

    task1 = {'action': Task1, 'cycleTime': datetime.timedelta(seconds=3), 'args': 'Running Task1'}
    task2 = {'action': Task2, 'cycleTime': datetime.timedelta(seconds=30), 'runImmediately': True}
    task3 = {'action': Task3, 'cycleTime': datetime.timedelta(minutes=1), 'runImmediately': True}

    s.AddTask(**task1)
    s.AddTask(**task2)
    s.AddTask(**task3)

    print s
    s.StartAllTasks()
    raw_input()
    s.StopAllTasks()
    '''
