## civic14
The Merge Conflictors (1-14)'s app for Civic Connect.

Deployed to Heroku @ [civic14.herokuapp.com](https://civic14.herokuapp.com/).

---
**Comprehensive List of Features / User Guide**:
- Templates
    - Every Template must have a Topic. Thus, the user is required to link the Template to a Topic.
    - On the Create screen (`/templates/create`), the user is directed to specify *replacement tags*. These are direct text replacement strings, that, when put through the email generation feature, replace the strings with their respective values.
    - The user must select an affiliation of the Template to create.
    - On the **Email Body** field, a real-time verification that the required replacement tags is shown for the user. The red badges turn green when the replacement tag is included in the email body. The user is unable to submit the template without adding these tags.
    - The above applies to the Template edit screen (`/templates/<id>/edit`).
    - Templates must be approved by an Administrator before displaying on the Topic Index (`/templates`).
- Editing Templates & Topics
    - On the Template/Topic detail screen, a pencil icon is shown to the user in the top right if they are the author of the Template/Topic. Clicking on the icon, the user is able to edit the Template/Topic and see the existing information pre-filled in.
- User Liked Templates & Topics
    - On the detail screens of the Template page (`/templates/<id>`) and Topic page (`/topics/<id>`), in the top right a star is shown. When clicked the Template/Topic is added to the user's liked items. When clicked again, the Template/Topic is removed from the user's liked items.
    - The liked/starred indicator is displayed on **multiple pages**, including the Template/Topic indexes, the email generation screen, and on the user's profile page
- Account Management & User Profiles
    - As a Guest, the user is unable to create templates/templates or like templates or topics. Once logged in via Google, the **Log In** tab is replaced by an **Account** dropdown with two options: **My Profile** and **Log Out**.
    - Clicking on the **My Profile** from the dropdown, the user is directed to their profile. Here they can view their profile picture, account name, account email, edit/update their contact information, and view their liked Templates/Topics.
    - Other users' profiles are accessible to everyone, even Guests. User profiles are hyperlinked on the Template/Topic detail pages. If the current logged in user does not match the profile being viewed, the contact information form is removed.
- Representatives and Automatic Email Generation
    - When the user clicks on the **Representatives** tab (`/representatives`), they are directed to a search screen. If the user is logged in and has entered in any of the address fields on their **Profile**, these will be automatically filled into the search bar.
    - Clicking **Find** the user is directed to the **Elected Officials** results page, which displays the searched address along with the officials in that area. This feature uses the [Google Civic Information API](https://developers.google.com/civic-information). A table shows the name (clicking on the name the image of the official is shown), party, phone number, email, and actions. The user is able to return to the search screen.
    - Clicking on the email icon under the Actions column for the desired official, the user is shown the **Template Selection Screen**. Here, the user can choose which template they would like to use to generate the email, as well as fill in the other required fields. In the Template dropdown, a ★ is shown to indicate if the user has liked the template.
    - After all field validations have passed, and clicking on **Generate Email** the user is directed to the **Generated Template** screen. The original Template text is modified per the direct text replacement tags. Here, the user can click on the **Send Email** button to open their email client with the entire email auto-filling in the client.
    