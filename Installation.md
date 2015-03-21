# Requiremenets #
  * [Taskwarrior](http://taskwarrior.org/)
  * [Python 2.7](http://python.org/) although it should also work on lower version

# Installation #
Copy the task-review script somewhere in your $PATH and start using it, simple as that :)

# Known issues #
  * The script won't work properly if you delete a task and you run taskwarrior in another terminal. The reason is that the garbage collector of task will change the ids of the tasks.