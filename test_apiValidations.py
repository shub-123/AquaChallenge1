import requests
import json
from utilities.configurations import get_host_url, get_jsondata, modify_json, get_host_resouces

"""Below function will use GET Request to view all the tasks present"""


def test_get_all_tasks():
    global response
    response = requests.get(get_host_url() + get_host_resouces()["host_resource1"])

    if response.status_code != 200:
        print("The Get Request is not successful, getting error code as", response.status_code)
    json_response = response.json()

    print("****************************Printing the entire lists of tasks******************************")
    print()
    print(json_response)

    '''Assert whether Get Request is successful or not'''
    assert response.status_code == 200

    '''Assert if the Json Heaaders Content- Type contains application/json'''
    headers = response.headers

    '''Open json_data file conatining headers info'''
    with open("C:\\Users\\Admin\\Downloads\\Challenge1\\utilities\\data.json") as jsonfilepointer:
        header_data = json.load(jsonfilepointer)
        content_type = header_data["Content-Type"]
        assert content_type == headers["Content-Type"]

    return response


def test_create_task(taskname, completion_status):
    """ We will be calling json from the configuration file where the data is parsed"""
    create_task_request = requests.post(get_host_url() + get_host_resouces()["host_resource1"], json=get_jsondata(taskname, completion_status))
    create_task_response = create_task_request.json()

    '''Verify if the Post request is completed or not'''
    assert create_task_request.status_code == 200

    '''if the status code for the post is 200 the we will print the whole data to console
    and we willl be checking that the response hsould no be empty dictionary'''
    if create_task_request.status_code == 200 and create_task_response != {}:
        print()
        print("New Task Created Successfully: -->", create_task_response)

        '''NOw if everthing works fine we will call the get task funcion whihc will
         check if the id created via POST is displaying correctly or not'''

        test_get_single_task(create_task_response["task_id"], taskname, completion_status)

        '''In the below code we will call the modify method and give the task id whihc is created via
         and taskname and completion status ia modify json function form configurations'''
        modify_task(create_task_response["task_id"])

        '''Below code  will call the Task Complete function and pass the taskid  and make it complete'''
        mark_test_completed(create_task_response["task_id"])

        '''Below code will call marke task incomplete and then verifes that the task is successfully incompleted'''
        mark_task_incomplete(create_task_response["task_id"])

        '''Below code will call delete task and the verifies that the task is successfullly deletd or not'''
        delete_task(create_task_response["task_id"])

    else:
        print("Task not Created", create_task_request.status_code)


def test_get_single_task(creation_task_id, task_name, completion_status):
    get_single_task_response = requests.get(get_host_url() + get_host_resouces()["host_resource2"] + creation_task_id)
    json_single_task_response = get_single_task_response.json()
    assert get_single_task_response.status_code == 200

    '''If the get request is successful, we will print the data to the console'''
    if get_single_task_response.status_code == 200 and json_single_task_response != {}:
        print()
        print("Following Created/MOdified Task is gettting viewed successfully via GET Single Request -->", "Task_id:", creation_task_id, json_single_task_response)
    else:
        print("There is an error in the GET request, Error Code", get_single_task_response.status_code)

    '''Now we will be asserting if the response header containes Content Type as application/json
    Here we can use the same approach we did for GET tasks'''

    headers = get_single_task_response.headers

    '''Open json_data file conatining headers info'''
    with open("C:\\Users\\Admin\\Downloads\\Challenge1\\utilities\\data.json") as jsonfilepointer:
        header_data = json.load(jsonfilepointer)
        content_type = header_data["Content-Type"]
        assert content_type == headers["Content-Type"]

    '''Below code will validate if the response of the Get Single Task is equal to the request of 
    the POST single task '''

    assert json_single_task_response["task"] == task_name
    assert json_single_task_response["completed"] == completion_status

    '''Now we will send the same arguments to verify_singletask_in_get_all_tasks function
    to see that the single data should be present in all tasks list'''

    test_verify_singletask_in_get_all_tasks(creation_task_id, task_name, completion_status)


'''Below function will verify if the single task created is presen in the whole tasks list or not'''


# @pytest.mark.run(order=4)
def test_verify_singletask_in_get_all_tasks(task_id, task_name, completion_status):
    all_tasks_data = test_get_all_tasks()
    task = {"id": task_id, "task": task_name, "completed": completion_status}

    for data in all_tasks_data.json():
        if data == task:
            print()
            print("Created?Modified Task: ", data, "is present in the entire task list")
            break
    else:
        print("Following Task, ", task, "is not present in the task List")


'''Below function is to Get all the tasks and verify that the Get status is successful and if there is error we get the 
status code of the bad request and also to check if the Header Content type is application/json'''


