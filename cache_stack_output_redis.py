import redis
import requests
import json, sys, os, re, pdb
sys.path.append(''.join([str(os.getcwd()),'/stackapi/']))
from application_config import *

#Initialize a redis object for global script use
redis = redis.Redis()


#Helper Functions
def print_request_object(r,method_type):
    print("Request status: "+str(r))
    print("REST method: "+method_type)
    print("URL: "+str(r.url))
    print(r.json)
    print(r.text[0:100])
    return

def return_request_object_log(r,method_type):
    log = ''

    log = log.join(['{', method_type, ', ', str(r.url), '}:{', r.text[0:100], '}'])

    return log

def invalid_test_exec_input(input_params):
    #We know input_params contains 5 or 6 inputs
    invalid_flag = False

    #Check if testcase input is correct
    testcase_int_end = re.search(r'\d+$', input_params[0])
    if testcase_int_end is None:
        invalid_flag = True

    #Check if step number input is correct
    teststep_int_end = re.search(r'\d+$', input_params[1])
    if teststep_int_end is None:
        invalid_flag = True

    if input_params[2].upper() not in ('POST','GET','HEAD', 'OPTIONS', 'DELETE'):
        invalid_flag = True

    return invalid_flag

def get_test_case_step_num(testnum):
    num = re.search(r'\d+$', testnum)
    if num is not None:
        num = int(num.group()) #get the number at end
        
    return num

def get_all_testcase_keys():
    data = []
    testcase_keys = redis.keys('testcase*')
    for key in testcase_keys:
        data.append(key.decode('ascii'))

    return data

def get_all_testcase_data():
    #Retrieve all testcase data from redis
    #we only care about keys that follow this format: testcase#
    result = []
    testcase_keys = redis.keys('testcase*')
    for key in testcase_keys:
        #Do appropriate sorting by key, and value to display correctly to user
        data = redis.hgetall(key)
        data = { key.decode('ascii'): val.decode('ascii') for key, val in data.items() }
        data = sorted(data.items())
        record = [key.decode('ascii'), data]
        result.append(record)
    
    #Python sorts by first element in sublists elements by default
    result.sort()

    return result

