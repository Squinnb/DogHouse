Harvard CS50 Web Programming in Python and Javascript

Quinn Barnett Capstone Project


My Capstone project is a website/ecommerce shop for an Animal shelter made with Django, Python and Javascript. The shelter has a profile for each dog that is up for adoption and also a mini shop on their website. The website is complete with user authentication (register, log in, logout). The site is made mobile responsive with Bootstrap.


The index page features a Search function that allows users to search for any dog name or breed and will return a list of dogs that has a matching substring in their breed or name column. It also features an about me page which like the search function uses Javascript and DOM manipulation to show and hide itself. It also uses Django's paginator to display the dogs 9 at a time.

The dog details page for each dog displays all of their information from their database entry and a photo. I also used "thedogapi" (https://thedogapi.com/) by making a get request with the query being the breed of the dog and if that breed has a profile it returns an extra bit of info including the dog breeds temperment, life span etc. Users can add dogs they are interested to their watch list and also see how many other users are interested in (watching) each dog. That list is then displayed on the user's user page. When they visit the shelter the shelter staff can then look up the dogs they want to meet provided their email or username.

The shop features a few times that would be useful for any dog owner including dog treats, toys and leashes. You can add items to your cart in your desired quantity. The items in your cart will also show up on each users user page where you can delete an item and or make a purchase. Each item in the shop similar to the dog details page also has it's own page where it's information from the database is displayed.


The user page displays both the dogs the user is "watching" and the items in their shopping cart. To purchase items the user can go to checkout from the user page where they will be asked to confirm the details. After they purchase the items the order will be displayed along with a thank you message. The user page also links to a page where the user can, having made a purchase view their past orders. They are displayed with the date the order was made, the items purchased and the total. They are organized by order status "pending", "ready" and "complete". The admin of the site can after a order is made update the status of the order and it will be updated on the users my orders page.

My project uses five different models in it's database: User, Dog, Product, ShopItem and Order. 


I believe my capstone project satisfies the complexity and distinctivness requirements given my explanation of it above. 




I really enjoyed this course and think Brian is a great teacher. I got a lot out of it and it made me feel like a much more confident developer. Thanks!