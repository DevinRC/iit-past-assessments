# import libraries / packages
import datetime

# initialize variables
company_name = "XYZ Company"
workers = 0
choice = 0
all_projects = []
completed_projects = []
execute = True
project_names = []
possible_inputs = ["ongoing", "completed", "onhold"]
statistics_list = [0] * len(possible_inputs)
redirect_choice = False
redirect_to = None


def menu(
    redirect: bool = False,
    to: int = None,
    name_of_the_company: str = company_name,
    msg: str = "Enter your choice: ",
) -> str:
    """This function finds the choice that should be displayed to the user next...

    Keyword arguments:
    redirect (bool) -- A boolean to know whether or not the user will be redirected
    to (int) -- The choice that user will be redirected to
    name_of_the_company (str) -- The companies name that will be displayed
    msg (str) -- The message that will be displayed to the user asking their next choice

    Return: (str) the next choice which the user has chosen...
    """
    main_menu = f"""
     {name_of_the_company}
     Main Menu
     1. Add a new project to existing projects.
     2. Remove a completed project from existing projects.
     3. Add new workers to available workers group.
     4. Updates details on ongoing projects.
     5. Project Statistics.
     6. Exit
    """.center(
        14
    )
    print(
        "Redirecting..." if redirect else main_menu
    )  # checking if the `redirect` variable is True if it is then "Redirecting..." if not then the main menu is displayed
    return (
        to if redirect else str(input(msg))
    )  # returning the variable `to` if `redirect` variable is True if it isnt then the user is asked an input with the `msg` string


def remove_completed_projects(
    code_of_project: str,
    every_project: list,
    workers_tot: int,
    stats_list: list,
    complete_projects: list,
    possible_stats: list,
) -> (bool, str):
    """Remove completed projects
    Keyword arguments:
    code_of_project (str) -- The code of the project that will be removed
    every_project (list) -- A list which contains all the projects which haven't been removed
    workers_tot (int) -- The number of workers
    stats_list (list) -- The list that tracks the statistics for choice (5)
    complete_projects (list) -- The list which contains all removed completed projects
    possible_stats (list) -- All the possible status
    Return: Tuple[A boolean which states whether or not the operation was successful, A string which has an output msg regarding the operation if it was successful or not.]
    """
    try:
        index_of_project = project_names.index(
            code_of_project
        )  # geting the index of the project
        actual_end_date = datetime.datetime.now().strftime(
            "%m/%d/%Y"
        )  # getting the current date
        (
            code_of_project,
            clients_name,
            start_date,
            expected_end_date,
            number_of_workers,
            old_project_status,
            index,
        ) = every_project[
            index_of_project
        ]  # assigning the details from the project_details
        completed_project_details = [
            code_of_project,
            clients_name,
            start_date,
            expected_end_date,
            number_of_workers,
            actual_end_date,
        ]  # create a new data structure which contains the details for an completed project
        if old_project_status == "ongoing":
            workers_tot += number_of_workers  # if the old project status is ongoing then the workers in the project are added back to the `workers_tot` variable
        stats_list[index] -= 1  # subtracting 1 from the old_status index
        stats_list[
            possible_stats.index("completed")
        ] += 1  # adding 1 for the completed statistics
        complete_projects.append(
            completed_project_details
        )  # append the `completed_project_details` list to the main complete_projects list
        del every_project[
            index_of_project
        ]  # delete the project from `every_project` list
        del project_names[
            index_of_project
        ]  # delete the project_code from the `project_names` list
        return (
            True,
            "Successfully removed completed projects.",
            workers_tot,
            status_list,
            completed_projects,
            every_project,
            project_names,
        )
    except Exception as e:
        return (
            False,
            e,
            workers_tot,
            status_list,
            completed_projects,
            every_project,
            project_names,
        )
    # return the (execution status, response message, workers_tot, status_list, completed_projects, every_project, project_names)


