
# Shortest Path to College

All roads lead to the college! :D

More precisely, to the Jadranska station (located at the [Faculty of Mathematics and Physics, University of Ljubljana, Slovenia](https://www.fmf.uni-lj.si/sl/studij-matematike/)), but let's ask ourselves:
- What is the fastest way to get from your home bus station to the desired bus stop anyway?
- Is it even possible to reach our goal with a direct connection to where we want?
- If possible, how long would it take and what would be the optimal route?

The present project answers the questions posed above and packages it all into a nice online service.

## Back End

It is clear that we can assign nodes and weighted links to some set of road connections and stops, and to them we can arrange a weighted **graph**. Therefore, in order to find the shortest route from one stop, it is a good idea to save the data in the form of a graph (data file `grafov.json`), whose weights are not necessarily independent of the graph search time.

The task of this project is to find an optimal path between two nodes in a multi-component graph with the stop FMF as the only common among them all.

We can walk along some links or we ride a bicycle, and after others we ride a bus. That's why I'm dividing my *links into 2 parts*:

1. **Connections whose weight varies with time** (in the data_graphs file, these are saved with a weight value of -1). When we search for the cheapest route, the current weight of this connection will have to be calculated from the text files (saved in the Departure Data folder) every time.
2. **Fixed weight links** independent of lookup time (stored with any positive value in graph_data file)

Later, I added the `type_of_connection' attribute to each connection, which tells if the user will travel by bus, train, walk, or ride a local bicycle from the beginning to the end of the connection. This functionality can be seen by pressing the button *show details -->* on the main page of the portal.

In the `model.py` file, I set about programming the objects that appear in my program:
- **Model**: The umbrella object that connects my program. It consists of individual graphs (driving lines),
- **Vozlišče (Node)**, which represents a stop for us,
- **Povezava (Connection)** that connects two nodes and presents us with some connection between them
- **Graf (Graph)** connecting nodes and links,
- **Uporabnik (User)**, who is responsible for recording the user's previous searches and his (her) "favorite relationships",
- **Iskanje (Search)**: Contains information on the place of departure and arrival, the search date, the price of the optimal walk, the cheapest route in this graph (if the searched nodes lie in the same component. I call them "lines" in the web service).

## Front End

To enhance the user experience, I then equipped each node with a **search frequency** parameter, which I used to *display the user's most popular nodes* (a node is popular if it has been visited many times). I did the same for all users at the same time, and then compared the results under the *najkrajsa-voznja/analiza-postajališč/* section.

In the front-end, I provided a **web service that supports multiple users**. Each user accesses their account via a username and password. I should also mention that all the objects mentioned above are equipped with methods for storing and reading data. Therefore, the user can close the program, come back the next day and still see their previous searches. This is where the python library *bottle.py* saved me a lot of time. I embellished the user experience with HTML files and *Bulma's CSS file framework*.

I added a variable called **številke linij (linenumbers)** to the user, which *keeps us information about the individual's favorite relations*. In this way, the user can log in, add a favorite route, log out, forget which line he usually takes, log back in and refresh his memory with the information obtained.

## Instructions for use

You run the program by running the `spletni_vmesnik.py.` (web_interface in Slovenian) file. If you don't already have the `hashlib' and `dateutil' Python libraries, you will need to download them in order to use this program.

## Further research

Graph algorithms are (unfortunately) not yet covered in the 1st year, but if anyone is interested, I would redirect them to:
- [The Algorithm Bible](https://edutechlearners.com/download/Introduction_to_algorithms-3rd%20Edition.pdf)
- [Article about the Dijkstra algorithm, which is also implemented in this program](https://www.programiz.com/dsa/dijkstra-algorithm)
- [Video about Dijster's algorithm](https://www.youtube.com/watch?v=GazC3A4OQTE)
- Contact for questions about this project: erzen.tjaz@gmail.com

## Author

Tjaž Eržen, student of Financial Mathematics
