# Application 1 : Rule Engine with AST
> Zeotap | Software Engineer Intern | Assignment | Application 1

## Applicant Introduction
Hi! I am Ayush, prev. JP Morgan Chase, Google Summer of Code. Although all of
this is already written on my GitHub profile, I'd still want to point to my 
[LinkedIn](https://www.linkedin.com/in/theayushanand/).

## Table of Contents
+ [Introduction](#introduction)
+ [Technical Parts](#technical-parts)
  - [Installation](#installation)
  - [How to run](#how-to-run)
+ [About Solution](#about-solution)
  - [Solution Overview](#solution-overview)
  - [Code Structure](#code-structure)
+ [Non Technical Parts](#non-technical-parts)
  - [My Approach](#my-approach)
  - [Feedback](#feedback)
+ [Outro](#outro)

## Introduction
> I read the assginment description a lot of times, so as to make sure I don't 
> miss on anything important. 


Most of the code I have written would seem like a story, so I made sure the README 
doesn't :D. Everything would mostly be in bullets hereafter:
* code is heavily commented and accompany suitable docstrings (React code 
  compatible with Doxygen, and Python code with Sphinx).
* Unittests are written keeping in mind all edge cases that could occur, there are 
  positive as well as negative test cases. Coverage too is kept above 80%.
* This README will talk about the technical parts first, then about the solution.
  And later about all miscellenous things, which are although technical, yet I put
  them in the "non-technical" bracket. They talk more about my thinking and approach
  towards the solution, and a brief discussion on the design is also present.

## Technical Parts
### Installation
I have tried my best to make it platform agnostic, and packaged everything into a 
Docker Container. You can also execute the below seperately for running them on 
your machine without Docker.

+ Frontend
    ```bash
    cd frontend/
    pnpm install
    ```
+ Backend

    If `poetry` isn't previously installed, install it first. 
    ```bash
    python3 -m venv $VENV_PATH
    $VENV_PATH/bin/pip install -U pip setuptools
    $VENV_PATH/bin/pip install poetry
    ```

    Then continue to create a venv, and install dependencies
    ```bash
    cd backend/
    poetry install
    ```

+ Database

    After a `poetry install`, execute the following to setup raw data in your 
    postgres instance. Make sure to populate the connection creds in the `.env`.
    ```bash
    poetry run python main.py --migrate
    ```

### How to run
Expecting that above installation process, suceeded.

+ Frontend
    ```bash
    pnpm run dev
    ```
+ Backend
    ```bash
    poetry run python main.py --dev
    ```
+ Database
    ```bash
    poetry run python main.py --db-start
    ```

## About Solution
### Solution Overview
### Code Structure
### Design Discussion

## Non Technical Parts
### My Approach
### Feedback

## Outro

Thanks.