#Main three functions to process three input types
def process_simple_http_request(selection):

    #Quit if q command is provided
    if selection == 'q':
        return
    #Split by comma, and make necesary string formatting adjustments
    try:
        input_params = selection.split(',')
        input_params = [str(i) for i in input_params]
        input_params = [i.strip(' ') for i in input_params]
        input_params[0] = input_params[0].upper()   #upper on REST method
        input_params[2] = input_params[2].lower()   #lower on authen boolean
    except Exception as e:
        print(''.join(["Following error occured: ",str(e)]))


    #Check if argument len makes sense
    if len(input_params)<3 or len(input_params)>4:
        print('Incorrect number of inputs, expected 3 or 4 arguments!')
        return
    else:
        try:
            #try to make an HTTP request and display to user the output

            if input_params[0] == 'GET':
                if input_params[2] == 'true':
                    print(input_params[1])
                    print()
                    r = requests.get(input_params[1], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    print_request_object(r,input_params[0])

                elif input_params[2] == 'false':
                    r = requests.get(input_params[1])
                    print_request_object(r,input_params[0])
                
                else:
                    raise Exception('incorrect boolean input')

            elif input_params[0] == 'POST':

                if input_params[2] == 'true':

                    if len(input_params) == 4:
                        r = requests.post(input_params[1], data=input_params[3], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    else:
                        r = requests.post(input_params[1], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    print_request_object(r,input_params[0])

                elif input_params[2] == 'false':
                    if len(input_params) == 4:
                        r = requests.post(input_params[1], data=input_params[3])
                    else:
                        r = requests.post(input_params[1])
                    print_request_object(r,input_params[0])

                else:
                    raise Exception('incorrect boolean input')

            elif input_params[0] == 'HEAD':
                if input_params[2] == 'true':
                    print(input_params[1])
                    print()
                    r = requests.head(input_params[1], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    print_request_object(r,input_params[0])

                elif input_params[2] == 'false':
                    r = requests.head(input_params[1])
                    print_request_object(r,input_params[0])

                else:
                    raise Exception('incorrect boolean input')

            elif input_params[0] == 'OPTIONS':
                if input_params[2] == 'true':
                    print(input_params[1])
                    print()
                    r = requests.options(input_params[1], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    print_request_object(r,input_params[0])

                elif input_params[2] == 'false':
                    r = requests.options(input_params[1])
                    print_request_object(r,input_params[0])

                else:
                    raise Exception('incorrect boolean input')

            elif input_params[0] == 'DELETE':
                if input_params[2] == 'true':
                    print(input_params[1])
                    print()
                    r = requests.delete(input_params[1], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    print_request_object(r,input_params[0])

                elif input_params[2] == 'false':
                    r = requests.get(input_params[1])
                    print_request_object(r,input_params[0])

                else:
                    raise Exception('incorrect boolean input')

            else:
                print('Incorrect method type argument!')
                return
        except Exception as e:
            print(''.join(["Following error occured: ",str(e)]))
    return
    
def process_recorded_test_execution(selection):
    if selection == 'q':
        return

    #Split by comma, and make necesary string formatting adjustments
    try:
        input_params = selection.split(',')
        input_params = [str(i) for i in input_params]
        input_params = [i.strip(' ') for i in input_params]
        input_params[2] = input_params[2].upper()   #upper on REST method
        input_params[4] = input_params[4].lower()   #lower on authen boolean

    except Exception as e:
        print(''.join(["Following error occured: ",str(e)]))

    #Check if argument len makes sense
    if len(input_params)<5 or len(input_params)>6:
        print('Incorrect number of inputs, expected 5 or 6 arguments!')
        return
    elif invalid_test_exec_input(input_params):
        print('Please specify testcase and teststep number, with correct REST method!')
        return
    else:
        #Correct input, Execute Test Recording
        try:
            #Execute Test Recording, implementing necessary logic to manage the recording
            print('Currently Recording Test')

            #try to make an HTTP request and display to user the output
            #also store appropriately to redis database

            if input_params[2] == 'GET':
                if input_params[4] == 'true':
                    print(input_params[3])
                    print()
                    r = requests.get(input_params[3], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)

                elif input_params[4] == 'false':
                    r = requests.get(input_params[3])
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)               
                else:
                    raise Exception('incorrect boolean input')

            elif input_params[2] == 'POST':

                if input_params[4] == 'true':

                    if len(input_params) == 6:
                        r = requests.post(input_params[3], data=input_params[5], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    else:
                        r = requests.post(input_params[3], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)

                elif input_params[4] == 'false':
                    if len(input_params) == 6:
                        r = requests.post(input_params[3], data=input_params[5])
                    else:
                        r = requests.post(input_params[3])
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)

                else:
                    raise Exception('incorrect boolean input')

            elif input_params[2] == 'HEAD':
                if input_params[4] == 'true':
                    print(input_params[3])
                    print()
                    r = requests.head(input_params[3], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)

                elif input_params[4] == 'false':
                    r = requests.head(input_params[3])
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)

                else:
                    raise Exception('incorrect boolean input')

            elif input_params[2] == 'OPTIONS':
                if input_params[4] == 'true':
                    print(input_params[3])
                    print()
                    r = requests.options(input_params[3], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)

                elif input_params[4] == 'false':
                    r = requests.options(input_params[3])
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)
                else:
                    raise Exception('incorrect boolean input')

            elif input_params[2] == 'DELETE':
                if input_params[4] == 'true':
                    print(input_params[3])
                    print()
                    r = requests.delete(input_params[3], auth=(HTTP_AUTH_USERNAME, HTTP_AUTH_PASSWORD))
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)

                elif input_params[4] == 'false':
                    r = requests.get(input_params[3])
                    
                    testcase_num = 'testcase'+str(get_test_case_step_num(input_params[0]))
                    teststep_num = str(get_test_case_step_num(input_params[1]))
                    log = return_request_object_log(r,input_params[2])
                    redis.hset(testcase_num, teststep_num, log)

                else:
                    raise Exception('incorrect boolean input')

            else:
                print('Incorrect method type argument!')
                return 

        except Exception as e:
            print(''.join(["Following error occured: ",str(e)]))
    return

def process_redis_query(selection):
    if selection == 'q':
        return

    #Split by comma, and make necesary string formatting adjustments
    try:
        result = []
        testcase_num = re.search(r'\d+$', selection)   #grab digits at the end
        if testcase_num is not None:
            testcase_num = testcase_num.group()

        result = []
        testcase_keys = redis.keys('testcase'+str(testcase_num))
        if len(testcase_keys) == 0:
            print(result)
        else:
            for key in testcase_keys:
                #Do appropriate sorting by key, and value to display correctly to user
                data = redis.hgetall(key)
                data = { key.decode('ascii'): val.decode('ascii') for key, val in data.items() }
                data = sorted(data.items())
                record = [key.decode('ascii'), data]
                result.append(record)
            
            #Python sorts by first element in sublists elements by default
            result.sort()
            print(result)
    except Exception as e:
        print(''.join(["Following error occured: ",str(e)]))
    return



def stack_ws_terminal():
    #main driver method to interact with tester
    while True:
        print("(1) Make a simple HTTP query? (2) Make a recorded test case execution? (3) Query Redis Database?")
        selection = input("Pick 1, 2, or 3: ")
        try:
            if selection == '1':
                while True:
                    print('**************************************************************************************')
                    print("(1) Enter a simple HTTP query to execute. Syntax: method_type, URL, authentication_boolean, optional_POST_data")
                    cmd = input('e.g. GET, http://127.0.0.1:5000/stack/2, TRUE>>> ')
                    if cmd != 'q': 
                        process_simple_http_request(cmd)
                    else:
                        break
            elif selection == '2':
                while True:
                    print('**************************************************************************************')
                    print("(2) Create a recorded test case execution. Syntax: testcase#, step#, method_type, URL, authentication_boolean, optional_POST_data")
                    print(''.join(["Existing Recorded Test Cases: ",str(get_all_testcase_data())]))
                    cmd = input('e.g. testcase4, step2, POST, http://127.0.0.1:5000/stack/0, TRUE, 43>>> ')

                    if cmd != 'q':
                        process_recorded_test_execution(cmd)
                    else:
                        break
            elif selection == '3':
                while True:
                    print('**************************************************************************************')
                    print("(3) Query old test cases in redis. Syntax: testcase#")
                    print("Existing keys in redis: " + str(get_all_testcase_keys()))
                    cmd = input('e.g. testcase3>>> ')
                    if cmd != 'q':
                        process_redis_query(cmd)
                    else:
                        break
            elif selection == 'q':
                print('exiting stack_ws_terminal now')
                break
            else:
                print('Invalid selection! Pick 1, 2, or 3. q to quit.')
        except Exception as e:
            print(''.join(["Following error occured: ",str(e)]))

if __name__ == '__main__':
    stack_ws_terminal()

