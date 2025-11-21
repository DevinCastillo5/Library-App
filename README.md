# Documentation:

## CREATE A BRANCH:

- We all have to make sure to create a branch so we do not push to main. The more we divide the work the quicker we can get it done.
- After you do your work and push to your branch you can make a pull request and let the group chat know.

---

### Order of Task Priority:

1️⃣ Update Database + CRUD

- CRUD: Just create the equivalent create, read(get), update, and delete functions that you see for the university one but make it for our library.

  2️⃣ Update Schemas

- Most simple task, just make the schemas for the tables.

  3️⃣ Update Routes

- Very Important task as this is folder is what communicates directly with what our frontend will be. But these will just depend on the CRUD files which is why that needs to be done first.

  4️⃣ Update Views (Starlette Admin)

- Views will be updated to that we can test and debug everything that we just created. Doing this will allow all the backend stuff to be perfected before moving onto front end stuff

  5️⃣ Test & Debug with Admin UI (views)

- Test all functions so its good for frontend development

  6️⃣ Build Frontend

- TBD, most likely will start off with just HTML, but will take it from there depending on time left before presentation.

---

### INSTALL DEPENDENCIES!!:

You have to run:

pip install -r requirements.txt

In your terminal in order for everything to work. In the future we might add more into requirements.txt if we find something that makes our lives easier but for now we will just stick with what the hat guy gave us.

---

### Important Notes Concerning Certain Files/Folders:

1. /database.py

- You have to change this to make sure it matches what you named the library database in your MySQL
- When you pull and then start coding each time you have to change this.
- For the sake of the main branch, it will remain as Devin's sql file since we used it for the presentation.
- OR which is the probably the better option, just keep using Devin's since you will have it downloaded after you pull from main.

2. /z_tobedeleted

- This folder is just for us to store things that will ultimately be deleted, but still might hold value

3. **init**.py

- These are found in each folder, these are made to be empty and should not have anything in them, just move on to the other files in the folder.

4. pycache, .idea, .venv

- Do not touch these, these are mainly just stuff that come from PyCharm since he made this project using pycharm. But just incase I don't want anything changed inside of them. I added them to .gitignore so that it stays the same no matter what when you guys push to your branches.
