# BAKEMATES
by Haleigh Gahan, Rohith Gottiparthi, Clara Martinson, and Tina Tian

## Project Description
BAKEMATES is a platform connecting bakers and dessert enthusiasts. 

## User Instructions

### For All Users
#### Searching for Baked Goods
On the landing page, search for your desired pastries within your city using the search bar. This will bring you to the listing page displaying the items. If you do not type anything in the search bar, you can view all items in bakemates.


### For Tasters
#### Creating an Account
On any page, select `Sign up` at the top right corner, then select `Taster`. Fill out your information to create your account. To see your profile and order history go to `Hello [username]!!`. To edit your information, click on `Edit Profile` and fill out the optional information. Once you are finished purchasing baked goods to your heart's content, don't forget to `Log Out` of the application. `Sign in` to access your account again in the future.

#### Placing Orders
Clicking on the image of an item will bring your to the items page, where you can purchase the item by clicking `Buy now`. This will bring you to the checkout form. Here you can enter your address and information for the Baker to see. Clicking the Paypal button on the left side of the screen allows you to purchase the item with Paypal, after which you will be redirected to your profile where you can see your order information at the bottom of the screen.

#### Leaving a Review
On a Baker's public profile you are able leave a review by assigning a rating with comments. You are only able to leave one review that cannot be modified, so make sure your verdict is final.

### For Bakers
#### Creating an Account
On any page, select `Sign up` at the top right corner, then select `Baker`. Fill out your information to create your account. To edit your information, click on `Edit Profile` in your home page and fill out the optional information. Once you have finished setting up your shop, `Log Out` of the application. `Sign in` to access your account again in the future.

#### Managing Your Items
On the baker home page, scroll down to `Your Listings`, which shows the details of all of your current items available to customers. There, you can add new items, update existing items, or delete existing items by clicking on the respective buttons, then fill out the information about the item you want to add/modify/delete.

#### Checking and Fulfilling Orders
On the baker home page, scroll down to `Your Orders`, which shows the details of all of your current orders by customers. There, you update the status of orders for your customer to see.

## Dependencies
- .env file: You must create a .env file with the paypal client id and paypal secret (see example.env)
- DBMS: mysql
- flask
- flask_bcrypt
- mysql.connector
- paypalrestsdk
- os 
- datetime
- dotenv

## List of Other Resources
- Tutorial followed: https://www.w3schools.com/howto/howto_css_form_icon.asp
- W3 schools for html & css info, https://www.w3schools.com/html/
- search bar: https://www.youtube.com/watch?v=AmdIfgxMqY8&t=88s
- how to import custom fonts: https://www.youtube.com/watch?v=g15mF_XAOB8&t=500s
- Class slides for flask information
- https://www.mysql.com for info on sql
- SQL LIKE queries for searches: https://www.w3schools.com/sql/sql_like.asp
- Paper on distribution: GCP Website, https://endjin.com/blog/2022/01/introduction-to-containers-and-docker#:~:text=Docker%20is%20a%20containerisation%20platform,source%20platform%2C%20free%20to%20download., https://www.docker.com/resources/what-container/, https://www.atlassian.com/microservices/microservices-architecture/kubernetes-vs-docker, https://kubernetes.io

-Fonts: fonts.google.com

-Icons: https://fontawesome.com/search?o=r&m=free

- generated sample data using chatgpt

- Background photos:
https://unsplash.com/photos/brown-bread-on-silver-foil-V6LEV6CBVLw

https://unsplash.com/photos/a-painting-of-pink-and-white-lines-on-a-wall-V1lmayjfBJc

https://unsplash.com/photos/brown-and-white-round-pastry-on-white-ceramic-plate-71sp4JBYO-U

https://www.freepik.com/free-photo/copy-space-ingredients-cookies_12242994.htm#query=baking&position=3&from_view=keyword&track=sph&uuid=33af41f4-c5cb-497d-8fa8-2ee033a2320b

## Division of Labor
- **Database set up**: Rohith Gottiparthi, Tina Tian
- **Role-based access control**: Tina Tian
- **HTML/CSS for most of the web pages**: Haleigh Gahan, Clara Martinson
- **Sign up/login**: Haleigh Gahan, Clara Martinson, Tina Tian
- **User profiles**: Rohith Gottiparthi, Tina Tian
- **Search and filter items**: Haleigh Gahan, Tina Tian
- **Add, update, delete items**: Clara Martinson, Tina Tian
- **Public profile for the bakers**: Rohith Gottiparthi, Clara Martinson
- **Placing and fulfilling orders**: Rohith Gottiparthi, Clara Martinson
- **Reviews**: Rohith Gottiparthi, Tina Tian
- **Documentation and paper on distribution**: Haleigh Gahan, Rohith Gottiparthi, Clara Martinson, Tina Tian

## Image Sources
- **BK001.jpg**: https://www.yourfreecareertest.com/baker/
- **BK002.jpg**: https://www.indeed.com/career-advice/finding-a-job/pastry-chef-vs-baker
- **BK003.jpg**: https://www.seattletimes.com/life/food-drink/a-seattle-area-tax-accountant-and-baker-competes-on-top-chef-amateurs/
- **apple-pie.jpg**: https://www.inspiredtaste.net/43362/apple-pie/
- **banana-bread.jpg**: https://joyfoodsunshine.com/best-banana-bread-recipe/
- **blueberry-muffins.jpg**: https://kitchenswagger.com/the-best-blueberry-muffin-recipe/
- **chocolate-cake.jpg**: https://bluebowlrecipes.com/chocolate-truffle-cake-with-milk-chocolate-buttercream/
- **croissant.jpg**: https://en.wikipedia.org/wiki/Croissant
- **beth-macdonald-V6LEV6CBVLw-unsplash.jpg**: https://unsplash.com/photos/brown-bread-on-silver-foil-V6LEV6CBVLw
- **annie-spratt-V1lmayjfBJc-unsplash.jpg**: https://unsplash.com/photos/a-painting-of-pink-and-white-lines-on-a-wall-V1lmayjfBJc
- **copy-space-ingredients-cookies.jpg**: https://www.freepik.com/free-photo/copy-space-ingredients-cookies_12242994.htm#query=baking&position=3&from_view=keyword&track=sph&uuid=33af41f4-c5cb-497d-8fa8-2ee033a2320b
- **cupcake-icon-614x460.jpg**: https://fontawesome.com/search?o=r&m=free
- **taylor-heery-71sp4JBYO-U-unsplash.jpg**: https://unsplash.com/photos/brown-and-white-round-pastry-on-white-ceramic-plate-71sp4JBYO-U