def create_project(
    status_list: list,
    index: int,
    code_of_project: str,
    clients_name: str,
    start_date: str,
    expected_end_date: str,
    number_of_workers: str,
    project_status: str,
    workers_tot: int,
    project_names: list,
    all_projects: list,
) -> (bool, str):
    """This function creates a new project
    Keyword arguments:
    status_list (list) -- The list that is used for project statistics
    index (index) -- The index of the project status in the status list
    code_of_project (str) -- The code of the project
    clients_name (str) -- The project's clients name
    start_date (str) -- The start date of the project
    expected_end_date (str) -- The expected end date of the project
    number_of_workers (str) -- The number of workers required for the project
    project_status (str) -- The status of the project out of (ongoing,on hold, completed)
    workers_tot (int) -- total number of workers in the organization
    project_names (list) -- a list that contains all the project codes
    all_projects (list) -- a list that contains all the projects
    Return: Tuple[
        A boolean which shows if the function successfully executed or not,
        The message which will be displayed to the user
    ]
    """
    try:
        status_list[index] += 1  # add 1 to the statistics list that tracks the entire
        project_data = [
            code_of_project,
            clients_name,
            start_date,
            expected_end_date,
            number_of_workers,
            project_status,
            index,
        ]  # create a list with the details that are required
        if project_status == "ongoing" and (
            number_of_workers > workers_tot
        ):  # checking if the project status is "ongoing" and if `number_of_workers` is greater than `workers_tot` variable
            return (
                False,
                "There is not enough workers",
                workers_tot,
                all_projects,
                project_names,
            )
        if project_status == "ongoing":  # checking if the project status is "ongoing"
            workers_tot -= number_of_workers  # subtracting the workers that were entered by the user by the total workers available
        project_names.append(
            code_of_project
        )  # appending the project code to the `project_names` list
        all_projects.append(
            project_data
        )  # appending the project date to the `all_projects` list
        return (
            True,
            "Successfully created a new project",
            workers_tot,
            all_projects,
            project_names,
        )
    except Exception as e:
        return (False, e, workers_tot, all_projects, project_names)
    # return the (execution status, response message, workers_tot,all_projects, project_names)


def update_project_details(
    status_list: list,
    index: int,
    previous_index: int,
    code_of_project: str,
    clients_name: str,
    start_date: str,
    expected_end_date: str,
    number_of_workers: str,
    project_status: str,
    current_workers: int,
    workers_tot: int,
    previous_project_status: str,
) -> (bool, str):
    """An function that updates the project details
    Keyword arguments:
    status_list (list) -- The list that is used for project statistics
    index (int) -- The index of the new project status in the status_list
    previous_index (int) -- The index of the previous project status in the status_list
    code_of_project (str) -- The project code of the project
    clients_name (str) -- The (updated / usual) client name
    start_date (str) -- The (updated / usual) start date
    expected_end_date (str) -- The (updated / usual) end date
    number_of_workers (str) -- The (updated / usual) number of workers
    project_status (str) -- The (updated / usual) project status
    current_workers (int) -- The number of workers before the project was updated
    workers_tot (int) -- The total number of workers
    previous_project_status (str) -- The previous project status
    Return: Tuple[
        A boolean which shows if the function successfully executed or not,
        The message which will be displayed to the user
    ]
    """
    try:
        if (
            number_of_workers
            > workers_tot
            + (current_workers if previous_project_status == "ongoing" else 0)
            and project_status == "ongoing"
        ):  # checking if there is enough workers if the project_status is "ongoing" to make sure that workers are going to be assigned, and then we check if the there is enough workers to add a project
            return (False, "Workers chosen are too much", workers_tot)
        if project_status == "ongoing":  # checking if the project status is "ongoing"
            workers_tot -= number_of_workers  # subtracting the number_of_workers from the workers total
        if (
            previous_project_status == "ongoing"
        ):  # checking if the project status is "ongoing"
            workers_tot += (
                current_workers  # adding the current_workers from the workers total
            )
        status_list[index] += 1  # updating the statistics_list of the new status
        status_list[
            previous_index
        ] -= 1  # updating the statistics metrics of the old status
        project_data = [
            code_of_project,
            clients_name,
            start_date,
            expected_end_date,
            number_of_workers,
            project_status,
            index,
        ]  # create an project_data list which contains all the data
        index = project_names.index(
            code_of_project
        )  # finding the index of the project_code
        all_projects[
            index
        ] = project_data  # reassign the all_projects index to the project_data list
        return (True, "Project details updated successfully", workers_tot)
    except Exception as e:
        return (False, e, workers_tot)
    # return the (execution status, response message, workers_tot)