def modify_task(task_id):
    modify_task_request = requests.put(get_host_url() + get_host_resouces()["host_resource2"] + task_id, json=modify_json())
    modify_task_response = modify_task_request.json()

    body = modify_json()
    task = body["task"]
    completion_status = body["completed"]
    '''Verify that the put request is successful'''
    assert modify_task_request.status_code == 200

    '''Once verified that the task modified successfully, we will print the response'''
    if modify_task_request.status_code == 200 and modify_task_response != {}:
        print()
        print(f"Task with task_id {task_id} is Modified successfully with following data:", modify_task_response, modify_json())

    """Now we will call the GET Request to verify if the new data is getting displayed after
    the modification"""
    test_get_single_task(modify_task_response['task_id'], task, completion_status)


'''This function will first make the task id as Completed, verify that the POST request is successful
we will verify that the get task has the mark as completed for the same task id'''


def mark_test_completed(task_id):
    mark_completed_request = requests.post(get_host_url() + get_host_resouces()["host_resource2"] + task_id + "/completed")
    mark_completed_response = mark_completed_request.json()

    assert mark_completed_request.status_code == 200

    """If POST request is successsful we willl validate that the reponse body is empty dict"""
    if mark_completed_request.status_code == 200 and mark_completed_response == {}:
        print()
        print(f"Mark task with task_id: {task_id} as Completion Successful.", mark_completed_response)
        verify_task_completion(task_id)

    else:
        print("Mark completion not successful", mark_completed_request.status_code)


def verify_task_completion(task_id):
    verify_completion_request = requests.get(get_host_url() + get_host_resouces()["host_resource2"] + task_id)
    verify_completion_response = verify_completion_request.json()

    """Verify if the GET request is successsful or not"""
    assert verify_completion_request.status_code == 200

    if verify_completion_request.status_code == 200 and verify_completion_response != {}:
        print()
        print(f"The task mark with task_id:  {task_id} as completed is verified successfully:", verify_completion_response)
    else:
        print("The task has not marked completed:", verify_completion_request.status_code)

    """Verify the same task is present in all the tasks list"""
    test_verify_singletask_in_get_all_tasks(task_id, verify_completion_response["task"],
                                            verify_completion_response["completed"])


def mark_task_incomplete(task_id):
    mark_incomplete_request = requests.post(get_host_url() + get_host_resouces()["host_resource2"] + task_id + "/incomplete")
    mark_incomplete_response = mark_incomplete_request.json()

    assert mark_incomplete_request.status_code == 200

    """If POST request is successsful we willl validate that the reponse body is empty dict"""
    if mark_incomplete_request.status_code == 200 and mark_incomplete_response == {}:
        print()
        print(f"Mark task with task_id: {task_id} as Incomplete Successful", mark_incomplete_response)
        verify_task_incomplete(task_id)

    else:
        print("Mark completion not successful", mark_incomplete_request.status_code)


def verify_task_incomplete(task_id):
    verify_incomplete_request = requests.get(get_host_url() + get_host_resouces()["host_resource2"] + task_id)
    verify_incomplete_response = verify_incomplete_request.json()

    """Verify if the GET request is successsful or not"""
    assert verify_incomplete_request.status_code == 200

    if verify_incomplete_request.status_code == 200 and verify_incomplete_response != {}:
        print()
        print(f"The task with task_id: {task_id} has marked incompleted: ", verify_incomplete_response)
    else:
        print("The task has not marked incompleted:", verify_incomplete_request.status_code)

    """Verify the same task is present in all the tasks list"""
    test_verify_singletask_in_get_all_tasks(task_id, verify_incomplete_response["task"],
                                            verify_incomplete_response["completed"])


def delete_task(task_id):
    delete_task_request = requests.delete(get_host_url() + get_host_resouces()["host_resource2"] + task_id)

    """Verify if the deletion is successful"""
    assert delete_task_request.status_code == 200

    if delete_task_request.status_code == 200:
        print()
        print(f"Task with task_id: {task_id} task_id Deleted successfully", delete_task_request.status_code)
        verify_delete_successful(task_id)
    else:
        print("Task not Deleted successfully", delete_task_request.status_code)


"""This function will check if the data is present or not, it should get us an empty dict on GET Request"""


def verify_delete_successful(task_id):
    verify_incomplete_request = requests.get(get_host_url() + get_host_resouces()["host_resource2"] + task_id)
    verify_incomplete_response = verify_incomplete_request.json()

    """Verify if the GET request is successsful or not"""
    assert verify_incomplete_request.status_code == 404

    if verify_incomplete_request.status_code == 404 and verify_incomplete_response == {}:
        print()
        print(f"The task with task_id: {task_id} has deleted successfully:", verify_incomplete_response)
        verify_delete_task_in_taskslist(task_id)
    else:
        print("The task has not deleted successfully:", verify_incomplete_request.status_code)


def verify_delete_task_in_taskslist(task_id):
    tasks = test_get_all_tasks()
    for task in tasks.json():
        if task["id"] == task_id:
            print()
            print("Error, delete not successful, The task is present in the list", task)
            break
    else:
        print(f"This task with task_id : {task_id} is not present in the Tasks list")


'''Get all Tasks'''
test_get_all_tasks()

'''Create a single task'''
test_create_task("Shubham Task", "true")
