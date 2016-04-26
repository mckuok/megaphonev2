Database Design for Users
=============

Database Structure
-------

| Attribute | Type |
| --------- | ---- |
| pk | Int  |
| name | String |
| email | String |
| password | hashed String |
| role | String |
| date_joined | Time |
| is_active | Boolean |
| is_staff | Boolean |
| subscribe_domain | String |
| subscribe_page | String |

-------
* pk: Primary key, unique
* name: Name of the user
* email: email of the user, used for login, unique
* password: password for the account, hashed, used for login
* role: Either as (M) Member, (P) PageAdmin, or (D) DomainAdmin
* date_joined: timestamp, generated when the account is created
* is_active: can be used to check if the user has activated the account, default to be true for now
* is_staff: superuser privilege, default to be false
* subscribe_domain: A string representation to store domains that the user subscribed to, formatted as: [pk1] [pk2] [pk3]   <-- without square brackets, where pk is the primary key for the domains
* subscribe_page: A string representation to store pages that the user subscribed to, formatted as: [pk1] [pk2] [pk3]   <-- without square brackets, where pk is the primary key for the pages
