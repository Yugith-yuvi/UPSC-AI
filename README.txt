UPSC PYQ quiz: beginner setup
============================

Files
-----
upsc_app.py      Your Streamlit frontend, updated to call the local backend.
upsc_backend.py  Your FastAPI backend, updated to filter the selected year range.
requirements.txt Python packages required by both files.

Run it on Windows
-----------------
1. Install Python from https://www.python.org/downloads/ if it is not installed.
   During setup, enable "Add Python to PATH".

2. Open PowerShell in this folder (the folder containing these files) and run:

   py -m pip install -r requirements.txt

3. In that PowerShell window, start the backend:

   py -m uvicorn upsc_backend:app --reload

   Keep this window open. The backend address is http://localhost:8000.
   You can open http://localhost:8000/docs to see its API documentation.

4. Open a second PowerShell window in this same folder and run:

   py -m streamlit run upsc_app.py

5. Streamlit will open the app in your browser. Go to Menu > Prelims PYQ Quiz,
   choose a subject and year range, then click Generate Quiz Test.

Put it online so it starts automatically
----------------------------------------
The included render.yaml describes two always-on Render services (the Streamlit
app and FastAPI API) plus a persistent disk for the SQLite question database.
Render can redeploy these services automatically after you push code changes
to GitHub.

1. Open your GitHub repository in a browser.
2. Add these files to the top level (root) of the repository:
   upsc_app.py, upsc_backend.py, requirements.txt, and render.yaml.
   You can also add this README.txt for reference.
3. Save the changes with GitHub's Commit changes button.
4. Sign in to Render, choose New > Blueprint, and connect the repository.
5. Render will show the services and estimated charges before creation. Review
   that screen before you confirm. The current setup uses two Starter web
   services and a 1 GB persistent disk; current listed rates work out to about
   $14.25/month before taxes, bandwidth, and other usage. Do not choose Apply
   unless that recurring cost is acceptable to you.
6. After the deploy completes, open the app service URL. Try the quiz and make
   sure the API returns questions. The API documentation is at the backend
   service URL followed by /docs.
7. Later, when you edit a file in GitHub and commit it, Render automatically
   builds and deploys the update. You do not need to start the app on your PC.

This makes the quiz app hosted online; it does not yet charge users. Before
charging users, you still need a payment account, user sign-in, subscription
checkout and cancellation, a webhook to update paid access, and a clear rule
for which app features are free or paid. Payment-provider setup depends on the
country where your business is registered.

Important question-bank note
----------------------------
The backend currently contains the sample questions that came with your code.
Please verify each question, correct answer, explanation, subject, and year
against official UPSC papers and answer keys before treating them as authentic
PYQs. The quiz now returns no results when no questions match the selected
subject/year range; it will not substitute unrelated questions.

To add more questions, copy a QuestionModel(...) entry in the `dataset = [...]`
section of upsc_backend.py and change its subject, year, question, options,
correct_option, and explanation. Save the file and restart the backend. New
entries are added without wiping or duplicating the existing database rows.

The app selects questions from the database. This is the right way to present
actual past-year questions: an AI model should not invent a question and label
it as an official PYQ. You can add AI-written explanations later, with review.

Where the database is stored
----------------------------
The backend creates upsc_prep.db in the folder where you start it. The updated
backend no longer deletes this database every time it starts.