def date_verification(msg: str) -> str:
    """A function that uses recursion to make sure that the entered date is in a correct format...
    Keyword arguments:
    msg (str) -- the message that should be displayed...
    Return: A string which contains a correct date format...
    """
    try:
        date = input(msg)  # asking the user for an input
        splitted_date = date.split(
            date[2] if len(date) > 3 else " "
        )  # splitting the data with the second element (starting from 0) the string
        if (
            len(splitted_date) != 3
        ):  # checking if there is 3 elements in the list of the splitting string
            print("Enter a valid format of the date..!")
            return date_verification(msg)
        month, date, _ = splitted_date  # splitting the list into month, date, and yrs
        if int(month) > 12:  # checking if the months are bigger than 12
            print("Enter a valid month..!")
            return date_verification(msg)
        if int(date) > 31:  # checking if the date is higher than 31
            print("Enter a valid date..!")
            return date_verification(msg)
        return date
    except:
        print("An error occured please enter the value again..!")
        return date_verification(msg)


def project_status_verification(
    msg: str = "Project Status (ongoing/completed/on hold) : ",
    update_status: bool = False,
) -> (str, list, int):
    """An function that uses recursion to make sure that an input is enter as required
    Keyword arguments:
    msg -- The message that should be displayed to the user to get the project status input
    update_status -- Whether to update the status count
    Return: Tuple[The state enter by the user,
                    the statistic list used to track the project status count,
                    the index of the enter state
                ]
    """
    project_state = (
        str(input(msg)).replace(" ", "").lower()
    )  # asking the user for the project_status and then replacing " " with "" and lowering the entire string
    if (
        project_state not in possible_inputs
    ):  # checking if the project_state is not in the possible_inputs
        print("The entered project status is incorrect...")
        return (
            project_status_verification()
        )  # Calls the project_status_verification() function (itself)
    if update_status:  # checking if the `update_status` boolean is True
        statistics_list[
            possible_inputs.index(project_state)
        ] += 1  # update the statistics_list
    return (
        project_state,
        statistics_list,
        possible_inputs.index(project_state),
    )  # returning (project_state,statistics_list,index)


def project_code_verification(msg: str, project_codes: list) -> str:
    """Project Code Verification function with the use of recursion...
    Keyword arguments:
    msg (str) -- The message that is displayed and ask the user to enter the project code
    project_codes (list) -- The list of project codes that already exists
    Return: (str) of a project code that doesnt already exist...
    """
    project_code = str(input(msg))  # asking the user for an project_code input
    if (
        project_code in project_codes
    ):  # checking if the project code in `project_codes` list
        print("Project Code already exists..!")
        return project_code_verification(
            msg, project_codes
        )  # return the same function (recursion)
    return project_code  # return the project_code


def check_if_int(msg) -> int:
    try:
        return int(input(msg))  # ask the user an input by displaying the `msg` variable
    except:
        print("The msg entered was not an integer")
        return check_if_int(msg)  # if an error is caused by trying to turn the input


