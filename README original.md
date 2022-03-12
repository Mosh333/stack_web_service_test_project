[![Build Status](https://travis-ci.org/403studios/stack-ws.svg?branch=master)](https://travis-ci.org/403studios/stack-ws)

**Got a question?** Email me!

# stack-ws

An implementation of the stack data structure using RESTful web services.

This is a sample project for interviewee assignments.

Contents:
  - [Installation](#installation)
  - [Configuring](#configuring)
  - [Running](#running)
  - [Examples](#examples)
  - [Documentation](#documentation)
  - [Exercise Instructions](#exercise-instructions)
    - [Instructions for Developers](#instructions-for-developers)
	- [Instructions for Testers](#instructions-for-testers)

----------

### Installation
This application has been tested using Ubuntu 14.04 LTS (Trusty Tahr) and MacOS 10.11 (El Capitan). **All versions of Windows are unsupported** and likely will not install or run. **Use at your own risk**.

The following instructions will install system-wide dependencies. Therefore, [virtualenv](https://pypi.python.org/pypi/virtualenv) is strongly recommended. You will also need to use [git](https://git-scm.com) to clone the source repository.

1. Clone repo:

        $ git clone https://github.com/403studios/stack-ws

2. Install Dependencies:

        $ pip install -r requirements.txt

### Configuring
See [application_config.py](https://raw.githubusercontent.com/403studios/stack-ws/master/stackapi/application_config.py) for a description of all configurable options.

### Running
All necessary dependencies will be installed during [Installation](#installation). To run:

    $ python run_stack_app.py

### Examples
The following examples are provided for convenience. These examples do not represent all available features. See the [API Documentation](#documentation) for a comprehensive list of all capabilities.

[Postman](https://www.getpostman.com/) is an excellent tool for testing HTTP-based APIs.

#### Using [cURL](http://curl.haxx.se)
###### Create a new stack:

    $ curl -u '<username>:<password>' -d '' http://<host>:<port>/stack
    0

If this call is successful, a stack id will be returned. This can be used for subsequent operations on this stack.

###### Push data to a stack:
Push the string 'foo' to the stack.

    $ curl -u '<username>:<password>' -d 'foo' http://<host>:<port>/stack/0
    foo

###### Read the stack:

    $ curl -u '<username>:<password>' http://<host>:<port>/stack/0
    deque(['foo'])

###### Read the size of the stack:

    $ curl -u '<username>:<password>' http://<host>:<port>/stack/0/size
    1

###### Pop data from the stack:

    $ curl -u '<username>:<password>' -X Delete http://<host>:<port>/stack/0
    foo

### Documentation
API Documentation is automatically-generated at runtime. Documentation can be accessed at: `http://<host>:<port>/documentation`

### Exercise Instructions
This exercise is aimed towards learning about an interviewee's approach to software development and testing. There is no right answer.

**Important Note:** Don't be shy! Ask questions if you're unsure of what to do. The goal of this exercise is not to trick you or evaluate your psychic abilities. We both get more out of this exercise if you ask questions and provide feedback along the way.

Feel free to use anything you have been given and any tools at your disposal.

##### Instructions for Developers
You will complete several development exercises each lasting approximately 30 minutes.

Steps to complete:

1. Familiarize yourself with the project. Read documentation provided, review any technologies in use that you aren't familiar with, review open and recently-closed issues, review code, environment, etc. You should receive a demo of this project to demonstrate functionality. If you have not, please send me an email.

2. Design and implement solutions to solve the problems/challenges given to you.

3. Test your implementation. Your solutions should be considered Production Quality and should be complete and bug free. All debugging code should be removed.

4. Once you have completed all exercises, submit your answers via email. Please email code as an attachment in a zip file.

5. Once I receive your submission, I will setup a debriefing session to review your solutions and discuss your results.

##### Instructions for Testers
Great testers are skilled in careful observation, critical thinking, and possess a rich collection of tools, information, and resources.

Using the [session-based testing](https://en.wikipedia.org/wiki/Session-based_testing) methodology, you will complete several test sessions each lasting approximately 30 minutes. Keep in mind exploratory testing is not ad-hoc testing. Exploratory testing is simultaneous learning, test design, and test execution.

Remember, a big advantage to using session-based testing is flexibility. If you discover an oddity during your session, you may want to explore it further or use this information to form subsequent test charters.

The goal of each of these test sessions is outlined by its test charter. Test charters are a guideline for you to define your testing mission and to outline what kind of problems you want to look for.

You will be given one or more testing charters. You may also be asked to create some test charters of your own to execute.

Steps to complete:

1. Familiarize yourself with the project. Read documentation provided, review any technologies in use that you aren't familiar with, review open and recently-closed issues, review code, environment, etc. You should receive a demo of this project to demonstrate functionality. If you have not, please send me an email.

2. Create any required test charters. Once complete, set up a quick review session and present your test charters to the team.

3. Execute your test session. On a small-scale project like this, each test session should take less than 30 minutes. Larger projects will generally have a longer test session time. One of the disadvantages of session-based testing is reproducibility so be sure to gather evidence and take good notes to capture your observations as you're executing test sessions. You may be asked to try to reproduce your observations.

4. Once each your test session is complete, prepare a Test Session Report. The Test Session report should consist of the following sections:

  - Session charter
  - Session length
  - Task breakdown
  - Data files
  - Test notes
  - Issues
  - Bugs

  Further info about Test Session Reports can be found [Here](https://simonsaysnomore.wordpress.com/2014/08/19/session-based-test-layout-session-report/).

5. Once all test charters are complete, setup a debriefing session to review your findings and discuss your results.
