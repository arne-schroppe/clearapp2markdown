import sys
import sqlite3
from operator import itemgetter


def read_tasks(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''select l.title, t.title from tasks as t, lists as l where t.list_identifier = l.identifier;''')
    tasks = c.fetchall()

    c.execute('''select l.title, t.title from completed_tasks as t, lists as l where t.list_identifier = l.identifier;''')
    finished_tasks = c.fetchall()

    conn.close()

    return (tasks, finished_tasks)


def to_markdown(tasks, completed_tasks):
    def print_all(tasks):
        all = combine_lists(tasks)
        for (l, ts) in all:
            print("\n\n## " + l.strip())
            for t in ts:
                print("- " + t.strip())
            print
    print("# Tasks")
    print_all(tasks)
    print("\n\n\n# Completed Tasks")
    print_all(completed_tasks)


def combine_lists(tasks):
    all = {}
    for (task_list, task) in tasks:
        if not task_list in all:
            all[task_list] = []

        all[task_list].append(task)

    all_sorted = sorted(all.items(), key=itemgetter(0))
    return all_sorted


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        sys.exit("Expected database file name")

    file_name = sys.argv[1]
    data = read_tasks(file_name)
    to_markdown(*data)
