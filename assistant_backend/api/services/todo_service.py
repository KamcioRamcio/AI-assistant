from api.models import Todo, TodoList
from django.db import models
import logging

from api.serializers import TodoSerializer, TodoListSerializer

logger = logging.getLogger(__name__)


class TodoService:
    @staticmethod
    def create_task(conversation, task_data):
        try:
            task = Todo.objects.create(
                task=task_data['name'],
                location=task_data['location'],
                deadline=task_data['deadline'],
            )
            return True, task
        except Exception as e:
            logger.error(f"Task creation failed: {str(e)}")
            return False, str(e)

    @staticmethod
    def get_user_tasks(user, todo_list_id=None):
        tasks = Todo.objects.filter(todo_list__user=user, todo_list_id=todo_list_id)
        tasks_raw = TodoSerializer(tasks, many=True).data
        if not tasks_raw:
            return "You have no tasks in your list!"

        formatted_tasks = ["Here are your tasks:\n"]

        for index, task in enumerate(tasks_raw, start=1):
            formatted_tasks.append(
                f"{index}. {task['task']}\n"
                f"   - Deadline: {task['deadline'][:10] if task['deadline'] else 'No deadline'}\n"
                f"   - Location: {task['location'] or 'Not specified'}\n"
                f"   - Status: {'Completed' if task['is_completed'] else 'Pending'}"
            )

        return "\n\n".join(formatted_tasks)


    @staticmethod
    def get_user_todo_lists(user):
        todo_lists = TodoList.objects.filter(user=user)
        return TodoListSerializer(todo_lists, many=True).data
        # if not todo_lists_raw:
        #     return "You have no todo lists!"
        #
        # formatted_todo_lists = ["Here are your todo lists:\n"]
        #
        # for index, todo_list in enumerate(todo_lists_raw, start=1):
        #     formatted_todo_lists.append(
        #         f"{index}. {todo_list['name']} - {todo_list['created_at']}\n"
        #         f"   - Tasks: {len(todo_list['todos'])}"
        #         f'\n\nWhich todo list would you like to view (number/id)?'
        #     )
        #
        # return "\n\n".join(formatted_todo_lists)
