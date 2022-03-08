# VV Pizzas

![Website Mockup]()

[Link to Live Website](https://vv-pizzas.herokuapp.com/)

[GitHub Repo](https://github.com/RickofManc/vv-pizzas)


***

## About

Vera's Vegan Pizzas is a popular South Manchester based food truck. The popularity of this delicious "can't believe it's vegan" pizza often leads to long wait times to order. Whilst most customers are happy to wait, Vera feels she is losing customers before they order due to the phone ordering system. There is a single point of contact to place orders via phone, and if this is frequently engaged, some customers will order elsewhere.  


***


## Index - Table of Contents

* [User Experience R&D](#user-experience-research-and-design)
    * [Strategy](#Strategy)
    * [Scope](#Scope)
    * [Structure](Structure)
    * [Skeleton](#Skeleton)
    * [Surface](#Surface)
* [Features](#Features)
* [Testing](#Testing)
* [Deployment](#Deployment)
* [Credits](#Credit)


***


## User Experience Research and Design


### Strategy

Vera requires a solution that provides another method for customers to place orders. An online based ordering system should be simple and clear in design and layout and take a similar duration to ordering by phone. 

A successful solution should reduce the amount of calls Vera is handling to allow her to focus on cooking.
Furthermore, as the orders as received digitally to a Google based spreadsheet, Vera will be able to execute them in order from viewing the spreadsheet on a digital device.

There are additional benefits of moving to a digitally driven ordering system; in that Vera will have order data and her fingertips. Allowing Vera to analyse and forecast stock levels for a particular day and/or location far easier than the current paper based method.


#### Leading User Stories

* As a customer, I want to place an order with VV Pizzas at the first time of trying, so that I don't have to keep calling back.
* As a customer, I want to understand how long it will take to cook my order, so that I can plan my journey time.
* As a customer, I want to learn which pizzas are available, so I can choose my preferred option.
* As a customer, I want to learn which sizes are available, so I can choose the appropriate size for my appetite.
* As a customer, I want to order multiple pizzas, so I can provide food to more people.
* As a customer, I want to be able to amend the order before committing, so that if a mistake is made I don't have to restart the order.
* As the owner, I want to reduce the time spent on the phone and writing orders, so I can focus on executing the orders.
* As the owner, I want to provide an easier method of ordering pizza, so that our customers are happier.
* As the owner, I want to be able to control when we can and can't receive orders, so that the kitchen does not become overloaded and the wait time for customers increases.
* As the owner, I want to have data from the days orders, so that I can learn of customers trends and forecast more accurately.


#### Primary strategic aims for the website
* The application will provide a method of receiving and executing orders from Vera's customers.
* The application will be intuitive for the customer to follow, and take a similar amount of time as if ordering by phone.
* Customers who had previously ordered elsewhere due a continually engaged phone line, will place an order with Vera, which in turn will increase revenue.


The roadmap below highlights the high-level strategic opportunities versus the importance and viability/feasibility of development for the MVP (Minimal Viable Product):

![Strategic Opportunities Roadmap](readme-images/strategic-opportunities-roadmap.png)


### Scope

An agile approach of keeping the in scope features simple and aligned to the strategy for the MVP will be adopted.
Below is a list of the leading features for the application.

#### In Scope Features
* Create an online interface for customers to place orders.
* A welcome message.
* Options for ordering different pizza sizes.
* Options for ordering different pizza toppings.
* On screen confirmation of the order before placing with Vera.
* Provide the order details in a spreadsheet to Vera as they are received.

#### Potentially In Scope Features (Time Dependant for MVP launch)
* Provide the customer with a price to be paid on collection.
* Add the value of each order within the spreadsheet.
* Add totals for the days orders within the spreadsheet.

#### Out of Scope Features (for a future release)
* Options for ordering custom toppings.
* Email confirmation of the placed order.
* Provide the customer with the opportunity to pay online.
* Provide the customer with an expected wait time dependent on current live orders.


### Structure

This website will be structured with the following design considerations;
* The customer will be welcomed to the CLI (Command Line Interface) with a welcome message from Vera.
* The customer will be asked for basic details, including their name which could be used as the order reference for the MVP.
* The customer will then be asked which pizza they would like from the menu.
* This will be followed by the size of pizza they would like; Small, Medium, Large
* Confirmation of their order will be provided, asking them whether they would like to place the order, or order anything else.
* If the customer needs to order more items they will be navigated back the first ordering question.
* If the customer has requested all items then the order will be placed and the Google Sheet updated for Vera.
* Finally the customer will be thanked and informed of the time for collection. customer.


### Skeleton

Key to the UX attributes is the ease for which customers can place an order. Therefore the website will contain a simple interface that immediately welcomes the customers and takes them through the process with minimal inputs.

The journey should take a similar amount of time to when ordering by phone which should ensure no customers are lost with the change in method. 

Aesthetically the page background will inform the customer they are ordering pizza, whilst emoji's will be used within the interface to communicate some fun. However, they will not be used to replace words to avoid any confusion with the customer.

Should the customer make an error whilst ordering, they will have the ability to amend the order before committing, or by clicking a 'Restart Order' button.

As part of this phase wireframes for monitor and smartphone have been produced using [Balsamiq](https://balsamiq.com/wireframes/) (see image below - the wireframes are located within the project [Repo](https://github.com/RickofManc/vv-pizzas)).

The website is responsive through differing screen widths and mobile devices. 

![Wireframes](readme-images/vv-pizza-wireframes.png)



### Surface 

The key aim for the MVP launch is to have a readable interface for the customer to order. With this in mind the surface theme has retained a simple amd clean style.


#### Colour 

The colour palette signals 'Italy' to the customer, to convey the link with the Italian food of pizza. The Savoy Azure Blue works well around the webpage as a bold colour to communicate information to the customer, it does not work as well within the interface against the black background. Where as the Green and Red from the Italian flag are still readable within the interface, whilst not being overly used to ensure all critical text is readable.

![VV Pizza Palette](readme-images/vv-pizza-colour-palette.png)


#### Fonts






#### Images & Icons

To provide .

***

## Features

### Current Features

*

##### Meta data

To support the strategic aim 'Educate on the impact of burning fossil fuels on Climate Change', Meta data has been included within the website HTML head element to increase the traffic to this website. Furthermore the site page has been titled appropriately as another method of informing users of their location.

##### Redirection

A '404 Not Found' page has been added to the website in the event of a failed link or page. This page kindly informs the user of the error and provides a button to navigate them back to VV Pizzas website.


### Future Features

Following a successful MVP launch, the application had the opportunity to be further developed over a relatively short period to improve the user experience. Here are a few of the immediate features that can be developed:
* Provide a fully functioning website that offers more information on VV Pizzas
* Provide a opportunity to pay online prior to collection
* Provide a real-time update on the order to customer via email/SMS.


***


## Data Model 



***


## Testing 

Throughout the Build phase Chrome Developer Tools are used to ensure all pages are being developed to remain intuitive, responsive and accessible across all device widths. Primarily the pages were designed at 1920px wide reducing to 320px for mobile devices. These tools and others were used for the Testing phase. Full details and results of this phase can be found within the project [Repo](https://github.com/RickofManc/60-seconds-to-save-earth).

The following sections summarise the tests and results.


### Code 

The code on each file has been tested using the appropriate validation service; W3C Markup for HTML, W3C Jigsaw for CSS and PEP8 Online for Python.

Below are the summarised positive results from these tests:

* **run.py** - 0 Errors / 0 Warnings
* **index.html** - 0 Errors / 0 Warnings
* **404.html** - 0 Errors / 0 Warnings
* **style.css** - 0 Errors / 1 Warning 


### Browser



### Device




### Accessibility 

Each page has been tested using the [Wave (Web Accessibility Evaluation Tool)](https://wave.webaim.org/) where zero errors or alerts were identified.




### Performance 

Using Lighthouse performance testing within Chrome Developer Tools, all pages performance has been tested on both Desktop and Mobile devices. The results highlighted a slightly slower page load time than is recommended. This was primarily due to the browser attempting to load the JavaScript files at the same time as the DOM and CSS. To resolve this issue the 'defer' attribute was applied in the HTMl Script tags informing the Browser to prioritise the more critical page elements before the JavaScript. This helped to improve the user experience, and see the following positive results.

![Lighthouse Test Results]()


### User Stories

The leading user stories have been tested to ensure the priority aims of the website have been delivered. 
Below is a summary of the stories validation.

* 


### Issues

The issues listed in the table below we identified during March 2022.

*


## Deployment

This project was deployed using the steps below with version releasing active. Please do not make any changes to files within this repository as any changes pushed to the main branch will be automatically reflected on the live website. Instead please follow the second set of steps which guide you to forking and cloning the website where changes can be made without impact to the live website. Thanks!

1. Logged into [my GitHub repository](https://github.com/RickofManc/vv-pizzas)
1. Clicked on the "Settings" button in the main Repository menu.
1. Clicked "Pages" from the left hand side navigation menu.
1. Within the Source section, clicked the "Branch" button and changed from 'None' to 'Main' in the dropdown menu.
1. The page automatically refreshed with a url displayed.
1. Tested the link by clicking on the url.

The live website can be found here https://vv-pizzas.herokuapp.com/

To fork this website to either propose changes or to use as an idea for another website, follow these steps:
1. If you haven't yet, you should first set up Git. Don't forget to set up authentication to GitHub.com from Git as well.
1. Navigate to the [VV Pizza](https://github.com/RickofManc/vv-pizzas).
1. Click the 'Fork' button on the upper right part fo the page. It's in between 'Watch' and 'Star'.
1. You will now have a fork of the VV Pizzas repository added to your GitHub profile. Navigate to your own profile and find the forked repository to add the required files.
1. Above the list of forked files click the 'Code' button.
1. A drop-down menu will appear providing a choice of cloning options. Select the one which is applicable to your setup.
Further details on completing the final step can be found on GitHub's ['Fork a Repo'](https://docs.github.com/en/get-started/quickstart/fork-a-repo) page.


***


## Credit

### People

* Mentor Brian Macharia for guiding and advising throughout the projects lifecycle.
* Code Institute Slack community for peer reviewing the code.


### Python Libraries




### Software & Web Applications

* [Balsamiq](https://balsamiq.com/) - Used to build wireframes in the Skelton phase. 
* This website was coded using Python3, HTML5, CCS3 and JavScript with [GitPod](https://gitpod.io/) used for an IDE and [GitHub](https://github.com/) as a hosting repository.
* [W3schools](https://www.w3schools.com/) - Source of 'How to...' information throughout the build.
* [Stack Overflow](https://stackoverflow.com/) - Source of 'How to...' information on Python code.
* [Python Tutor](https://pythontutor.com/) - For testing sections of code.
* [FreeConvert](https://www.freeconvert.com/) - For converting and compressing images to improve performance.
* [Wave](https://wave.webaim.org/) - Accessibility Testing to ensure content is readable for all users.
* [HTML Validator](https://validator.w3.org/) - For validating HMTL code.
* [PEP8 Validator](http://pep8online.com/)  - For validating Python code.
* [Code Beautify](https://codebeautify.org/) - For validating the layout of all code.
* [IE NetREnderer](https://netrenderer.com/index.php) - For testing website functionality on IE versions 7-10.
* [LambdaTest](https://www.lambdatest.com/) - For cross browser testing on macOS versions of Safari and Opera.