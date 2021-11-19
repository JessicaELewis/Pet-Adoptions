# Pet Adoption Prediction
**Can we predict how long a cat or dog will be available for adoption before they find their forever home?**

I focused on the cities in King County, Washington for 2 reasons: 1. Using the whole country or world was too much. 2. I live here.

## Data

<ul>
    <li>[Petfinder API](https://www.petfinder.com/user/developer-settings/)</li>
    <li>US Census - Demographics for cities in King County Washington</li>
</ul>


## Data cleaning

<ul>
    <li>Cats and dogs are processed separately. Each step had to be completed for each species.</li>
    <li>Made a function for preprocessing the data that can be used for future data that will be used for predictions as well as for the training/testing.
        <ul>
            <li>Some columns in the dataset housed dicts. These were pulled out into their own columns.</li>
            <li>Dropped unnecessary columns</li>
            <li>Removed duplicates</li>
        </ul>
    </li>
    <li>Each record included the ID of the organization that is responsible for the animal. I grabbed the org's city using the API's organization call and replaced the IDs with their city name.</li>
</ul>

## Feature Engineering

<ul>
    <li>I subtracted 'published_at' from 'status_changed_at' to make a new column called 'duration_as_adoptable' to describe how long the animal was at the shelter before being adopted. This is the dependent variable.</li>
</ul>

## EDA

**Dependent Variable: duration_as_adoptable**

First, I wrote out a few questions and found the answers in the data:

**Q:** Do larger cities have faster average adoption rates?<br />
    **A:** The size of a city doesn't have as strong a correlation to adoption rates as I expected

**Q:** Does average age of the city's human population affect adoption rates?<br />
    **A:** Average age of humans is not a good indicator of pet adoption rate

**Q:** What are the most adopetd breeds?<br />
    **Cats:** Domestic Shorthair<br />
    **Dogs:** Chihuahua


## Feature Selection



## Machine learning models

## Model selection and performance
