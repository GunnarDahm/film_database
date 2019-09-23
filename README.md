<h1> Film Database Retrieval and Analysis</h1>

<h2> Status: In Progress </h2>

<h2> Purpose </h2>
<p> The purpose of this project is retrieve film data from OMDB and create a localized SQLite databse, with 
the ability to export tables as a CSV filetype.</p>

<h2> Methods Used </h2>

<ul>
<li>Relational Databases</li>
<li>SQLite</li>
<li>OMDB API</li>
</ul>

<h2> Technologies </h2>
<ul>
<li>Python (v.3.7)</li>
</ul>

<h2> Required Libraries </h2>
<ul>
<li>Pandas</li>
<li>SQLite</li>
</ul>

<h2> Project Description </h2>

<p>
This project utilizes the OMDB API (<a href="http://www.omdbapi.com/">
See Here </a>) to retreive film data in the form of a .json file and saves it to a localized 
SQLite database. This retreival process saves the posters of each film retrieved to a local directory as well. 
Currently, the film information is stored in 4 tables; Movies, Actors, Directors, and Writers. Each table has the title 
as a common key. 
</p>

<p>
The film_retrieval.py has functions to initialize a database and then add individual films to specified databases. The 
table_export.py has basic user input for SQL commands for the purposes of exporting tables as csv from the SQLite 
database. 
</p>

<p>
The database, posters, and tables directories currently within this repo are for example purposes and are not 
necessary to retain for function. The directories will automatically be created and populated with the use of the 
scripts. 
</p>

<h2> To Use: </h2>

<p>
To create a database, first ensure the above python libraries are installed. Also,
 you will first need a OMDB API key, which can be acquired from <a href="http://www.omdbapi.com/">
 here </a>. Once acquired the API key must be inputted as a parameter in the film_retrieval script. Run the 
 create_database function to name and create a database. The database will then be saved as SQLite file in the database
 directory. Run the search_movie function to search films by title. Added movies, directors, actors, and writers will
 be added to the appropriate tables within the specified database. Posters retrieved for each film will be saved to the 
 posters directory.

</p>

<p>
Running the table_export.py script will prompt you for input of a SQL command to generate a table from the specified 
database. The database the script connects to will need to be changed in the parameters section. 
Note that the final ";" is not necessary for input and the command disallows for the input of new lines, 
unfortunately. The generated table will be saved to the tables directory under the inputted name. 
</p>

<h2> To Do: </h2>
<ul>
<li>Add in a Twitter sentiment analysis function to retrieve current sentiment data using the Twitter API</li>
</ul>


<h2> Author:</h2>
<p> Gunnar Dahm </p>