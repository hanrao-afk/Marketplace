# UCSC Marketplace
## Authored by Ashwin, Aahaan, Avinash

### Purpose
Our site is meant to a be a Marketplace for UCSC students. It allows them to post products that they want to get rid of and meet up with other students to sell them

### Design 

#### Databases

We have two databases that we use. The first is the *listings* database. This allows us to keep track of all the listings. It has a 
- category: The category of the item, selected from a predefined set of options.
- condition: The condition of the item, selected from a predefined set of options.
- price: Price of the item, represented as an integer.
- image: The URL or text representation of the image associated with the item.
- description: The description of the item.
- creator: The email of the user who created the listing. This field is automatically populated with the email of the authenticated user who created the listing.

The next database is the *account_info* database. This has a 
- id: An auto-generated unique identifier for the account. It is not readable or writable directly
- email: The email address associated with the account. It is not writable directly
- phone: The phone number associated with the account, stored as a string
- payment: The preferred payment method, selected from a predefined set of options
- college: The UCSC college the student is associated with 

#### Pages

- index.html: This is the welcome page which shows a list of all items. Users can use a dropdown to filter by category. They can also search keywords that are in the names of items or description 
- description.html: This is the page when you click on a specific item. You can see the description as well as the seller info 
- account.html: This is the page where the user can enter their personal information. We have a field for phone number, college, and preferred payment method. The default values are N/A, other, other as follows. The user can also see their listings here where they can edit and delete them. 
- edit_listing.html: When a user tries to edit a listing, it brings them to this page
- category.html: The page contains all the items in a specific category. 
- add.html: The user can add a new listing to be displayed 
- layout.html: This contains our navbar and breadcrumbs code 


#### Important Functions 

- account: This function gets all the user information associated with the logged in email. If there is none, it inserts default values into the account_info database and allows the user to edit it. It also displays all the listings posting by that user
- add: The function allows us to add the listing. We use a custom form with image as an upload rather than a text as it is in the listings database. This is because we need to encode the base 64 url in order to store and display the image
- save_account_info: When the user inserts their account information, this function is used to add it to the database 
- description: The function allows us to look at the description and ownwer information for a listing
- filter: This allows the breadcrumbs and dropdown to work and filter the listings by category 
- edit_listing: This function allows the user to edit their listing that they have posted
- delete_listing: If a user has sold their item or no longer wants to sell it, they can delete their listing with this function 