while execute:
    choice = menu(redirect=redirect_choice, to=redirect_to)  # call the menu() function
    redirect_choice, redirect_to = False, None
    if choice == "1":  # checking if the message entered is "1"
        print(
            f"""
            {company_name}
            Add a new project
          """.center(
                14
            )
        )
        code_of_project = project_code_verification(
            "Project Code : ", project_names
        )  # ask the user for the project code
        if code_of_project == "0":  # checking if the project_code entered is "0"
            continue
        clients_name = str(
            input("Clients Name : ")
        )  # ask the user for the clients_name
        start_date = date_verification(
            "Start Date (MM/DD/YYYY) : "
        )  # ask the user for the start date
        expected_end_date = date_verification(
            "Expected end date (MM/DD/YYYY) : "
        )  # ask the user for the start_date
        number_of_workers = check_if_int(
            "Numbers of Workers : "
        )  # ask the user for the number_of_workers
        (
            project_status,
            status_list,
            index,
        ) = project_status_verification()  # ask the user for the project_status
        save = str(
            input("Do you want to save the project(Yes/No)? ")
        )  # ask the user if they wanna save the project
        if save.upper() == "YES":
            (
                execution_status,
                response_msg,
                workers,
                all_projects,
                project_names,
            ) = create_project(
                status_list,
                index,
                code_of_project,
                clients_name,
                start_date,
                expected_end_date,
                number_of_workers,
                project_status,
                workers,
                project_names,
                all_projects,
            )  # calling the `create_project()` function
            print(
                f"{response_msg} ({execution_status})"
            )  # print out the response_msg and execution_status
        else:
            print("The project was *not* saved ..!")

    elif choice == "2":  # checking if the entered choice is "2"
        print(
            f"""
      {company_name}
      Remove Completed Project
    """.center(
                14
            )
        )
        code_of_project = str(
            input("Project Code : ")
        )  # asking the user for the project_code
        if (
            code_of_project not in project_names
        ):  # checking if the project_code is not already in the project_names list
            print("The project does not exist")
            continue
        save = str(
            input("Do you want to remove the project (Yes/ No)? ")
        )  # asking the user if they wanna remove the project
        if save.upper() == "YES":
            (
                execution_status,
                response_msg,
                workers,
                status_list,
                completed_projects,
                every_project,
                project_names,
            ) = remove_completed_projects(
                code_of_project,
                all_projects,
                workers,
                statistics_list,
                completed_projects,
                possible_inputs,
            )  # calling the `remove_completed_projects()`
            print(f"{response_msg} ({execution_status})")
        else:
            print(
                "The project was not removed..!"
            )  # print out the response_msg and execution_status

    elif choice == "3":  # if the user enters "3"
        print(
            f"""
      {company_name}
      Add new Workers
    """.center(
                14
            )
        )
        new_no_of_workers = check_if_int(
            "Number Workers to Add : "
        )  # asking the user for the number of workers to add
        if new_no_of_workers < 0:  # making sure that there is more than zero worker
            print("Workers must be more than 0..!")
            continue
        save = str(
            input("Do you want to add ? (Yes / No) ")
        )  # asking the user if they wanna add the the project
        if save.upper() == "YES":  # checking if the user entered "YES"
            workers += new_no_of_workers  # adding the number of workers to the total available worker list
            print("Workers added successfully..!")
        else:
            print("Workers were not added..!")

    elif choice == "4":  # check if the user entered is "4"
        print(
            f"""
      {company_name}
      Update Project Details
    """.center(
                14
            )
        )
        code_of_project = str(input("Project Code : "))  # enter the project code
        if (
            code_of_project not in project_names
        ):  # checking if the project_code is in the project_names list
            print("There isn't a project with the mentioned project code..!")
            continue
        if (
            code_of_project.replace(" ", "") == "0"
        ):  # checking if the project_code is zero
            continue
        clients_name = str(
            input("Clients Name : ")
        )  # asking the user for the clients name
        start_date = date_verification(
            "Start Date (MM/DD/YYYY) : "
        )  # asking the user for the start date
        expected_end_date = date_verification(
            "Expected end date (MM/DD/YYYY) : "
        )  # asking the user for the expected end date
        number_of_workers = check_if_int(
            "Numbers of Workers : "
        )  # asking the user for the number of workers
        (
            project_status,
            status_list,
            index,
        ) = project_status_verification()  # asking the user for the project status
        save = str(
            input("Do you want to update the project details (Yes/No)?")
        )  # asking the user if they wanna update the project_details
        if save.upper() == "YES":
            (
                current_workers,
                previous_project_status,
                previous_index,
            ) = all_projects[project_names.index(code_of_project)][
                4:
            ]  # assigning the current_workers, previous_project_status, previous_index to the [4:]
            execution_status, response_msg, workers = update_project_details(
                status_list,
                index,
                previous_index,
                code_of_project,
                clients_name,
                start_date,
                expected_end_date,
                number_of_workers,
                project_status,
                current_workers,
                workers,
                previous_project_status,
            )  # call the `update_project_details` method
            print(
                f"{response_msg} ({execution_status})"
            )  # printing out the response msg and the execution status
        else:
            print("The project was not updated")

    # When user choice is 5
    elif choice == "5":  # checking if the user entered "5"
        print(
            f"""
      {company_name}
      Project Statistics
    """.center(
                14
            )
        )
        for idx, item in enumerate(
            possible_inputs
        ):  # iterating the possible_inputs using `enumerate` function
            print(f"Number of {item} projects : {statistics_list[idx]}")
        print(f"Number of available workers : {workers}")
        add_project = str(
            input("Do you want to add the project (Yes/No)?")
        )  # asking the user if they wanna add the project
        if (
            add_project.upper() == "YES"
        ):  # checking if the user says they wanna add the project
            redirect_choice, redirect_to = (
                True,
                "1",
            )  # setting variables so that they can change redirect the user to the "1" choice

    elif choice == "6":  # checking if the user entered "6"
        print("Exiting Program...")
        execute = False  # setting execute to False so the program stops

    else:
        print("Please enter a valid choice..!")
