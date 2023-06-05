# Tutor Me Project built in CS 3240

Group ID: A-13



Common Requirements
All projects must do the following, regardless of idea chosen:

All projects must incorporate Google user accounts as the primary way that someone logs into the system. You will need to use the Google account API to make this work. There are several libraries that are built for Django to work with Google accounts with tutorials.
You will have to create two different user access levels for each project. This will take a slightly different form with each project, but the basic idea is some users will be “common” users and some users will be “administrative” users. Users of one type should not be able to access features of the other type!
The two test accounts we will use will be: common user - cs3240.student@gmail.com and admin user - cs3240.super@gmail.com
All projects must incorporate the SIS API that we will provide information about.
All projects must be built using the prescribed language (Python 3), framework (Django 4), build environment (GitHub Actions CI), source control management (GitHub), and cloud hosting (Heroku). No exceptions to these will be granted.
You must use the PostgreSQL database engine for production on Heroku and continuous integration (on GitHub Actions). You are allowed to use SQLite for local testing so you do not have to install PostgreSQL on your own machine, but another option is to change your settings.py file point to the PostgreSQL DB on Heroku at all times.

Project Option 3: Tutor Me
Students are often looking for tutors for courses. This app will help facilitate this matching.

Tutors (this projects “administrator” user type) must be able to post the courses that they can tutor by searching through the set of courses by course mnemonic, course number, or course name.
Tutors can post their hourly rate and available time frames.
Students must be able to search for tutors by class, searching by course mnemonic, course number, or course name.
When a student finds a tutor they would like to work with, they must be able to submit a request for tutoring at a particular time. This time must fall within the tutor’s posted available time frames.
Tutors can then see their requests when they login. They can then approve or reject a tutoring session, which will show up on the student’s page when they login.

Isaiah Parr - DevOps manager
Stacy Meng
Alexis Mann
Meyers Li
Mehmet Yaylagul
